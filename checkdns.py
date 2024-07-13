import argparse
import gzip
import io
import dns.rdata
import dns.rdatatype

def parse_dns_line(line):
    # Example parsing logic, adjust as per your DNS record format
    parts = line.strip().split()
    if len(parts) >= 5 and parts[2] == 'IN' and parts[3] in ['NS', 'A', 'AAAA', 'CNAME']:
        return parts[4]
    return None

def extract_nameservers_from_dns_file(filename, gzipped):
    nameservers = []

    # Determine file opening mode
    open_func = gzip.open if gzipped else open

    with open_func(filename, 'rt') as f:
        for line in f:
            # Example: Parse each line to extract nameservers
            nameserver = parse_dns_line(line)
            if nameserver:
                nameservers.append(nameserver)

    return nameservers

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Extract nameservers from a DNS zone file.')
    parser.add_argument('-f', '--file', type=str, required=True, help='Input DNS zone file')
    parser.add_argument('-gz', action='store_true', help='Indicates input file is gzip compressed')
    args = parser.parse_args()

    # Extract nameservers
    nameservers = extract_nameservers_from_dns_file(args.file, args.gz)

    # Print the extracted nameservers
    print("Nameservers:")
    if nameservers:
        for ns in nameservers:
            print(ns)
    else:
        print("No nameservers found or there was an error.")

if __name__ == '__main__':
    main()
