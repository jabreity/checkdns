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

    # Find new records added in file2
    new_records_file2 = []
    with gzip.open(file2, 'rt') as f2:
        for line_number, line in enumerate(f2, start=1):
            if line.startswith(';') or line.strip() == '':
                continue
            fields = line.split()
            if len(fields) >= field_num and fields[field_num - 1] in unique_in_file2:
                new_records_file2.append((line_number, line.strip()))

    # Print results
    print(f"Unique field values in {file1} but not in {file2}:")
    for value in sorted(unique_in_file1):
        print(value)

    print(f"\nNew records added in {file2}:")
    for line_number, line_content in new_records_file2:
        print(f"Line {line_number}: {line_content}")

    print("\nDifferences in record type counts:")
    for record_type, counts in diff_record_types.items():
        print(f"{record_type}: {file1}={counts[0]}, {file2}={counts[1]}")
