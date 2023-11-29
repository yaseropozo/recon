import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_all_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        return [link['href'] for link in links]
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return []

def crawl_website(start_url, max_depth=3):
    visited_urls = set()

    def recursive_crawl(url, depth):
        if depth > max_depth or url in visited_urls:
            return

        print(f"Processing: {url}")
        visited_urls.add(url)

        links = get_all_links(url)
        for link in links:
            absolute_link = urljoin(url, link)
            if urlparse(absolute_link).scheme in ('http', 'https'):
                recursive_crawl(absolute_link, depth + 1)

    recursive_crawl(start_url, 1)

if __name__ == "__main__":
    starting_url = "https://www.artsy.net"  # Replace with the target website
    crawl_website(starting_url)
