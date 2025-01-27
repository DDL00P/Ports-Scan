import socket
import threading
import argparse
from tqdm import tqdm  


BANNER = """
 ____  ____  ____  _      ____  ____  ____  _____  ____
/ ___\/   _\/  _ \/ \  /|/  __\/  _ \/  __\/__ __\/ ___\
|    \|  /  | / \|| |\ |||  \/|| / \||  \/|  / \  |    \
\___ ||  \_ | |-||| | \|||  __/| \_/||    /  | |  \___ |
\____/\____/\_/ \|\_/  \|\_/   \____/\_/\_\  \_/  \____/
"""


open_ports = []


def scan_port(ip, port, silent=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) 
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)  
            if not silent:
                print(f"Port {port} is open.")
        sock.close()
    except socket.error:
        if not silent:
            print(f"Port {port} is closed.")


def scan_ports(ip, start_port, end_port, silent=False, threads=1000, verbose=False, open_only=False, output_file=None):
    print(BANNER)
    print(f"Starting scan on {ip} from port {start_port} to port {end_port}")
    
    
    def thread_scan_port(port):
        if verbose:
            print(f"Scanning port {port}...")
        scan_port(ip, port, silent)
    
    threads_list = []
    total_ports = end_port - start_port + 1
    progress_bar = tqdm(total=total_ports, desc="Scanning ports", unit="port")  

    for port in range(start_port, end_port + 1):
        
        thread = threading.Thread(target=thread_scan_port, args=(port,))
        threads_list.append(thread)
        
        if len(threads_list) >= threads:
            for t in threads_list:
                t.start()
            for t in threads_list:
                t.join()
            threads_list = []
            progress_bar.update(threads)  
    
    
    for t in threads_list:
        t.start()
    for t in threads_list:
        t.join()
    progress_bar.update(len(threads_list))  
    progress_bar.close()  

    
    if open_only:
        print("\nOpen ports found:")
        if open_ports:
            for port in open_ports:
                print(f"Port {port} is open.")
        else:
            print("No open ports found.")
    else:
        print("Scan completed.")

    
    if output_file:
        with open(output_file, "w") as file:
            if open_ports:
                file.write("Open ports found:\n")
                for port in open_ports:
                    file.write(f"Port {port} is open.\n")
            else:
                file.write("No open ports found.\n")
        print(f"Results saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Port scanning tool.")
    parser.add_argument("--ip", type=str, required=True, help="Target IP address.")
    parser.add_argument("--open", action="store_true", help="Show only open ports.")
    parser.add_argument("--silent", action="store_true", help="Silent scan (no output).")
    parser.add_argument("--verbose", action="store_true", help="Show detailed information during scan.")
    parser.add_argument("--threads", type=int, default=1000, choices=[1000, 2000, 3000, 4000, 5000], help="Number of threads (1000, 2000, 3000, 4000, or 5000).")
    parser.add_argument("--start", type=int, default=1, help="Start port (default 1).")
    parser.add_argument("--end", type=int, default=65535, help="End port (default 65535).")
    parser.add_argument("-f", "--file", type=str, help="Save results to a text file.")

    args = parser.parse_args()

    
    scan_ports(args.ip, args.start, args.end, silent=args.silent, threads=args.threads, verbose=args.verbose, open_only=args.open, output_file=args.file)

if __name__ == "__main__":
    main()
