def main():
    parser = argparse.ArgumentParser(description='Process a zone file and extract unique field values')
    parser.add_argument('filename', help='Path to the zone file')
    parser.add_argument('-f', '--field', type=int, default=4, help='Field number to extract (default is 4)')
    args = parser.parse_args()

    filename = args.filename
    field_num = args.field

    try:
        field_values = set()

        with open(filename, 'r') as file:
            for line in file:
                # Skip comment lines and empty lines
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

if __name__ == "__main__":
    main()
