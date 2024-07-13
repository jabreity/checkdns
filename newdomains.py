import argparse
import os
import gzip

def find_gz_files(directory):
    """
    Recursively find .gz files within a directory.
    """
    gz_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.gz'):
                gz_files.append(os.path.join(root, file))
    return gz_files

def extract_unique_fields(filename, field_num):
    """
    Extract unique field values from a gzipped file.
    """
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
    """
    Count occurrences of different record types in a gzipped file.
    """
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
    """
    Compare two gzipped files and print differences.
    """
    field_values1 = extract_unique_fields(file1, field_num)
    field_values2 = extract_unique_fields(file2, field_num)

    record_types1 = count_record_types(file1)
    record_types2 = count_record_types(file2)

    unique_in_file1 = field_values1 - field_values2
    unique_in_file2 = field_values2 - field_values1

    diff_record_types = {}
    for record_type in record_types1:
        if record_types1[record_type] != record_types2.get(record_type, 0):
            diff_record_types[record_type] = (record_types1[record_type], record_types2.get(record_type, 0))

    new_records_file2 = []
    with gzip.open(file2, 'rt') as f2:
        for line_number, line in enumerate(f2, start=1):
            if line.startswith(';') or line.strip() == '':
                continue
            fields = line.split()
            if len(fields) >= field_num and fields[field_num - 1] in unique_in_file2:
                new_records_file2.append((line_number, line.strip()))

    print(f"Unique field values in {file1} but not in {file2}:")
    for value in sorted(unique_in_file1):
        print(value)

    print(f"\nNew records added in {file2}:")
    for line_number, line_content in new_records_file2:
        print(f"Line {line_number}: {line_content}")

    print("\nDifferences in record type counts:")
    for record_type, counts in diff_record_types.items():
        print(f"{record_type}: {file1}={counts[0]}, {file2}={counts[1]}")

def process_directories(dir1, dir2, field_num):
    """
    Compare gzipped files in two directories.
    """
    files1 = find_gz_files(dir1)
    files2 = find_gz_files(dir2)

    for filename1 in files1:
        basename1 = os.path.basename(filename1)
        matching_file2 = os.path.join(dir2, basename1)
        if matching_file2 in files2:
            print(f"\nComparing files: {filename1} and {matching_file2}\n")
            compare_files(filename1, matching_file2, field_num)

def main():
    parser = argparse.ArgumentParser(description='Compare gzipped zone files or directories')
    parser.add_argument('dir1', help='Path to the first directory or gzipped file')
    parser.add_argument('dir2', help='Path to the second directory or gzipped file')
    parser.add_argument('-f', '--field', type=int, default=4, help='Field number to extract (default is 4)')
    args = parser.parse_args()

    dir1 = args.dir1
    dir2 = args.dir2
    field_num = args.field

    if os.path.isfile(dir1) and os.path.isfile(dir2):
        print(f"\nComparing files: {dir1} and {dir2}\n")
        compare_files(dir1, dir2, field_num)
    elif os.path.isdir(dir1) and os.path.isdir(dir2):
        process_directories(dir1, dir2, field_num)
    else:
        print("Error: Please provide two files or two directories.")

if __name__ == "__main__":
    main()
