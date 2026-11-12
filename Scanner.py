# Port Scanner - by Abel Mwedihanga
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))
        s.close()
        if result == 0:
            return port
    except:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(description="Simple Python Port Scanner")
    parser.add_argument("target", help="Target IP or hostname e.g. 127.0.0.1")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=1024)
    args = parser.parse_args()

    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print("Could not resolve hostname.")
        return

    print(f"Scanning {args.target} ({target_ip}) ports {args.start}-{args.end}...")
    open_ports = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda p: scan_port(target_ip, p), range(args.start, args.end + 1))
        for port in results:
            if port:
                print(f"[+] Port {port} is OPEN")
                open_ports.append(port)

    print(f"\nDone. {len(open_ports)} open ports found: {open_ports}")

if __name__ == "__main__":
    main()