from cgitb import reset
import re
from urllib import response
import requests
import json
from turtle import Turtle

def alienvault(Domains, useragent):
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{Domains}/passive_dns"
    headers = {"User-Agent": useragent}
    try:
        req = requests.get(url, headers=headers, timeout=15, verify=True)
        if req.status_code == 200:
            data = req.json()
            if "passive_dns" in data:
                hostnames = [entry["hostname"] for entry in data["passive_dns"]]
                return type(hostnames)
            else:
                return None
        else:
            print(f"Request failed with status code: {req.status_code}")
            return None
    except:
        return None
    
def anubis(Domains, useragent):
    url = f"https://jldc.me/anubis/subdomains/{Domains}"
    headers = {"User-Agent": useragent}
    
    try:
        response = requests.get(url, verify=True, headers=headers, timeout=15)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        data = response.json()

        return data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    

def censys(Domain, useragent):
    subdomains = []
    page = pages = 1
    try:
        while page <= pages:
            headers = {"Content-Type": "application/json", "Accept": "application/json", "User-agent": useragent}
            auth = (censys_api_id, censys_api_secret)
            data = {"query": Domain, "page": page, "fields": ["parsed.names"]}
            response = requests.post("https://www.censys.io/api/v1/search/certificates",
                                     headers=headers, json=data, auth=auth, stream=True, timeout=15)
            data = json.loads(response.text)
            pages = data["metadata"]["pages"]
            for res in data["results"]:
                pn = res["parsed.names"]
                for sub in pn:
                    sub = sub.replace("http://", "")
                    sub = sub.replace("https://", "")
                    if "." + Domain in sub and not sub.startswith("*") and not subdomains.__contains__(sub):
                        subdomains.append(sub)
            page = page + 1
    except Exception as e:
        pass
    return subdomains



def facebook(Domains,useragent):
    subdomains =[]
    response = requests.get(
        f"https://graph.facebook.com/certificates?query={Domains}&fields=domains&limit=10000&access_token={facebook_access_token}",
        stream=True,verify=True,headers={"User-Agent":useragent})
    data = json.loads(response.text)
    for res in data["data"]:
        for sub in res["domains"]:
            if not sub.startswith('*') and not subdomains.__contains__(sub):
                subdomains.append(sub)
    return subdomains

def hackertarget(Domains,useragent):
    try:
        url = f"https://api.hackertarget.com/hostsearch/?q={Domains}"
        req = requests.get(url=url,verify=True,headers={"User-Agent":useragent},timeout=15)
        if Domains in req.text:
            resp = req.text
            s = []
            for i in resp.splitlines():
                s.append(i)
            return s
        else:
            pass
    except:
        pass
    
    
def crt(Domains, useragent):
    subdomains = []
    try:
        response = requests.get(f"https://crt.sh/?q={Domains}&output=json", stream=True, verify=True, headers={"User-Agent": useragent}, timeout=15)
        data = json.loads(response.text)
        for res in data:
            for sub in res["name_value"].split("\n"):
                if not sub.startswith('*') and sub not in subdomains:
                    subdomains.append(sub)
    except:
        pass
    return subdomains



def shodan(Domains, useragent,shodan_api_key):
    subdomains = []
    try:
        response = requests.get(f"https://api.shodan.io/dns/domain/{Domains}?key={shodan_api_key}", stream=True, headers={"User-Agent": useragent})
        response.raise_for_status()
        data = json.loads(response.text)
        
        for sub in data["subdomains"]:
            if sub + "." + Domains not in subdomains:
                subdomains.append(sub + "." + Domains)
    except:
        pass

    return subdomains


def urlscan(Domains, useragent):
    subdomains = []
    try:
        response = requests.get(f"https://urlscan.io/api/v1/search/?q=domain:{Domains}", stream=True, verify=True, headers={"User-Agent": useragent}, timeout=15)
        response.raise_for_status()
        data = json.loads(response.text)
        
        for res in data["results"]:
            if res["page"]["domain"] not in subdomains:
                subdomains.append(res["page"]["domain"])
    except:
        pass

    return subdomains
