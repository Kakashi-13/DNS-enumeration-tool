import dns.resolver
import dns.query
import dns.zone
import dns.reversename
import socket

# Function to query DNS records
def query_dns(domain, record_type):
    print(f"Attempting to query {record_type} records for {domain}...")
    try:
        resolver = dns.resolver.Resolver()
        answers = resolver.resolve(domain, record_type)
        print(f"\n{record_type} records for {domain}:")
        if not answers:
            print(f"No {record_type} records found for {domain}.")
        for rdata in answers:
            print(f"- {rdata.to_text()}")
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        print(f"No {record_type} record found for {domain}.")
    except Exception as e:
        print(f"Error querying {record_type} record: {e}")

# Function to get reverse DNS lookup
def reverse_dns_lookup(ip):
    print(f"Attempting reverse DNS lookup for IP address {ip}...")
    try:
        result = dns.reversename.from_address(ip)
        reverse = dns.resolver.resolve(result, "PTR")
        print(f"\nReverse DNS record for {ip}:")
        for rdata in reverse:
            print(f"- {rdata.to_text()}")
    except Exception as e:
        print(f"Error performing reverse DNS lookup: {e}")

# Function to query common DNS records
def dns_enumeration(domain):
    print(f"\nStarting DNS enumeration for {domain}...")
    query_dns(domain, "A")  # A record (IP address)
    query_dns(domain, "MX")  # MX record (Mail exchange)
    query_dns(domain, "NS")  # NS record (Name server)
    query_dns(domain, "TXT")  # TXT record (Text data, often used for SPF, etc.)
    query_dns(domain, "SOA")  # SOA record (Start of authority)
    print("\nDNS enumeration completed.\n")

# Function to get nameservers for a domain
def get_nameservers(domain):
    print(f"Fetching nameservers for {domain}...")
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        nameservers = [ns.to_text() for ns in ns_records]
        if nameservers:
            print(f"\nNameservers for {domain}:")
            for ns in nameservers:
                print(f"- {ns}")
        else:
            print(f"No nameservers found for {domain}.")
        return nameservers
    except Exception as e:
        print(f"Error fetching NS records: {e}")
        return []

# Function to perform zone transfer if possible (for enumeration)
def zone_transfer(domain, nameserver):
    print(f"\nAttempting zone transfer for {domain} at nameserver {nameserver}...")
    try:
        zone = dns.zone.from_xfr(dns.query.xfr(nameserver, domain))
        print(f"Zone transfer successful for {domain} at nameserver {nameserver}:")
        for name, ttl, rdata in zone.nodes.items():
            print(f"- {name.to_text()}: {rdata.to_text()}")
    except dns.exception.DNSException as e:
        print(f"Error performing zone transfer with {nameserver}: {e}")
    except Exception as e:
        print(f"Unexpected error during zone transfer: {e}")

# Main function
def main():
    domain = input("Enter domain to enumerate: ")
    
    # Starting DNS enumeration
    dns_enumeration(domain)
    
    # Get authoritative nameservers for zone transfer
    nameservers = get_nameservers(domain)
    
    if nameservers:
        # Attempt zone transfer with the retrieved nameservers
        for ns in nameservers:
            zone_transfer(domain, ns)
    else:
        print(f"Could not find any nameservers for {domain} to attempt zone transfer.")
    
    # Reverse DNS lookup (for IP address input)
    try:
        ip = socket.gethostbyname(domain)
        reverse_dns_lookup(ip)
    except socket.gaierror:
        print("Invalid domain name, unable to resolve IP address.")

# Running the script
if __name__ == "__main__":
    main()
