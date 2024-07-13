import argparse
import gzip
from dns import zone

def extract_nameservers_from_dns_file(filename, gzipped):
    nameservers = []

    # Determine file opening mode
    open_func = gzip.open if gzipped else open

    with open_func(filename, 'rt') as f:
        zone_reader = zone.ZoneReader(f)

        for name, ttl, rdtype, rdata in zone_reader.iterate_rdatas():
            if rdtype == 'NS':
                nameservers.append(rdata.to_text())

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
    for ns in nameservers:
        print(ns)

if __name__ == '__main__':
    main()
