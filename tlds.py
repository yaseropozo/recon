import tldextract
import sys
import requests

import re

def is_valid_subdomain(subdomain):
    # Check if the subdomain contains at least one dot
    if '.' not in subdomain:
        return False

    return True

def extract_apex_domain(subdomain):
    ext = tldextract.TLDExtract()
    extracted = ext(subdomain)
    return f"{extracted.domain}.{extracted.suffix}"

def filter_subdomains(subdomains):
    filtered_subdomains = []

    for subdomain in subdomains:
        if is_valid_subdomain(subdomain) and not re.match(r'^\d+\.\d+\.\d+\.\d+$', subdomain):
            filtered_subdomains.append(subdomain)

    return filtered_subdomains

def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py organization_name")
        sys.exit(1)

    org = sys.argv[1]

    url = "https://crt.sh/?o=" + org + "&output=json"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    with open("json.txt", "w") as output_file:
        output_file.write(str(response.content) + "\n")



    subdomains_set = set()  # Use a set to store unique subdomains

    if response.status_code == 200:
        data = response.json()
        for item in data:
            common_name = item['common_name']

            if ' ' not in common_name:
                if common_name.startswith("*."):
                    common_name = common_name[2:]
                subdomain = extract_apex_domain(common_name)
                if is_valid_subdomain(subdomain) and not re.match(r'\d+\.\d+\.\d+\.\d+', subdomain):
                    subdomains_set.add(subdomain)

    else:
        print("Failed to retrieve data. HTTP status code:", response.status_code)



    filtered_subdomains = filter_subdomains(subdomains_set)
    # Extract and print unique apex domains
    for apex_domain in filtered_subdomains:
        print(apex_domain)

if __name__ == "__main__":
    main()

