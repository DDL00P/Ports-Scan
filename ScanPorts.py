import socket
import threading
import argparse
from tqdm import tqdm  # For progress indicator
import sys
import time

# List to store open ports
open_ports = []

# Function to check if a port is open
def scan_port(ip, port, silent=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set a timeout
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)  # Add open port to the list
            if not silent:
                # Only print when the scan is done, not after each port check
                pass
        sock.close()
    except socket.error:
        if not silent:
            pass  # Do not print anything when a port is closed in silent mode

# Function to scan ports in the specified range
def scan_ports(ip, start_port, end_port, silent=False, threads=1000, verbose=False, open_only=False, output_file=None):
    print(f"Starting scan on {ip} from port {start_port} to port {end_port}")
    
    # Create threads for scanning
    def thread_scan_port(port):
        if verbose:
            print(f"Scanning port {port}...")
        scan_port(ip, port, silent)
    
    threads_list = []
    total_ports = end_port - start_port + 1
    progress_bar = tqdm(total=total_ports, desc="Scanning ports", unit="port", ncols=100, bar_format="{l_bar}{bar}| {percentage:3.0f}%")  # Progress indicator

    try:
        # Scanning ports in chunks of 2000
        for port_chunk_start in range(start_port, end_port + 1, 2000):
            port_chunk_end = min(port_chunk_start + 1999, end_port)  # Make sure we don't go over the end port
            for port in range(port_chunk_start, port_chunk_end + 1):
                # Create a thread for each port
                thread = threading.Thread(target=thread_scan_port, args=(port,))
                threads_list.append(thread)
            
            # Control the number of simultaneous threads
            if len(threads_list) >= threads:
                for t in threads_list:
                    t.start()
                for t in threads_list:
                    t.join()
                threads_list = []
                progress_bar.update(len(range(port_chunk_start, port_chunk_end + 1)))  # Update the progress indicator after processing each chunk

        # Start the remaining threads for the last block
        for t in threads_list:
            t.start()
        for t in threads_list:
            t.join()

        progress_bar.update(len(threads_list))  # Update the progress indicator for the last block
        progress_bar.close()  # Close the progress indicator

        # Display only open ports if the --open option is activated
        if open_only:
            print("\nOpen ports found:")
            if open_ports:
                for port in open_ports:
                    print(f"Port {port} is open.")
            else:
                print("No open ports found.")
        else:
            print("Scan completed.")

        # Save the results to a file if the -f option is specified
        if output_file:
            with open(output_file, "w") as file:
                if open_ports:
                    file.write("Open ports found:\n")
                    for port in open_ports:
                        file.write(f"Port {port} is open.\n")
                else:
                    file.write("No open ports found.\n")
            print(f"Results saved to {output_file}")

    except KeyboardInterrupt:
        # Handle Ctrl+C interruption
        print("\nScan canceled successfully.")
        progress_bar.close()

# Main function to parse arguments
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

    # Start port scanning
    scan_ports(args.ip, args.start, args.end, silent=args.silent, threads=args.threads, verbose=args.verbose, open_only=args.open, output_file=args.file)

if __name__ == "__main__":
    main()
