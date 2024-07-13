import argparse
import os
import gzip
import re
import json
from collections import defaultdict
from typing import List, Dict, Union
import socket

def read_zone_file(filename: str) -> str:
    """Reads and returns content of a zone file, handles gzipped files."""
    if filename.endswith('.gz'):
        with gzip.open(filename, 'rt') as f:
            content = f.read()
    else:
        with open(filename, 'r') as f:
            content = f.read()
    return content

def parse_zone_file(content: str) -> List[Dict[str, Union[str, List[str]]]]:
    """Parses DNS TLD zone file and returns a list of records."""
    records = []
    current_record = None

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith(';'):
            continue  # skip empty lines and comments
        elif line.startswith('$ORIGIN'):
            continue  # handle $ORIGIN if needed
        elif line.startswith('$'):
            continue  # skip other $ directives for now
        elif re.match(r'^\S+\s+\d+\s+IN\s+[A-Z]+\s+', line):
            if current_record:
                records.append(current_record)
            parts = re.split(r'\s+', line.strip(), maxsplit=4)
            current_record = {
                'name': parts[0],
                'ttl': parts[1],
                'class': parts[2],
                'type': parts[3],
                'data': [parts[4].strip()]
            }
        elif current_record and line.startswith(' '):
            current_record['data'].append(line.strip())
        else:
            continue  # handle other record types as needed

    if current_record:
        records.append(current_record)

    return records

def list_record_types(records: List[Dict[str, str]]) -> List[str]:
    """Lists all unique record types present in the zone file."""
    return list(set(record['type'] for record in records))

def list_records_by_type(records: List[Dict[str, str]], record_type: str) -> List[Dict[str, str]]:
    """Lists all records of a specific type."""
    return [record for record in records if record['type'] == record_type]

def list_ip_addresses(records: List[Dict[str, str]]) -> List[str]:
    """Lists all IP addresses present in A or AAAA records."""
    ip_addresses = set()
    for record in records:
        if record['type'] in ['A', 'AAAA']:
            for data in record['data']:
                try:
                    ip = socket.gethostbyname(data)
                    ip_addresses.add(ip)
                except socket.gaierror:
                    pass  # Handle DNS resolution errors if needed
    return list(ip_addresses)

def list_name_servers(records: List[Dict[str, str]]) -> List[str]:
    """Lists all name servers present in NS records."""
    name_servers = set()
    for record in records:
        if record['type'] == 'NS':
            name_servers.update(record['data'])
    return list(name_servers)

def list_records_by_nameserver(records: List[Dict[str, str]], nameserver: str) -> List[Dict[str, str]]:
    """Lists all records served by a specific name server."""
    filtered_records = []
    for record in records:
        if 'NS' in record and nameserver in record['NS']:
            filtered_records.append(record)
    return filtered_records

def list_records_by_type_by_ip(records: List[Dict[str, str]], record_type: str, ip_address: str) -> List[Dict[str, str]]:
    """Lists all records of a specific type served by a specific IP address."""
    filtered_records = []
    for record in records:
        if record['type'] == record_type:
            for data in record['data']:
                try:
                    if ip_address == socket.gethostbyname(data):
                        filtered_records.append(record)
                except socket.gaierror:
                    pass  # Handle DNS resolution errors if needed
    return filtered_records

def sanitize_filename(filename: str) -> str:
    """Sanitizes the filename to prevent directory traversal."""
    return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

def process_directory(directory: str) -> List[str]:
    """Returns a list of file paths for .txt and .txt.gz files in the directory."""
    file_paths = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt') or filename.endswith('.txt.gz'):
            file_paths.append(os.path.join(directory, filename))
    return file_paths

def output_to_stdio(records: List[Dict[str, str]], output_types: List[str]):
    """Outputs results to standard output (stdio) based on selected output types."""
    for output_type in output_types:
        if output_type == 'json':
            print(json.dumps(records, indent=2))
        elif output_type == 'txt':
            for record in records:
                print(record)
        else:
            print("Unsupported output type. Please use 'json', 'txt', or 'stdio'.")

def output_to_file(records: List[Dict[str, str]], output_types: List[str], filename: str):
    """Outputs results to JSON or TXT file based on selected output types."""
    for output_type in output_types:
        if output_type == 'json':
            with open(filename + '.json', 'w') as f:
                json.dump(records, f, indent=2)
        elif output_type == 'txt':
            with open(filename + '.txt', 'w') as f:
                for record in records:
                    f.write(str(record) + '\n')
        else:
            print("Unsupported output type. Please use 'json' or 'txt'.")

