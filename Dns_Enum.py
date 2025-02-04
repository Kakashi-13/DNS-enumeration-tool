import dns.resolver
import dns.query
import dns.zone
import dns.reversename
import socket

# Function to query DNS records
def query_dns(domain, record_type):
    print(f"\n[+] Querying {record_type} records for {domain}...")
    try:
        resolver = dns.resolver.Resolver()
        answers = resolver.resolve(domain, record_type)
        if answers:
            print(f"✅ {record_type} Records for {domain}:")
            for rdata in answers:
                print(f"   - {rdata.to_text()}")
        else:
            print(f"⚠ No {record_type} records found for {domain}.")
    except dns.resolver.NoAnswer:
        print(f"⚠ No {record_type} record found for {domain}.")
    except dns.resolver.NXDOMAIN:
        print(f"❌ Domain {domain} does not exist.")
    except Exception as e:
        print(f"❌ Error querying {record_type} record: {e}")

# Function to get reverse DNS lookup
def reverse_dns_lookup(ip):
    print(f"\n[+] Performing Reverse DNS Lookup for IP: {ip}...")
    try:
        rev_name = dns.reversename.from_address(ip)
        reverse = dns.resolver.resolve(rev_name, "PTR")
        print(f"✅ Reverse DNS Records for {ip}:")
        for rdata in reverse:
            print(f"   - {rdata.to_text()}")
    except dns.resolver.NoAnswer:
        print(f"⚠ No PTR record found for {ip}.")
    except Exception as e:
        print(f"❌ Error performing reverse DNS lookup: {e}")

# Function to query multiple DNS records
def dns_enumeration(domain):
    print(f"\n[*] Starting DNS Enumeration for: {domain}")
    record_types = ["A", "MX", "NS", "TXT", "SOA"]
    for record in record_types:
        query_dns(domain, record)
    print("\n✅ DNS Enumeration Completed.")

# Function to retrieve nameservers for a domain
def get_nameservers(domain):
    print(f"\n[+] Retrieving Nameservers for {domain}...")
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        nameservers = [ns.to_text() for ns in ns_records]
        if nameservers:
            print(f"✅ Nameservers for {domain}:")
            for ns in nameservers:
                print(f"   - {ns}")
            return nameservers
        else:
            print(f"⚠ No nameservers found for {domain}.")
            return []
    except Exception as e:
        print(f"❌ Error fetching NS records: {e}")
        return []

# Function to attempt zone transfer
def zone_transfer(domain, nameserver):
    print(f"\n[+] Attempting Zone Transfer for {domain} at {nameserver}...")
    try:
        zone = dns.zone.from_xfr(dns.query.xfr(nameserver, domain))
        print(f"✅ Zone Transfer Successful at {nameserver}:")
        for name, node in zone.nodes.items():
            print(f"   - {name.to_text()}: {node.to_text()}")
    except dns.query.TransferError:
        print(f"❌ Zone Transfer Failed: Server denied request at {nameserver}.")
    except dns.exception.DNSException as e:
        print(f"❌ DNS Error during zone transfer: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# Main function
def main():
    domain = input("\nEnter domain to enumerate: ").strip()
    
    if not domain:
        print("❌ Invalid input. Please enter a valid domain.")
        return

    # Start DNS Enumeration
    dns_enumeration(domain)
    
    # Retrieve and attempt zone transfer
    nameservers = get_nameservers(domain)
    
    if nameservers:
        for ns in nameservers:
            zone_transfer(domain, ns)
    else:
        print(f"⚠ Skipping zone transfer, no nameservers found.")

    # Perform Reverse DNS Lookup
    try:
        ip = socket.gethostbyname(domain)
        reverse_dns_lookup(ip)
    except socket.gaierror:
        print(f"⚠ Unable to resolve IP for {domain}, skipping reverse lookup.")

# Execute script
if __name__ == "__main__":
    main()
