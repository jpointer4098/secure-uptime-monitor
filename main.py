import requests
from dotenv import load_dotenv
import os
import time
import ssl
import socket
from urllib.parse import urlparse

load_dotenv()

urls = os.getenv("URLS_TO_MONITOR", "").split(",")
log_file = "monitor_log.txt"

def check_ssl_expiry(url):
    try:
        hostname = urlparse(url).hostname
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expiry_date = cert['notAfter']
                return expiry_date
    except Exception:
        return None

def monitor():
    if not urls or urls == [""]:
        print("No URLs found to monitor.")
        return

    with open(log_file, "a") as log:
        for url in urls:
            url = url.strip()
            try:
                start = time.time()
                response = requests.get(url, timeout=10)
                end = time.time()
                ssl_expiry = check_ssl_expiry(url)
                log.write(f"URL: {url}\n")
                log.write(f"Status Code: {response.status_code}\n")
                log.write(f"Response Time: {round(end - start, 2)} seconds\n")
                log.write(f"SSL Expiry: {ssl_expiry}\n")
                log.write("-" * 40 + "\n")
                print(f"Checked {url}: {response.status_code} | Response Time: {round(end - start, 2)}s | SSL Expiry: {ssl_expiry}")
            except Exception as e:
                log.write(f"URL: {url}\n")
                log.write(f"Error: {str(e)}\n")
                log.write("-" * 40 + "\n")
                print(f"Error checking {url}: {str(e)}")

if __name__ == "__main__":
    monitor()
