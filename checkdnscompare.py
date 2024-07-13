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

        return field_values

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return set()

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

        return record_types

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}

def compare_files(file1, file2, field_num):
    # Extract unique field values and record type counts for both files
    field_values1 = extract_unique_fields(file1, field_num)
    field_values2 = extract_unique_fields(file2, field_num)

    record_types1 = count_record_types(file1)
    record_types2 = count_record_types(file2)

    # Identify differences
    unique_in_file1 = field_values1 - field_values2
    unique_in_file2 = field_values2 - field_values1

    diff_record_types = {}
    for record_type in record_types1:
        if record_types1[record_type] != record_types2.get(record_type, 0):
            diff_record_types[record_type] = (record_types1[record_type], record_types2.get(record_type, 0))

    # Print results
    print(f"Unique field values in {file1} but not in {file2}:")
    for value in sorted(unique_in_file1):
        print(value)

    print(f"\nUnique field values in {file2} but not in {file1}:")
    for value in sorted(unique_in_file2):
        print(value)

    print("\nDifferences in record type counts:")
    for record_type, counts in diff_record_types.items():
        print(f"{record_type}: {file1}={counts[0]}, {file2}={counts[1]}")

def main():
    parser = argparse.ArgumentParser(description='Compare gzipped zone files')
    parser.add_argument('file1', help='Path to the first gzipped zone file')
    parser.add_argument('file2', help='Path to the second gzipped zone file')
    parser.add_argument('-f', '--field', type=int, help='Field number to extract (default is 4)')
    args = parser.parse_args()

    file1 = args.file1
    file2 = args.file2
    field_num = args.field if args.field else 4

    compare_files(file1, file2, field_num)

if __name__ == "__main__":
    main()
