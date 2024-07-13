import argparse
import re

def parse_zone_file(file_path):
    """Parses a zone file line by line, yielding record data.

    Args:
        file_path: Path to the zone file.

    Yields:
        A tuple containing the line number, line content, and a boolean indicating if the line is a comment.
    """
    with open(file_path, 'r') as f:
        line_number = 0
        for line in f:
            line_number += 1
            line = line.strip()
            if not line or line.startswith(';'):
                yield line_number, line, True
            else:
                yield line_number, line, False

def extract_nameservers(file_path):
    """Extracts nameservers from a zone file.

    Args:
        file_path: Path to the zone file.

    Yields:
        Nameserver records.
    """
    for line_number, line, is_comment in parse_zone_file(file_path):
        if not is_comment and line.startswith('NS '):
            # Extract nameserver from line
            yield line

def extract_record_types(file_path):
    """Extracts record types from a zone file.

    Args:
        file_path: Path to the zone file.

    Yields:
        Unique record types.
    """
    record_types = set()
    for line_number, line, is_comment in parse_zone_file(file_path):
        if not is_comment:
            record_type = line.split()[0]
            record_types.add(record_type)
    return record_types

# ... other extraction functions for specific records, nameservers with specific record types, etc.

def main():
    parser = argparse.ArgumentParser(description='DNS zone file processor')
    parser.add_argument('input_file', help='Input zone file')
    parser.add_argument('--list-nameservers', action='store_true', help='List all nameservers')
    parser.add_argument('--list-record-types', action='store_true', help='List all record types')
    # Add other command-line options

    args = parser.parse_args()

    if args.list_nameservers:
        for nameserver in extract_nameservers(args.input_file):
            print(nameserver)
    elif args.list_record_types:
        for record_type in extract_record_types(args.input_file):
            print(record_type)
    # ... other logic for different options

if __name__ == '__main__':
    main()
