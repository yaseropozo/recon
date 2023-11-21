import sys
import asyncio
import aiohttp
import aiodns


target_ports = []

if sys.argv[1].lower() == "range":
    try:
        start_port, end_port = map(int, sys.argv[2].split('-'))
        target_ports = range(start_port, end_port + 1)
    except ValueError:
        print("Invalid range format. Example: 1-100")
        sys.exit(1)
elif sys.argv[1].lower() == "list":
    try:
        target_ports = list(map(int, sys.argv[2].split(',')))
    except ValueError:
        print("Invalid list format. Example: 80,443,8080")
        sys.exit(1)
elif sys.argv[1].lower() == "default":
    target_ports = [80, 443]
elif sys.argv[1].lower() == "top":
    target_ports = [
        80, 443, 81, 300, 591, 593, 832, 981, 1010, 1311, 1099, 2082, 2095, 2096, 2480, 3000, 3001, 3002, 3003, 3128, 3333, 4243, 4567, 4711, 4712, 4993, 5000, 5104, 5108, 5280, 5281, 5601, 5800, 6543, 7000, 7001, 7396, 7474, 8000, 8001, 8008, 8014, 8042, 8060, 8069, 8080, 8081, 8083, 8088, 8090, 8091, 8095, 8118, 8123, 8172, 8181, 8222, 8243, 8280, 8281, 8333, 8337, 8443, 8500, 8834, 8880, 8888, 8983, 9000, 9001, 9043, 9060, 9080, 9090, 9091, 9092, 9200, 9443, 9502, 9800, 9981, 10000, 10250, 11371, 12443, 15672, 16080, 17778, 18091, 18092, 20720, 32000, 55440, 55672
    ]
else:
    print("Invalid argument. Use 'range', 'list', 'default', or 'top'.")
    sys.exit(1)

async def is_host_reachable(subdomain):
    resolver = aiodns.DNSResolver()

    try:
        result = await resolver.query(subdomain, 'A')

        # Check if the result list is empty
        if not result:
            return None

        ip_address = result[0].host
        print(f"{ip_address} : {subdomain}")

        # Check if the host has a valid IP address
        return ip_address

    except (aiodns.error.DNSError, asyncio.TimeoutError):
        return None

async def check_subdomain(subdomain):
    valid_ip = await is_host_reachable(subdomain)
    if valid_ip:
        ports = target_ports

        for port in ports:
            # Check HTTP
            url = f"http://{subdomain}:{port}"
            if await is_valid(url):
                print(f"http://{subdomain}:{port}")

            # Check HTTPS
            url = f"https://{subdomain}:{port}"
            if await is_valid(url):
                print(f"https://{subdomain}:{port}")

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
    subdomains_file = ""
    if (sys.argv[1].lower() == "default") or (sys.argv[1].lower() == "top"):
        if len(sys.argv) != 3:
            print("Usage: python script_name.py <default/top>  <subdomains_file>")
            sys.exit(1)
        subdomains_file = sys.argv[2]
    elif len(sys.argv) != 4:
        print("Usage: python script_name.py <range/list/default/top> <ports> <subdomains_file>")
        sys.exit(1)
    elif len(sys.argv) == 4:
        subdomains_file = sys.argv[3]

    with open(subdomains_file, "r") as file:
        subdomains_list = [line.strip() for line in file]

    asyncio.run(main(subdomains_list))
