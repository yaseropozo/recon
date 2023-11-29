import sys
import asyncio
import aiodns

if len(sys.argv) != 2:
    print("Usage: python script_name.py <subdomains_file>")
    sys.exit(1)

async def is_host_reachable(subdomain):
    resolver = aiodns.DNSResolver()

    try:
        result = await resolver.query(subdomain, 'A')

        # Check if the result list is empty
        if not result:
            return None

        ip_address = result[0].host
        return ip_address

    except (aiodns.error.DNSError, asyncio.TimeoutError):
        return None

async def check_subdomain(subdomain):
    valid_ip = await is_host_reachable(subdomain)
    if valid_ip:
        print(f"{subdomain}:{valid_ip}")

async def main(subdomains):
    tasks = [check_subdomain(subdomain) for subdomain in subdomains]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    subdomains_file = sys.argv[1]

    with open(subdomains_file, "r") as file:
        subdomains_list = [line.strip() for line in file]

    asyncio.run(main(subdomains_list))
