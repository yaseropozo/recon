import concurrent.futures
import requests
import sys

def scan_directory(url, directory):
    target_url = f"{url}/{directory}"
    response = requests.get(target_url)
    
    if response.status_code == 200:
        print(f"[+] Found: {target_url}")

def worker(args):
    url, directory = args
    scan_directory(url, directory)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <file_with_urls> <wordlist>")
        sys.exit(1)

    file_with_urls = sys.argv[1]
    wordlist_path = sys.argv[2]

    try:
        with open(file_with_urls, "r") as url_file:
            urls = [line.strip() for line in url_file]
    except FileNotFoundError:
        print(f"File not found: {file_with_urls}")
        sys.exit(1)

    with open(wordlist_path, "r") as wordlist_file:
        directories = [line.strip() for line in wordlist_file]

    # Create a list of (url, directory) tuples for each combination of URL and directory
    task_list = [(url, directory) for url in urls for directory in directories]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(worker, task_list)

if __name__ == "__main__":
    main()
