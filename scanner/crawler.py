# scanner/crawler.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited = set()

    def crawl(self):
        to_visit = [self.base_url]

        while to_visit:
            url = to_visit.pop()
            if url not in self.visited:
                self.visited.add(url)
                try:
                    response = requests.get(url, timeout=5)
                    soup = BeautifulSoup(response.text, "html.parser")
                    for link in soup.find_all('a', href=True):
                        href = link.get('href')
                        full_url = urljoin(url, href)
                        parsed_base = urlparse(self.base_url).netloc
                        parsed_link = urlparse(full_url).netloc
                        if parsed_base == parsed_link:
                            to_visit.append(full_url)
                except requests.RequestException:
                    continue

        return list(self.visited)
