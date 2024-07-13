import argparse
import re

def extract_fourth_column_from_tld_zone(filename, column_number):
  """Extracts the specified column from a TLD zone file.

  Args:
    filename: Path to the TLD zone file.
    column_number: The index of the column to extract (1-based).

  Returns:
    A list of unique sorted values from the specified column.
  """

  unique_values = set()
  with open(filename, 'r') as zone_file:
    for line in zone_file:
      # Handle comments and empty lines
      if line.startswith(';') or not line.strip():
        continue

      # Extract columns based on column_number
      columns = line.split()
      if len(columns) >= column_number:
        unique_values.add(columns[column_number - 1])
  return sorted(unique_values)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Extract a column from a TLD zone file")
  parser.add_argument("filename", help="Path to the TLD zone file")
  parser.add_argument("-c", "--column", type=int, default=4, help="Column number to extract (default: 4)")
  args = parser.parse_args()

  unique_values = extract_fourth_column_from_tld_zone(args.filename, args.column)
  print(unique_values)