def compare_zone_files(records_old: List[Dict[str, str]], records_new: List[Dict[str, str]]) -> Dict[str, List[str]]:
    """Compares two sets of DNS TLD zone files and returns added and removed domains."""
    old_domains = set(record['name'] for record in records_old)
    new_domains = set(record['name'] for record in records_new)

    added_domains = list(new_domains - old_domains)
    removed_domains = list(old_domains - new_domains)

    return {'added_domains': added_domains, 'removed_domains': removed_domains}

def main():
    parser = argparse.ArgumentParser(description='Process DNS TLD zone files and provide various outputs.')
    parser.add_argument('path_old', type=str, help='Path to old DNS TLD zone file or directory')
    parser.add_argument('path_new', type=str, help='Path to new DNS TLD zone file or directory')
    parser.add_argument('--compare', action='store_true', help='Compare old and new zone files and list added/removed domains')
    parser.add_argument('--list-record-types', action='store_true', help='List all record types present')
    parser.add_argument('--list-records-by-type', metavar='RECORD_TYPE', type=str, help='List all records of a specific type')
    parser.add_argument('--list-ip-addresses', action='store_true', help='List all IP addresses present in A or AAAA records')
    parser.add_argument('--list-name-servers', action='store_true', help='List all name servers present in NS records')
    parser.add_argument('--list-records-by-nameserver', metavar='NAMESERVER', type=str, help='List all records served by a specific name server')
    parser.add_argument('--list-records-by-type-by-ip', metavar=('RECORD_TYPE', 'IP_ADDRESS'), nargs=2, help='List all records of a specific type served by a specific IP address')
    parser.add_argument('--output-types', metavar='OUTPUT_TYPES', nargs='+', choices=['stdio', 'json', 'txt'], default=['stdio'], help='Output types (default: stdio)')
    args = parser.parse_args()

    path_old = sanitize_filename(args.path_old)
    path_new = sanitize_filename(args.path_new)

    if os.path.isdir(path_old):
        file_paths_old = process_directory(path_old)
    elif os.path.isfile(path_old):
        file_paths_old = [path_old]
    else:
        print("Error: Path for old files must be a directory or file.")
        return

    if os.path.isdir(path_new):
        file_paths_new = process_directory(path_new)
    elif os.path.isfile(path_new):
        file_paths_new = [path_new]
    else:
        print("Error: Path for new files must be a directory or file.")
        return

    records_old = []
    for file_path in file_paths_old:
        try:
            content = read_zone_file(file_path)
            records_old.extend(parse_zone_file(content))
        except (FileNotFoundError, IOError) as e:
            print(f"Error: File '{file_path}' not found or could not be read.")
            continue

    records_new = []
    for file_path in file_paths_new:
        try:
            content = read_zone_file(file_path)
            records_new.extend(parse_zone_file(content))
        except (FileNotFoundError, IOError) as e:
            print(f"Error: File '{file_path}' not found or could not be read.")
            continue

    if args.compare:
        comparison_result = compare_zone_files(records_old, records_new)
        output_to_stdio(comparison_result, args.output_types)

    if args.list_record_types:
        output_to_stdio(list_record_types(records_new), args.output_types)

    if args.list_records_by_type:
        records_of_type = list_records_by_type(records_new, args.list_records_by_type)
        output_to_stdio(records_of_type, args.output_types)

    if args.list_ip_addresses:
        ip_addresses = list_ip_addresses(records_new)
        output_to_stdio(ip_addresses, args.output_types)

    if args.list_name_servers:
        name_servers = list_name_servers(records_new)
        output_to_stdio(name_servers, args.output_types)

    if args.list_records_by_nameserver:
        records_by_ns = list_records_by_nameserver(records_new, args.list_records_by_nameserver)
        output_to_stdio(records_by_ns, args.output_types)

    if args.list_records_by_type_by_ip:
        record_type, ip_address = args.list_records_by_type_by_ip
        records_by_type_by_ip = list_records_by_type_by_ip(records_new, record_type, ip_address)
        output_to_stdio(records_by_type_by_ip, args.output_types)

    if 'stdio' not in args.output_types:
        output_filename = os.path.splitext(file_paths_new[0])[0] + '_processed'
        output_to_file(records_new, args.output_types, output_filename)

if __name__ == '__main__':
    main()
