#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <org_name> <swordlist> <dns resolver>"
    exit 1
fi

domains_file="results/$1/domains.txt"

# Check if the file exists
if [ ! -f "$domains_file" ]; then
    echo "Error: File '$domains_file' not found."
    exit 1
fi

# Read each domain from the file and run the Python script
while IFS= read -r domain || [[ -n "$domain" ]]; do
    output_file="temp_psubs.txt"
    echo "Running subdomains_collector.py for domain: $domain"
    python3 subdomains_collector.py "$domain" >> results/$1/"$output_file" 2>&1
    echo "Output saved to: $output_file"
done < "$domains_file"

cat results/$1/"$output_file" | grep -v @ > "psubs.txt"

cat results/$1/"$output_file" | grep @ > "emails_psubs.txt"

python3 subdomain-bruteforcer.py "$domains_file" "$2" | tr -d "['\",]" | tr ' ' '\n' > results/$1/fakesubs.txt

cat results/$1/psubs.txt results/$1/fakesubs.txt | sort | uniq > results/$1/allsubs.txt

python3 massdns.py results/$1/allsubs.txt "$3" | tee -a results/$1/subs_ip.txt
