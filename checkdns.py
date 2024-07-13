import argparse
import gzip
import io
import dns.zone
import dns.exception

def extract_nameservers_from_dns_file(filename, gzipped):
    nameservers = []

    # Determine file opening mode
    open_func = gzip.open if gzipped else open

    with open_func(filename, 'rt') as f:
        # Use io.TextIOWrapper to handle gzip or regular text file
        zone_file = io.TextIOWrapper(f)

        try:
            zone = dns.zone.from_file(zone_file, filename)
            for name, node in zone.nodes.items():
                for rdataset in node.rdatasets:
                    if rdataset.rdtype == dns.rdatatype.NS:
                        for rr in rdataset:
                            nameservers.append(rr.to_text())
        except dns.exception.SyntaxError as e:
            print(f"Error parsing zone file '{filename}': {e}")

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
