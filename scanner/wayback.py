import requests
from urllib.parse import urlparse

def get_wayback_urls(domain):
    parsed = urlparse(domain)
    root_domain = parsed.netloc or parsed.path
    api = f"https://web.archive.org/cdx/search/cdx?url={root_domain}/*&output=text&fl=original&collapse=urlkey"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(api, headers=headers, timeout=10)
        if res.status_code == 200:
            urls = res.text.splitlines()
            filtered = [
                url for url in urls
                if not any(url.endswith(ext) for ext in [
                    ".jpg", ".jpeg", ".png", ".gif", ".svg", ".css", ".js", ".woff", ".ttf", ".ico", ".pdf"
                ])
            ]
            return list(set(filtered))
    except Exception as e:
        print(f"[Wayback Error] {e}")
    return []

def fetch_wayback_urls(domain):
    return get_wayback_urls(domain)
