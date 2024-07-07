import socket
import dns.resolver
import requests
import whois

def get_ip_address(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None

def get_dns_records(domain):
    try:
        result = {}
        for qtype in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']:
            answer = dns.resolver.resolve(domain, qtype, raise_on_no_answer=False)
            result[qtype] = [str(rdata) for rdata in answer]
        return result
    except Exception as e:
        return None

def get_http_server_details(domain):
    try:
        response = requests.head(f"http://{domain}", timeout=5)
        return response.headers
    except requests.RequestException:
        return None

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return w
    except Exception:
        return None

def gather_domain_info(domain):
    info = {}
    
    # Get IP address
    info['IP Address'] = get_ip_address(domain)
    
    # Get DNS records
    info['DNS Records'] = get_dns_records(domain)
    
    # Get HTTP server details
    info['HTTP Server Details'] = get_http_server_details(domain)
    
    # Get WHOIS information
    info['WHOIS Information'] = get_whois_info(domain)
    
    return info

if _name_ == "_main_":
    domain = input("Enter domain: ")
    info = gather_domain_info(domain)
    for key, value in info.items():
        print(f"{key}:\n{value}\n")