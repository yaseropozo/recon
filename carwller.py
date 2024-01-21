import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from robotexclusionrulesparser import RobotExclusionRulesParser
import sys


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
        return url.startswith('http')  # Adjust as needed

    def should_crawl(self, url, depth):
        return (
            depth <= self.max_depth
            and url not in self.visited_urls_set
            and self.is_allowed_by_robots(url)
        )

    def crawl(self):
        with open('output.txt', 'a') as output_file:
            while self.queue:
                current_url, depth = self.queue.popleft()

                if current_url in self.visited_urls_set:
                    continue

                try:
                    response = requests.get(current_url, verify=False)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')

                        # Add your logic for processing the page content here
                        # For example, print the page title:
                        print(current_url)
                        output_file.write(current_url + '\n')

                        self.visited_urls_set.add(current_url)

                        if depth < self.max_depth:
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
                    pass

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]

    try:
        with open(file_name, 'r') as file:
            urls = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"File not found: {file_name}")
        sys.exit(1)

    for start_url in urls:
        crawler = WebCrawler(start_url)
        crawler.crawl()

if __name__ == "__main__":
    main()
