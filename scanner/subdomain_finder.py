# scanner/subdomain_finder.py

import requests
import re

def find_subdomains(domain):
    """
    Uses the crt.sh public certificate transparency logs to find subdomains.
    """
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print(f"[ERROR] crt.sh responded with {response.status_code}")
            return []

        data = response.json()
        subdomains = set()

        for entry in data:
            name_value = entry.get("name_value", "")
            for sub in name_value.split("\n"):
                sub = sub.strip()
                if "*" not in sub and sub.endswith(domain):
                    subdomains.add(sub.lower())

        return sorted(subdomains)

    except Exception as e:
        print(f"[Subdomain Finder Error] {e}")
        return []
