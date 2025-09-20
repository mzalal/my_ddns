"""
Dynamic DNS (DDNS) service for updating Cloudflare DNS records.

This script updates a Cloudflare DNS A record with the current public
IP address when it detects a change. It fetches the public IP from
icanhazip.com and compares it with the existing DNS record content.

Requirements:
- CLOUDFLARE_API_TOKEN: Cloudflare API token with DNS edit permissions
- CLOUDFLARE_ZONE_ID: Zone ID for the domain
- CLOUDFLARE_DNS_RECORD_ID: DNS record ID to update
- RECORD_NAME: Domain name/subdomain to update

Dependencies: requests, python-dotenv, cloudflare

Logs all operations to my_ddns.log file.
"""

import os
import sys
import logging
import requests
from dotenv import load_dotenv
from cloudflare import Cloudflare

load_dotenv()

API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")
ZONE_ID = os.environ.get("CLOUDFLARE_ZONE_ID")
DNS_RECORD_ID = os.environ.get("CLOUDFLARE_DNS_RECORD_ID")
DNS_RECORD_NAME = os.environ.get("DNS_RECORD_NAME")


logging.basicConfig(
    filename="my_ddns.log",
    encoding="utf-8",
    filemode="a",
    format="[{levelname}][{asctime}]: {message}",
    level=logging.INFO,
    style="{",
)


def exit_for_error(error):
    """Log the occurred error and exit with status code 1."""
    logging.error(error)
    print("An error has occurred, check the log file for more information.")
    sys.exit(1)


def get_public_ip():
    """Fetch the current public IP address."""
    print("Fetching current public IP address...")
    try:
        response = requests.get("https://icanhazip.com/")
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        exit_for_error(e)


def get_dns_record_content(client):
    """Retrieve the DNS record content from Cloudflare."""
    print("Retrieving DNS record content...")
    try:
        response = client.dns.records.get(
            dns_record_id=DNS_RECORD_ID,
            zone_id=ZONE_ID,
        )
        return response.content
    except Exception as e:
        exit_for_error(e)


def update_dns_record_content(client, dns_record_content):
    """Update the DNS record with new content on Cloudflare."""
    print("Updating DNS record content...")
    try:
        client.dns.records.edit(
            dns_record_id=DNS_RECORD_ID,
            zone_id=ZONE_ID,
            name=DNS_RECORD_NAME,
            type="A",
            content=dns_record_content,
        )
    except Exception as e:
        exit_for_error(e)


def main():
    """Main function to check and update DNS record if IP has changed."""
    client = Cloudflare(api_token=API_TOKEN)

    public_ip = get_public_ip()
    dns_record_content = get_dns_record_content(client)

    if public_ip != dns_record_content:
        print("Current IP and DNS record content mismatch")
        update_dns_record_content(client, public_ip)
        logging.info(
            f"DNS record content changed from {dns_record_content} to {public_ip}"
        )
        print("DONE")
    else:
        print("Current IP and DNS record content match, nothing needs to be done.")


if __name__ == "__main__":
    main()
