import gzip
import sys
import concurrent.futures
import argparse
from collections import Counter

# Define DNS record types
VALID_RECORD_TYPES = {"a", "aaaa", "dnskey", "ds", "ns", "nsec3", "nsec3param", "rrsig", "soa"}

def process_line(line):
    # Strip any trailing newline or space characters
    line = line.strip()
    # Split the line into fields based on whitespace
    fields = line.split()
    return fields

def filter_records(file_path, record_type, name_server, num_threads):
    try:
        with gzip.open(file_path, 'rt') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return
    except IOError:
        print(f"Error: An error occurred while reading the file {file_path}.")
        return

    # Function to filter lines based on record type and name server
    def filter_line(line):
        fields = process_line(line)
        if len(fields) < 3:
            return None  # Invalid line
        current_record_type, current_name_server = fields[2].lower(), fields[1].lower()
        if current_record_type == record_type and current_name_server == name_server:
            return line
        return None

    # Use ThreadPoolExecutor to filter lines concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(filter_line, lines))

    # Filter out None results and print matching lines
    matching_lines = [result for result in results if result is not None]
    if matching_lines:
        print(f"\nFiltered Records for Type '{record_type.upper()}' and Name Server '{name_server}':\n")
        for line in matching_lines:
            print(line.strip())
    else:
        print(f"\nNo records found for Type '{record_type.upper()}' and Name Server '{name_server}'.")

def list_name_servers(file_path):
    try:
        with gzip.open(file_path, 'rt') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return
    except IOError:
        print(f"Error: An error occurred while reading the file {file_path}.")
        return

    name_servers = set()

    for line in lines:
        fields = process_line(line)
        if len(fields) < 3:
            continue  # Skip invalid lines
        current_name_server = fields[4].lower()
        name_servers.add(current_name_server)

    print("\nName Servers encountered in the file:\n")
    for ns in sorted(name_servers):
        print(ns)

def compare_zone_files(file1_path, file2_path):
    try:
        with gzip.open(file1_path, 'rt') as file1, gzip.open(file2_path, 'rt') as file2:
            lines1 = set(file1.readlines())
            lines2 = set(file2.readlines())
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except IOError as e:
        print(f"Error: {e}")
        return

    added_records = lines2 - lines1
    deleted_records = lines1 - lines2

    print("\nAdded Records:\n")
    for line in sorted(added_records):
        print(line.strip())

    print("\nDeleted Records:\n")
    for line in sorted(deleted_records):
        print(line.strip())

def count_record_types(file_path):
    try:
        with gzip.open(file_path, 'rt') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return
    except IOError:
        print(f"Error: An error occurred while reading the file {file_path}.")
        return

    record_counter = Counter()

    for line in lines:
        fields = process_line(line)
        if len(fields) < 3:
            continue  # Skip invalid lines
        record_type = fields[4].lower()
        record_counter[record_type] += 1

    print("\nCount of DNS Record Types:\n")
    for record_type, count in sorted(record_counter.items()):
        print(f"{record_type.upper()}: {count}")

def list_record_types(file_path):
    try:
        with gzip.open(file_path, 'rt') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return
    except IOError:
        print(f"Error: An error occurred while reading the file {file_path}.")
        return

    record_types = set()

    for line in lines:
        fields = process_line(line)
        if len(fields) < 3:
            continue  # Skip invalid lines
        record_type = fields[4].lower()
        record_types.add(record_type)

    print("\nRecord Types in the File:\n")
    for record_type in sorted(record_types):
        print(record_type)

def main():
    parser = argparse.ArgumentParser(description="Process DNS records from a gzipped TLD Zone Transfer file.")
    parser.add_argument("file", nargs='?', help="Path to the gzipped file.")
    parser.add_argument("-r", "--record-type", help="Type of DNS record to filter (e.g., 'a', 'aaaa').", choices=VALID_RECORD_TYPES)
    parser.add_argument("-n", "--name-server", help="Name server to filter.")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of threads to use (default is 4).")
    parser.add_argument("-l", "--list-name-servers", action="store_true", help="List all name servers encountered in the file.")
    parser.add_argument("-c", "--compare", nargs=2, metavar=('file1', 'file2'), help="Compare two gzipped zone files.")
    parser.add_argument("-e", "--enumerate-counts", action="store_true", help="Enumerate counts of each DNS record type in the file.")
    parser.add_argument("--list-record-types", action="store_true", help="List the DNS record types present in the file.")

    args = parser.parse_args()

    if args.compare:
        compare_zone_files(args.compare[0], args.compare[1])
    elif args.list_name_servers:
        if args.file:
            list_name_servers(args.file)
        else:
            print("Error: You must specify a file with --list-name-servers.")
            parser.print_help()
    elif args.enumerate_counts:
        if args.file:
            count_record_types(args.file)
        else:
            print("Error: You must specify a file with --enumerate-counts.")
            parser.print_help()
    elif args.list_record_types:
        if args.file:
            list_record_types(args.file)
        else:
            print("Error: You must specify a file with --list-record-types.")
            parser.print_help()
    elif args.record_type and args.name_server:
        if args.file:
            filter_records(args.file, args.record_type, args.name_server, args.threads)
        else:
            print("Error: You must specify a file with --record-type and --name-server.")
            parser.print_help()
    else:
        print("Error: You must specify an operation.")
        parser.print_help()

if __name__ == "__main__":
    main()
