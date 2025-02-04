# 🛡️ DNS Enumeration Tool  

A Python-based **DNS Enumeration Tool** that gathers important DNS records, attempts **zone transfers**, and performs **reverse DNS lookups**. It helps security professionals, penetration testers, and ethical hackers identify potential vulnerabilities in a domain’s DNS configuration.  

## 🚀 Features  
- ✅ Queries **A, MX, NS, TXT, and SOA** records  
- ✅ Performs **reverse DNS lookups**  
- ✅ Fetches **nameservers** for a domain  
- ✅ Attempts **zone transfers** (AXFR)  
- ✅ Structured and **verbose output** for better readability  
- ✅ Error handling for **better reliability**  

## 📌 Installation  
Ensure you have **Python 3.x** installed. Then, install the required dependencies:  

```sh
pip install dnspython
```
## 🎯 Usage 
Run the script and enter the domain name when prompted:
```sh
python dns_enum.py
```

## Example Output
```sh
Enter domain to enumerate: example.com

[*] Starting DNS Enumeration for: example.com

[+] Querying A records for example.com...
✅ A Records for example.com:
   - 93.184.216.34

[+] Querying NS records for example.com...
✅ NS Records for example.com:
   - ns1.example.com.
   - ns2.example.com.

[+] Attempting Zone Transfer for example.com at ns1.example.com...
❌ Zone Transfer Failed: Server denied request at ns1.example.com.

[+] Performing Reverse DNS Lookup for IP: 93.184.216.34...
✅ Reverse DNS Records for 93.184.216.34:
   - example.com.
```
## 🔧 How It Works
1. DNS Enumeration: Extracts different DNS records (A, MX, NS, TXT, SOA).
2. Zone Transfer Attempt: Tries to transfer DNS zone data if misconfigured.
3. Reverse Lookup: Resolves an IP to its domain name.
4. Error Handling: Catches exceptions and provides clear messages.

## ⚠️ Disclaimer
This tool is intended for educational and ethical security research only. Do not use it on domains without explicit permission.

## 🤝 Contributing
Contributions are welcome! Fork the repo, create a feature branch, and submit a pull request.
