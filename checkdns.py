import os
import argparse
import gzip
import json
import dns.zone
from dns.rdatatype import to_text as rdatatype_to_text


def parse_args():
    parser = argparse.ArgumentParser(description="DNS TLD Zone File Processor")
    parser.add_argument("inputs", nargs="+", help="One or more files or directories to process")
    parser.add_argument("--compare", action="store_true", help="Compare between zone files or directories")
    parser.add_argument("--gzip", action="store_true", help="Constrain input to .txt.gz extensions when provided with a directory")
    parser.add_argument("--list-ip", action="store_true", help="List all IP addresses within input")
    parser.add_argument("--list-nameservers", action="store_true", help="List all nameservers within input")
    parser.add_argument("--list-records-by-nameserver", metavar="NAMESERVER", help="List all records with a specific nameserver within input")
    parser.add_argument("--list-record-types", action="store_true", help="List all record types within input")
    parser.add_argument("--output-json", action="store_true", help="Output in JSON format")
    parser.add_argument("--output-txt", action="store_true", help="Output in TXT format")
    parser.add_argument("--output-by-type-by-ip", action="store_true", help="Output records by type by IP")
    parser.add_argument("--list-nameservers-by-type", metavar="RECORD_TYPE", help="List all nameservers with a specific record type")
    parser.add_argument("--list-record-types-by-nameserver", metavar="NAMESERVER", help="List all record types by nameserver")
    parser.add_argument("--list-records-by-ttl", metavar="TTL", help="List all records by TTL")
    parser.add_argument("--list-all-ttl-values", action="store_true", help="List all TTL values")
    parser.add_argument("--list-dnssec-public-keys", action="store_true", help="List all DNSSEC public keys")
    parser.add_argument("--validate-dnssec-public-keys", action="store_true", help="Validate all DNSSEC public keys")
    return parser.parse_args()


def is_valid_file(filename):
    return os.path.isfile(filename) and (filename.endswith('.txt') or filename.endswith('.gz'))


def is_valid_directory(dirname):
    return os.path.isdir(dirname)


def list_txt_files(directory, gzip_only=False):
    files = []
    for file in os.listdir(directory):
        if gzip_only:
            if file.endswith('.txt.gz'):
                files.append(os.path.join(directory, file))
        else:
            if file.endswith('.txt'):
                files.append(os.path.join(directory, file))
    return files


def process_zone_file(filename):
    records = []

    try:
        with open_zone_file(filename) as f:
            zone = dns.zone.from_file(f, filename)
            for name, node in zone.nodes.items():
                for rdataset in node.rdatasets:
                    for rdata in rdataset:
                        records.append({
                            'name': name.to_text(),
                            'ttl': rdataset.ttl,
                            'rdtype': rdatatype_to_text(rdataset.rdtype),
                            'data': rdata.to_text()
                        })

    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")

    return records


def open_zone_file(filename):
    if filename.endswith('.gz'):
        return gzip.open(filename, 'rt')
    else:
        return open(filename, 'r')


def main():
    args = parse_args()

    # Collect input files from directories if provided
    input_files = []
    for item in args.inputs:
        if is_valid_file(item):
            input_files.append(item)
        elif is_valid_directory(item):
            input_files.extend(list_txt_files(item, args.gzip))

    # Process each input file
    results = []
    for file in input_files:
        results.extend(process_zone_file(file))

    # Perform requested operations
    output = None

    if args.list_ip:
        ips = set()
        for record in results:
            if record['rdtype'] == 'A' or record['rdtype'] == 'AAAA':
                ips.add(record['data'])
        output = ips

    elif args.list_nameservers:
        nameservers = set()
        for record in results:
            if record['rdtype'] == 'NS':
                nameservers.add(record['data'])
        output = nameservers

    elif args.list_records_by_nameserver:
        nameserver = args.list_records_by_nameserver
        records = [record for record in results if record['rdtype'] == 'NS' and record['data'] == nameserver]
        output = records

    # Add more options as needed...

    # Output results
    if output is not None:
        if args.output_json:
            print(json.dumps(list(output), indent=4))
        elif args.output_txt:
            for item in output:
                print(item)
        else:
            print(output)


def test_script():
    # Create a temporary test directory with test files
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()
    try:
        # Create test files
        with open(os.path.join(temp_dir, 'test1.txt'), 'w') as f:
            f.write("""$ORIGIN example.com.
@   3600 IN SOA sns.dns.icann.org. noc.dns.icann.org. (
                2023070801 ; serial
                7200       ; refresh (2 hours)
                3600       ; retry (1 hour)
                1209600    ; expire (2 weeks)
                3600       ; minimum (1 hour)
                )

@   3600 IN NS a.iana-servers.net.
@   3600 IN NS b.iana-servers.net.
www 3600 IN A 192.0.2.1
""")
        
        with gzip.open(os.path.join(temp_dir, 'test2.txt.gz'), 'wt') as f:
            f.write("""$ORIGIN example.net.
@   3600 IN SOA sns.dns.icann.org. noc.dns.icann.org. (
                2023070802 ; serial
                7200       ; refresh (2 hours)
                3600       ; retry (1 hour)
                1209600    ; expire (2 weeks)
                3600       ; minimum (1 hour)
                )

@   3600 IN NS a.example.net.
@   3600 IN NS b.example.net.
www 3600 IN A 192.0.2.2
""")
        
        # Run the script with test arguments
        test_args = ["--list-ip", "--output-json", temp_dir]
        args = parse_args()
        args.inputs = test_args[2:]
        main()

    finally:
        shutil.rmtree(temp_dir)

if
