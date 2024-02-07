#!/bin/bash

# Check if the correct number of command-line arguments is provided
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <org_name> <default/top/range/list> [ports]"
    exit 1
fi

# Assign command-line arguments to variables
org_name="$1"
mode="$2"
ports="$3"

# Set the results directory
results_dir="results/$org_name"

# Check if the mode is "range" or "list" and ensure the [ports] argument is provided
if [ "$mode" == "range" ] || [ "$mode" == "list" ]; then
    if [ "$#" -lt 3 ]; then
        echo "Error: Ports argument is required for mode '$mode'."
        exit 1
    fi
fi

# Run the port scanner script
python3 "port-scanner.py" "$results_dir/subs_ip.txt" "$mode" "$ports" > "$results_dir/ports.txt"

awk -F':' '{print $1":"$2}' "$results_dir/ports.txt"  > "$results_dir/portsonly" && python3 live-subdomain.py "$results_dir/portsonly"                                                                                                                    
   
