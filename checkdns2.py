import argparse
import gzip

def extract_unique_fields(filename, field_num):
    field_values = set()

    try:
        with gzip.open(filename, 'rt') as file:
            for line in file:
                if line.startswith(';') or line.strip() == '':
                    continue
                
                fields = line.split()
                if len(fields) >= field_num:
                    field_values.add(fields[field_num - 1])

        # Print the unique sorted values
        for value in sorted(field_values):
            print(value)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

def count_record_types(filename):
    record_types = {
        'a': 0,
        'aaaa': 0,
        'dnskey': 0,
        'ds': 0,
        'ns': 0,
        'nsec3': 0,
        'nsec3param': 0,
        'rrsig': 0,
        'soa': 0
    }

    try:
        with gzip.open(filename, 'rt') as file:
            for line in file:
                if line.startswith(';') or line.strip() == '':
                    continue
                
                fields = line.split()
                if len(fields) >= 4 and fields[3] in record_types:
                    record_types[fields[3]] += 1

        # Print the count of each record type
        for record_type, count in record_types.items():
            print(f"{record_type}: {count}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

def main():
    parser = argparse.ArgumentParser(description='Process a gzipped zone file')
    parser.add_argument('filename', help='Path to the gzipped zone file')
    parser.add_argument('-f', '--field', type=int, help='Field number to extract (default is 4)')
    parser.add_argument('--count', action='store_true', help='Count occurrences of DNS record types')
    args = parser.parse_args()

    filename = args.filename
    field_num = args.field if args.field else 4

    if args.count:
        count_record_types(filename)
    else:
        extract_unique_fields(filename, field_num)

if __name__ == "__main__":
    main()
