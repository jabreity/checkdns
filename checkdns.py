import re

def extract_fourth_column_from_tld_zone(filename):
  """Extracts the fourth column from a TLD zone file.

  Args:
    filename: Path to the TLD zone file.

  Returns:
    A list of unique sorted values from the fourth column.
  """

  unique_values = set()
  with open(filename, 'r') as zone_file:
    for line in zone_file:
      # Handle comments and empty lines
      if line.startswith(';') or not line.strip():
        continue

      # Assuming fourth column is the domain name, adjust regex if needed
      match = re.match(r"^\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", line)
      if match:
        unique_values.add(match.group(4))
  return sorted(unique_values)

if __name__ == "__main__":
  filename = "/home/jason/projects/czds-api-client-python/domains/zonefiles/com.txt"
  unique_domains = extract_fourth_column_from_tld_zone(filename)
  print(unique_domains)
