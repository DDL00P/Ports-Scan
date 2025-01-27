# Port Scanner Script - Explanation

## Overview
This is a Python script that performs port scanning on a target IP address. It checks if the ports within a specified range are open or closed and provides options to scan ports in parallel using multiple threads for faster execution. The results can be saved to a file or displayed in the terminal.

## Key Features
1. **Multithreading:** Uses threads to scan multiple ports simultaneously, improving performance.
2. **Progress Bar:** Displays a progress bar to show the current scanning status.
3. **Port Range:** Allows scanning of ports from a start port to an end port, defaulting to the range 1-65535.
4. **Options:** Includes options for verbose output, silent scanning, and saving the results to a file.

## Arguments
- `--ip`: Specifies the target IP address to scan.
- `--start`: Defines the starting port for the scan (default: 1).
- `--end`: Defines the ending port for the scan (default: 65535).
- `--open`: Only display open ports.
- `--silent`: Perform a silent scan with no output shown.
- `--verbose`: Shows detailed information during scanning.
- `--threads`: The number of threads to use for the scan (options: 1000, 2000, 3000, 4000, 5000).
- `-f` or `--file`: Save the results to a text file.

## How It Works
1. **Scanning Ports:** The script creates a socket connection for each port in the specified range and checks if it is open. If the port is open, it is added to the list of open ports.
2. **Multithreading:** The script uses threads to perform the scan concurrently. It manages the number of threads being executed at any time to avoid overwhelming the system.
3. **Progress Bar:** The `tqdm` library is used to display a progress bar that updates as ports are scanned.
4. **Saving Results:** If the `--file` option is used, the results are saved to the specified text file.

## Example Usage
```bash
python3 port_scanner.py --ip 192.168.1.1 --start 80 --end 100 --verbose
