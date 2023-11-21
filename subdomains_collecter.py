import time
import sys
import os
import argparse
import threading
from multiprocessing import Pool
import argparse
from apis.apis import alienvault,anubis,hackertarget,crt,urlscan
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"



if len(sys.argv) < 2:
    print("Usage: python script_name.py domains")
    sys.exit(1)

domains = sys.argv[1]

ListSubdomains = []

def addDomainsthreaded(defname):
    try:
        th = defname(domains,user_agent)
        for i in th:
            if not ListSubdomains.__contains__(i):
                ListSubdomains.append(i)
                if domains in i:
                    if "," in i:
                        s = i.split(",")[0]
                        print(s)
                    else:
                        print(i)
                else:
                    pass
            else:
                pass
    except:
        pass


def run():
    threading.Thread(addDomainsthreaded(alienvault,)).start()
    threading.Thread(addDomainsthreaded(anubis)).start()
    threading.Thread(addDomainsthreaded(hackertarget)).start()
    threading.Thread(addDomainsthreaded(crt)).start()
    threading.Thread(addDomainsthreaded(urlscan)).start()

def Start():
    threading.Thread(run()).start()
    N = 0
    for i in ListSubdomains:
        if domains in i:
            N+=1
        else:
            pass
    print(f"Subdomains Found {N}")
Start()
    

