import socket
import dns.resolver
import requests

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None

def get_dns_records(domain):
    records = {}
    for record_type in ['A', 'AAAA', 'MX', 'NS', 'CNAME', 'TXT']:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [str(rdata) for rdata in answers]
        except dns.resolver.NoAnswer:
            records[record_type] = []
        except dns.resolver.NXDOMAIN:
            records['error'] = 'Domain does not exist'
            break
        except Exception as e:
            records['error'] = str(e)
            break
    return records

def get_server_details(domain):
    try:
        response = requests.get(f'http://{domain}', timeout=5)
        server_info = response.headers.get('Server')
        return server_info
    except requests.exceptions.RequestException:
        return None

def gather_domain_info(domain):
    info = {}
    info['IP Address'] = get_ip(domain)
    info['DNS Records'] = get_dns_records(domain)
    info['Server Details'] = get_server_details(domain)
    return info

def display_info(info):
    print("Domain Information Gathering Tool\n")
    print("IP Address:", info['IP Address'])
    print("\nDNS Records:")
    for record_type, records in info['DNS Records'].items():
        print(f"  {record_type}:")
        if isinstance(records, list):
            for record in records:
                print(f"    {record}")
        else:
            print(f"    {records}")
    print("\nServer Details:", info['Server Details'])

if __name__ == "__main__":
    domain = input("Enter the domain: ")
    info = gather_domain_info(domain)
    display_info(info)
