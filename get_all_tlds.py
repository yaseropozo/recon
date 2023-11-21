import re
import requests

TLD_LIST_URL = "https://publicsuffix.org/list/public_suffix_list.dat"

pattern = r'^[a-zA-Z]'

def download_tlds():
    response = requests.get(TLD_LIST_URL)
    if response.status_code == 200:
        lines = response.text.split("\n")
        tlds = [line.strip("*.") for line in lines if line and not line.startswith("//") and re.match(pattern, line)]
        
        zero_dot_tlds = [tld for tld in tlds if tld.count(".") == 0]
        one_dot_tlds = [tld for tld in tlds if tld.count(".") == 1]
        two_dot_tlds = [tld for tld in tlds if tld.count(".") == 2]
        

        # Sort both lists
        zero_dot_tlds.sort()
        one_dot_tlds.sort()
        two_dot_tlds.sort()

        

        two_dot_tldsl = "\n".join(two_dot_tlds)
        with open("tlds-3.txt", "wb") as file:
            file.write(two_dot_tldsl.encode('utf-8'))

    
        one_dot_tldsl = "\n".join(one_dot_tlds)
        with open("tlds-2.txt", "wb") as file:
            file.write(one_dot_tldsl.encode('utf-8'))

    
        zero_dot_tldsl = "\n".join(zero_dot_tlds)
        with open("tlds-1.txt", "wb") as file:
            file.write(zero_dot_tldsl.encode('utf-8'))
        return True
    else:
        return False
        
        
        



print(download_tlds())
