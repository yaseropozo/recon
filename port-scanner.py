import socket
import sys

def port_scan(target_host, target_ports):
    open_ports = []
    
    for port in target_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Adjust timeout as needed
        result = sock.connect_ex((target_host, port))

        if result == 0:
            open_ports.append(port)

        sock.close()

    return open_ports

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <range/list> <ports>")
        sys.exit(1)

    target_host = "www.ibm.com"

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
    else:
        print("Invalid argument. Use 'range' or 'list'.")
        sys.exit(1)

    open_ports = port_scan(target_host, target_ports)
    print(f"Open ports on {target_host}: {open_ports}")
