# Scan a given ip range for webservers operation on standard and common non-statndard ports

import socket
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import sys

# Function to check if a port is open on a given IP
def check_port(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=1):
            return True
    except (socket.timeout, socket.error):
        return False

# Function to get the title of the page
def get_page_title(url):
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No title found"
            return title
    except requests.RequestException:
        return None

# Function to scan an IP address for web servers
def scan_ip(ip, output_file):
    unwanted_titles = [
        "No title found", "Welcome to nginx!", "IIS Windows Server", 
        "Apache2 Ubuntu Default", "404 Not Found", "Page not found", 
        "Apache2 Debian Default", "Success!", "Default Site", 
        "HTTP Server Test Page", "LNMP"
    ]

    for port in [80, 8080, 8000,8081,8888,9090,9091]:
        if check_port(ip, port):
            url = f"http://{ip}:{port}"
            title = get_page_title(url)
            if title and not any(unwanted_title in title for unwanted_title in unwanted_titles):
                result = f"Found Web Server: {url} -> Title: {title}"
                print(result)
                with open(output_file, 'a') as f:
                    f.write(f"{url},{title}\n")

# Function to generate IP addresses within a given range
def ip_range(ip1, ip2):
    start = list(map(int, ip1.split('.')))
    end = list(map(int, ip2.split('.')))
    temp = start

    ip_range_list = []

    ip_range_list.append(ip1)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1, 0):
            if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
        ip_range_list.append(".".join(map(str, temp)))

    return ip_range_list

# Main function to perform the scan
def main(ip1, ip2):
    output_file = "output.txt"
    ip_addresses = ip_range(ip1, ip2)
    with ThreadPoolExecutor(max_workers=10) as executor:
        for ip in ip_addresses:
            executor.submit(scan_ip, ip, output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 scan_web_servers.py <start_ip> <end_ip>")
        sys.exit(1)

    ip1 = sys.argv[1]  # Start IP from command line
    ip2 = sys.argv[2]  # End IP from command line

    main(ip1, ip2)
