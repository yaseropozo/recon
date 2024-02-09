import sys
import asyncio
import aiohttp
import aiodns

target_ports = []


async def check_subdomain(subdomain):
    url_http = f"http://{subdomain}"
    await check_and_print(url_http)

    url_https = f"https://{subdomain}"
    await check_and_print(url_https)


async def check_and_print(url):
    status_code, response_length = await is_valid(url)
    if status_code:
        print(f"{url},{status_code},{response_length}")


async def is_valid(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                status_code = response.status
                response_length = len(await response.read())
                return status_code, response_length
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return None, None


async def main(subdomains):
    tasks = [check_subdomain(subdomain) for subdomain in subdomains]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    subdomains_file = sys.argv[1]

    with open(subdomains_file, "r") as file:
        subdomains_list = [line.strip() for line in file]

    asyncio.run(main(subdomains_list))
 
