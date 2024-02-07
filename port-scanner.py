import socket
import sys


def port_scan(subdomain, target_port):


        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Adjust timeout as needed

        target_host = subdomain  # Change 'yourdomain.com' to your actual domain

        result = sock.connect_ex((target_host, port))

        if result == 0:
            sock.close()
            return target_port,socket.getservbyport(target_port)

    
def print_usage_and_exit():
    print("Usage: python script_name.py <subdomains_file> <default/top/range/list> [ports]")
    sys.exit(1)

def parse_ports_argument(argument):
    try:
        return list(map(int, argument.split(',')))
    except ValueError:
        print("Invalid ports format. Example: 80,443,8080")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage_and_exit()

    subdomains_file = sys.argv[1]
    option = sys.argv[2].lower()

    if option in {"default", "top"}:
        if len(sys.argv) != 3:
            print_usage_and_exit()

        target_ports = [80, 443] if option == "default" else [
            80, 443, 81, 300, 591, 593, 832, 981, 1010, 1311, 1099, 2082, 2095, 2096, 2480, 3000, 3001, 3002, 3003, 3128, 3333, 4243, 4567, 4711, 4712, 4993, 5000, 5104, 5108, 5280, 5281, 5601, 5800, 6543, 7000, 7001, 7396, 7474, 8000, 8001, 8008, 8014, 8042, 8060, 8069, 8080, 8081, 8083, 8088, 8090, 8091, 8095, 8118, 8123, 8172, 8181, 8222, 8243, 8280, 8281, 8333, 8337, 8443, 8500, 8834, 8880, 8888, 8983, 9000, 9001, 9043, 9060, 9080, 9090, 9091, 9092, 9200, 9443, 9502, 9800, 9981, 10000, 10250, 11371, 12443, 15672, 16080, 17778, 18091, 18092, 20720, 32000, 55440, 55672
        ]
    elif option == "range":
        if len(sys.argv) != 4:
            print_usage_and_exit()

        try:
            start_port, end_port = map(int, sys.argv[3].split('-'))
            target_ports = range(start_port, end_port + 1)
        except ValueError:
            print("Invalid range format. Example: 1-100")
            sys.exit(1)
    elif option == "list":
        if len(sys.argv) != 4:
            print_usage_and_exit()

        target_ports = parse_ports_argument(sys.argv[3])
    else:
        print_usage_and_exit()

    try:
        with open(subdomains_file, "r") as file:
            subdomains_list = [line.strip() for line in file]

        target_ports = [80, 443]  # Default ports; you can customize this list
        for port in target_ports: 
            for line in subdomains_list:
                subdomain, ip_address = line.split(":")
                try:
                    port,protocol = port_scan(ip_address, port)
                    print(f"{subdomain}:{port}:{protocol}")
                except TypeError:
                    pass

    except FileNotFoundError:
        print(f"Error: File '{subdomains_file}' not found.")
        sys.exit(1)

