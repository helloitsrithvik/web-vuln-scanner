import requests

class OpenRedirectScanner:
    def __init__(self, url):
        self.url = url
        self.payload = "https://evil.com"

    def scan(self):
        results = []
        if "?" in self.url:
            test_url = self.url.replace("=", "=" + self.payload)
            try:
                response = requests.get(test_url, allow_redirects=False)
                if response.status_code in [301, 302] and "evil.com" in response.headers.get("Location", ""):
                    results.append(
                        f"Open Redirect vulnerability found!\n→ {test_url}"
                    )
            except Exception:
                pass
        return results

# ✅ This function allows importing and using it easily
def check_redirect(url):
    scanner = OpenRedirectScanner(url)
    return scanner.scan()
