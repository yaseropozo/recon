import tldextract
import sys
import requests
import time
import re

def extract_apex_domain(subdomain):
    ext = tldextract.TLDExtract()
    extracted = ext(subdomain)
    return f"{extracted.domain}.{extracted.suffix}"

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

    counter = 0 
    start_time = time.time()
    common_names = set()  # Use a set to store unique apex domains

    if response.status_code == 200:
        data = response.json()
        for item in data:
            common_name = item['common_name']
            counter += 1
            if ' ' not in common_name:
                if common_name.startswith("*."):
                    common_name = common_name[2:]
                apex_domain = extract_apex_domain(common_name)
                common_names.add(apex_domain)
        
    else:
        print("Failed to retrieve data. HTTP status code:", response.status_code)

    print("counter is :      "+str(counter))
    
    # Extract and print unique apex domains
    for apex_domain in common_names:
        print(f"Apex Domain: {apex_domain}")

if __name__ == "__main__":
    main()
