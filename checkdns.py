import argparse
import gzip
import json
import os
import re
import zlib
from collections import defaultdict
from typing import List, Dict, Any, Union


def list_files(directory: str, extension: str = ".txt") -> List[str]:
    """
    List all files in a directory with a specific extension.
    If --gzip option is provided, constrain to .txt.gz files.
    """
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if extension == ".txt" and filename.endswith(".txt"):
                files.append(os.path.join(root, filename))
            elif extension == ".txt.gz" and filename.endswith(".txt.gz"):
                files.append(os.path.join(root, filename))
    return files


def process_zone_file(filename: str) -> List[str]:
    """
    Process a zone file and extract records.
    """
    records = []
    with open(filename, 'rb') as f:
        # Check if file is gzip compressed
        magic = f.read(2)
        f.seek(0)
        if magic == b'\x1f\x8b':
            f = gzip.open(f, 'rt', encoding='utf-8')
        for line in f:
            line = line.strip()
            # Process line here (e.g., extract IPs, nameservers, etc.)
            # Example regex to extract nameservers:
            nameserver_match = re.match(r'^\s*([\w.-]+)\s+IN\s+NS\s+([\w.-]+)\s*$', line)
            if nameserver_match:
                records.append(nameserver_match.group(2))
            # Other record types can be processed similarly
    return records


def extract_nameservers(filename: str) -> List[str]:
    """
    Extract nameservers from a zone file.
    """
    return process_zone_file(filename)


def extract_ips(filename: str) -> List[str]:
    """
    Extract IP addresses from a zone file.
    """
    return process_zone_file(filename)


def extract_records_with_nameserver(filename: str, nameserver: str) -> List[str]:
    """
    Extract records associated with a specific nameserver from a zone file.
    """
    records = []
    with open(filename, 'rb') as f:
        # Check if file is gzip compressed
        magic = f.read(2)
        f.seek(0)
        if magic == b'\x1f\x8b':
            f = gzip.open(f, 'rt', encoding='utf-8')
        for line in f:
            line = line.strip()
            if nameserver in line:
                records.append(line)
    return records


def extract_record_types(filename: str) -> List[str]:
    """
    Extract all record types from a zone file.
    """
    types = set()
    with open(filename, 'rb') as f:
        # Check if file is gzip compressed
        magic = f.read(2)
        f.seek(0)
        if magic == b'\x1f\x8b':
            f = gzip.open(f, 'rt', encoding='utf-8')
        for line in f:
            line = line.strip()
            type_match = re.match(r'^\s*\S+\s+\d+\s+IN\s+(\S+)\s+', line)
            if type_match:
                types.add(type_match.group(1))
    return list(types)


def main(args: argparse.Namespace) -> None:
    results = defaultdict(list)

    # List all files to process
    input_files = []
    for input_path in args.inputs:
        if os.path.isdir(input_path):
            if args.gzip:
                input_files.extend(list_files(input_path, extension=".txt.gz"))
            else:
                input_files.extend(list_files(input_path))
        elif os.path.isfile(input_path):
            input_files.append(input_path)

    if not input_files:
        print("No valid input files found.")
        return

    for filename in input_files:
        if args.list_nameservers:
            results['nameservers'].extend(extract_nameservers(filename))
        if args.list_ips:
            results['ips'].extend(extract_ips(filename))
        if args.nameserver:
            results['records_with_nameserver'].extend(extract_records_with_nameserver(filename, args.nameserver))
        if args.list_record_types:
            results['record_types'].extend(extract_record_types(filename))

    # Output results based on options
    if args.output_format == 'json':
        output = json.dumps(results, indent=4)
        if args.output_file:
            with open(args.output_file, 'w') as f:
                f.write(output)
        else:
            print(output)
    elif args.output_format == 'txt':
        # Example text output (customize as needed)
        for key, value in results.items():
            print(f"{key}:")
            for item in value:
                print(item)
    else:
        print("Unsupported output format. Please choose 'json' or 'txt'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNS TLD zone file processor")
    parser.add_argument("inputs", nargs="+", help="Input zone files or directories")
    parser.add_argument("--gzip", action="store_true", help="Constrain input to .txt.gz extensions")
    parser.add_argument("--list-nameservers", action="store_true", help="List all nameservers within input")
    parser.add_argument("--list-ips", action="store_true", help="List all IP addresses within input")
    parser.add_argument("--nameserver", type=str, help="List all records with a specific nameserver within input")
    parser.add_argument("--list-record-types", action="store_true", help="List all record types within input")
    parser.add_argument("--output-format", choices=["json", "txt"], default="json", help="Output format")
    parser.add_argument("--output-file", type=str, help="Output file path")
    
    args = parser.parse_args()
    main(args)
