import sys
import asyncio
import aiohttp
import aiodns


target_ports = []




async def check_subdomain(subdomain):
    url = f"http://{subdomain}"
    if await is_valid(url):
        print(f"http://{subdomain}")

    # Check HTTPS
    url = f"https://{subdomain}"
    if await is_valid(url):
        print(f"https://{subdomain}")

async def is_valid(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                #print(response.headers)
                return response.status is not None
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return False

async def main(subdomains):
    tasks = [check_subdomain(subdomain) for subdomain in subdomains]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    subdomains_file = sys.argv[1]

    with open(subdomains_file, "r") as file:
        subdomains_list = [line.strip() for line in file]

    asyncio.run(main(subdomains_list))
