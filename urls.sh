#!/bin/bash

# Check if an organization name is provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <organization_name>"
    exit 1
fi

org_name="$1"
results_dir="results/$org_name"

python3 crawler.py "$results_dir/lives" > "$results_dir/crawled.txt" 

cat "$results_dir/crawled.txt" | grep "\.js" > "$results_dir/js.txt" 

cat "$results_dir/crawled.txt" | grep -v "\.js" >> "$results_dir/turls.txt" 

python3 webdirectory.py "$results_dir/lives" common.txt >> "$results_dir/turls.txt"

cat "$results_dir/turls.txt" | sort | uniq > "$results_dir/urls.txt"
 
