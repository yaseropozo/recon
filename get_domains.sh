#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 <sysarg1>"
    exit 1
fi

# Get sysarg1 from the command-line arguments

# Run get_all_tlds.py and capture the result in a variable
pwd
mkdir results/$1
pwd

max_retries=3
retries=0
sleep_time=120  # Initial sleep time is 2 minutes

while [ $retries -lt $max_retries ]; do
    result=$(python3 get_all_tlds.py)

    # Check if get_all_tlds.py was successful
    if [ $? -eq 0 ]; then
        break
    else
        echo "get_all_tlds.py failed, retrying in $sleep_time seconds..."
        sleep $sleep_time
        retries=$((retries+1))
        sleep_time=$((sleep_time+60))  # Increase sleep time by 1 minute for each retry
    fi
done

# Check if max retries reached
if [ $retries -eq $max_retries ]; then
    echo "Max retries reached. Exiting."
    exit 1
fi

# Copy files tlds-1.txt, tlds-2.txt, tlds-3.txt from /recon_data to the current working directory
cp /recon_data/tlds-{1..3}.txt .

# Run org-domains.py with sysarg1 and the copied files
if python3 tlds.py $1 | tr 'A-Z' 'a-z' | grep -vE '^\.' | grep -vE '\.$' | sort | uniq > results/$1/domains.txt; then
    echo "org-domains.py succeeded"
    exit 0
else
    echo "org-domains.py failed"
    exit 1
fi
     
