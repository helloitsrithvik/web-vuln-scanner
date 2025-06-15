from .crawler import Crawler
from .xss_scanner import check_xss
from .sql_scanner import check_sqli
from .open_redirect_scanner import check_redirect
from .wayback import get_wayback_urls

class WebScanner:
    def __init__(self, target_url, use_advanced_payloads=False, include_wayback=False):
        self.target_url = target_url
        self.use_advanced_payloads = use_advanced_payloads
        self.include_wayback = include_wayback
        self.xss_payloads = []
        self.sqli_payloads = []

    def set_payloads(self, xss_payloads, sqli_payloads):
        self.xss_payloads = xss_payloads
        self.sqli_payloads = sqli_payloads

    def run_all(self):
        results = []
        crawler = Crawler(self.target_url)
        urls = crawler.crawl()

        # 🔥 Add Wayback URLs
        if self.include_wayback:
            wayback_urls = get_wayback_urls(self.target_url)
            urls.extend(wayback_urls)

        urls = list(set(urls))  # Remove duplicates

        for url in urls:
            if "?" not in url:
                continue

            xss_vulns = check_xss(url, self.xss_payloads if self.use_advanced_payloads else None)
            if xss_vulns:
                results.append(f"🧨 XSS in {url}:\n" + "\n".join(xss_vulns))

            sqli_vulns = check_sqli(url, self.sqli_payloads if self.use_advanced_payloads else None)
            if sqli_vulns:
                results.append(f"💉 SQLi in {url}:\n" + "\n".join(sqli_vulns))

            redirect_vulns = check_redirect(url)
            if redirect_vulns:
                results.append(f"🔁 Open Redirects in {url}:\n" + "\n".join(redirect_vulns))

        return results

