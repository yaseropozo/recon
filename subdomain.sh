#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <domains_file> <swordlist>"
    exit 1
fi

domains_file="$1"

# Check if the file exists
if [ ! -f "$domains_file" ]; then
    echo "Error: File '$domains_file' not found."
    exit 1
fi

# Read each domain from the file and run the Python script
while IFS= read -r domain || [[ -n "$domain" ]]; do
    output_file="temp_psubs_$1"
    echo "Running subdomains_collector.py for domain: $domain"
    python3 subdomains_collector.py "$domain" >> "$output_file" 2>&1
    echo "Output saved to: $output_file"
done < "$domains_file"

cat "temp_psubs_"* | grep -v @ > "psubs_$1.txt"

cat "temp_psubs_"* | grep @ > "emails_psubs_$1.txt"

python3 subdomain-bruteforcer.py "$domains_file" "$2" > "fakesubs_$1"

cat "psubs_$1.txt" "fakesubs_$1" | sort | uniq > "allsubs_$1"

python3 massdns.py "allsubs_$1" "$3" | tee -a "subs_ip_$1"
