import sys
import requests
import time
import re

sys.setrecursionlimit(10000)
if len(sys.argv) < 2:
    print("Usage: python script_name.py organization_name")
    sys.exit(1)


org = sys.argv[1]

url = "https://crt.sh/?o=" + org + "&output=json"


try:
    response = requests.get(url)
except ValueError as e:
    print(f"Error parsing JSON: {e}")

with open("json.txt", "w") as output_file:
        output_file.write(str(response.content)+ "\n")

start_time = time.time()
common_names = []
if response.status_code == 200:
    data = response.json()
    for item in data:
        common_name = item['common_name']
        if ' ' not in common_name:
            if common_name.startswith("*."):
                common_name = common_name[2:]
                common_names.append(common_name)
            else:
                common_names.append(common_name)
            
    
else:
    print("Failed to retrieve data. HTTP status code:", response.status_code)
    
    
    
common_names.sort()


common_names = list(set(common_names))
#sort | uniq > list


end_time = time.time()
elapsed_time = end_time - start_time
# Print the sorted and unique common names
with open("subdomains.txt", "w") as output_file:
    for sub in common_names:
        output_file.write(sub + "\n")

# Print the elapsed time
#print(f"Elapsed time: {elapsed_time} seconds")

tlds3 = []
with open("tlds-3.txt", "r", encoding="utf-8") as tld_file3:
    for tld in tld_file3:
        if tld:
            tlds3.append(tld)
            
tlds2 = []
with open("tlds-2.txt", "r", encoding="utf-8") as tld_file2:
    for tld in tld_file2:
        tld = tld.strip()
        if tld:
            tlds2.append(tld)
            
            
tlds1 = []
with open("tlds-1.txt", "r", encoding="utf-8") as tld_file1:
    for tld in tld_file1:
        tld = tld.strip()
        if tld:
            tlds1.append(tld)
            
matched_domains = set()



tld_pattern1 = "|".join(re.escape(tld.strip()) for tld in tlds1)
pattern1 = r'([\w+\d+\-]*)\.(' + tld_pattern1+')?$'

tld_pattern2 = "|".join(re.escape(tld.strip()) for tld in tlds2)
pattern2 = r'([\w+\d+\-]*)\.(' + tld_pattern2+')?$'
#print(pattern2)

tld_pattern3 = "|".join(re.escape(tld.strip()) for tld in tlds3)
pattern3 = r'([\w+\d+\-]*)\.(' + tld_pattern3+')?$'
#print(pattern3)


result_dict1= {} 
result_dict2= {} 
result_dict3= {} 



for subdomain in common_names:
    dom = re.search(pattern3, subdomain)
    if dom:
        matched_domains.add(dom.group(0))
        common_names.remove(subdomain)
        result_dict3[dom.group(0)] = subdomain

# print("print dict 3 ----------------------------------------------------------")
# print("=======================================================================")
# print("\n\n\n")
for key, value in result_dict3.items():
    #print(f"dom: {key}, subdomain: {value}")  
    print(key)





for subdomain in common_names:
    dom = re.search(pattern2, subdomain)
    if dom:
        matched_domains.add(dom.group(0))
        common_names.remove(subdomain)
        result_dict2[dom.group(0)] = subdomain

# print("print dict 2 ----------------------------------------------------------")
# print("=======================================================================")
# print("\n\n\n")
for key, value in result_dict2.items():
    #print(f"dom: {key}, subdomain: {value}")
    print(key)



for subdomain in common_names:
    dom = re.search(pattern1, subdomain)
    if dom:
        matched_domains.add(dom.group(0))
        common_names.remove(subdomain)
        result_dict1[dom.group(0)] = subdomain

# print("print dict 1 ----------------------------------------------------------")
# print("=======================================================================")
# print("\n\n\n")

for key, value in result_dict1.items():
    #print(f"dom: {key}, subdomain: {value}")
    print(key)


    
    
        
        
        
        

with open("extracedtest.txt", "w") as output_file:
    for sub in matched_domains:
        output_file.write(sub + "\n")




