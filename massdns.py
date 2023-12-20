import sys
import asyncio
import aiodns
import random

if len(sys.argv) < 3:
    print("Usage: python script_name.py <subdomains_file> <dns_resolvers_file>")
    sys.exit(1)

async def is_host_reachable(subdomain, resolver):
    resolver_instance = aiodns.DNSResolver(nameservers=[resolver])

    try:
        result = await resolver_instance.query(subdomain, 'A')

        # Check if the result list is empty
        if not result:
            return None

        ip_address = result[0].host
        return ip_address

    except (aiodns.error.DNSError, asyncio.TimeoutError):
        return None

async def check_subdomain(subdomain, resolver):
    
    valid_ip = await is_host_reachable(subdomain, resolver)
    if valid_ip:
        print(f"{subdomain}:{valid_ip}")

async def main(subdomains, resolvers):
    tasks = [check_subdomain(subdomain, random.choice(resolvers)) for subdomain in subdomains]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    subdomains_file = sys.argv[1]
    resolvers_file = sys.argv[2]

    with open(subdomains_file, "r") as subdomains_file:
        subdomains_list = [line.strip() for line in subdomains_file]

    with open(resolvers_file, "r") as resolvers_file:
        resolvers_list = [line.strip() for line in resolvers_file]

    asyncio.run(main(subdomains_list, resolvers_list))
