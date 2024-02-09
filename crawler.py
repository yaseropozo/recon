import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from robotexclusionrulesparser import RobotExclusionRulesParser

# Suppress SSL/TLS warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class WebCrawler:
    def __init__(self, start_url, max_depth=1):
        self.start_url = start_url
        self.max_depth = max_depth
        self.visited_urls_set = set()
        self.queue = deque([(start_url, 0)])
        self.robot_parser = RobotExclusionRulesParser()
        self.fetch_robot_txt(start_url)
        self.host = urlparse(start_url).netloc  # Extract host from the start URL

    def fetch_robot_txt(self, base_url):
        robots_url = urljoin(base_url, '/robots.txt')
        try:
            robots_content = requests.get(robots_url, verify=False).text
            self.robot_parser.parse(robots_content)
        except Exception as e:
            print(f"Error fetching robots.txt for {base_url}: {e}")

    def is_allowed_by_robots(self, url):
        return self.robot_parser.is_allowed('*', url)

    def is_absolute_url(self, url):
        return bool(urlparse(url).scheme)

    def get_absolute_url(self, base_url, relative_url):
        return urljoin(base_url, relative_url)

    def is_valid_url(self, url):
        return url.startswith('http') and urlparse(url).netloc == self.host

    def should_crawl(self, url, depth):
        return (
            depth <= self.max_depth
            and url not in self.visited_urls_set
            and self.is_allowed_by_robots(url)
        )

    def extract_js_links(self, soup):
        js_links = []
        # Extract JavaScript links from script tags
        script_tags = soup.find_all('script', src=True)
        for script_tag in script_tags:
            js_link = script_tag['src']
            if not self.is_absolute_url(js_link):
                js_link = self.get_absolute_url(self.current_url, js_link)
            js_links.append(js_link)

        return js_links

    def crawl(self):
        while self.queue:
            current_url, depth = self.queue.popleft()

            if current_url in self.visited_urls_set:
                continue

            try:
                response = requests.get(current_url, verify=False)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    self.current_url = current_url

                    print(f"{current_url},{response.status_code},{len(response.content)}")

                    self.visited_urls_set.add(current_url)

                    if depth < self.max_depth:
                        # Extract JavaScript links from the current HTML page
                        js_links = self.extract_js_links(soup)
                        for js_link in js_links:
                            if (
                                self.is_valid_url(js_link)
                                and self.should_crawl(js_link, depth + 1)
                            ):
                                self.queue.append((js_link, depth + 1))

                        # Extract links from anchor tags
                        links = soup.find_all('a', href=True)
                        for link in links:
                            next_url = link['href']

                            if not self.is_absolute_url(next_url):
                                next_url = self.get_absolute_url(current_url, next_url)

                            if (
                                self.is_valid_url(next_url)
                                and self.should_crawl(next_url, depth + 1)
                            ):
                                self.queue.append((next_url, depth + 1))

            except Exception as e:
                pass  # You might want to log or handle exceptions here

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    urls_file = sys.argv[1]
    with open(urls_file, 'r') as file:
        start_url = file.readline().strip()

    crawler = WebCrawler(start_url)
    crawler.crawl()
 
