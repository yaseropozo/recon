#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <org_name> <swordlist> <dns_resolver>"
    exit 1
fi

org_name="$1"
wordlist="$2"
dns_resolver="$3"
results_dir="results/$org_name"
domains_file="$results_dir/domains.txt"
temp_psubs_file="$results_dir/temp_psubs.txt"
psubs="$results_dir/psubs.txt"
emails_psubs="$results_dir/emails_psubs.txt"

# Check if the file exists
if [ ! -f "$domains_file" ]; then
    echo "Error: File '$domains_file' not found."
    exit 1
fi

# Create results directory if it doesn't exist
mkdir -p "$results_dir"

# Read each domain from the file and run the Python script
while IFS= read -r domain || [[ -n "$domain" ]]; do
    echo "Running subdomains_collector.py for domain: $domain"
    python3 subdomains_collector.py "$domain" >> "$temp_psubs_file" 2>&1
    echo "Output saved to: $temp_psubs_file"
done < "$domains_file"

# Filter out lines not containing '@' from temp_psubs.txt
grep -v '@' "$temp_psubs_file" > "$psubs"

# Filter out lines containing '@' from temp_psubs.txt
grep '@' "$temp_psubs_file" > "$emails_psubs"

# Run subdomain-bruteforcer.py and process the output
python3 subdomain-bruteforcer.py "$domains_file" "$wordlist" | tr -d "['\",]" | tr ' ' '\n' > "$results_dir/fakesubs.txt"

# Combine and sort unique subdomains
cat "$psubs" "$results_dir/fakesubs.txt" | sort | uniq > "$results_dir/allsubs.txt"

# Run massdns.py and append results to subs_ip.txt
python3 massdns.py "$results_dir/allsubs.txt" "$dns_resolver" | tee -a "$results_dir/subs_ip.txt"
  
