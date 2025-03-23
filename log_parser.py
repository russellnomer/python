def extract_ips_from_log(log_file, target_url):
    """
    Reads a log file and prints IP addresses that accessed a specific URL.

    Args:
        log_file (str): The path to the log file.
        target_url (str): The URL to filter for.
    """
    try:
        with open(log_file, "r") as file:
            for line in file:
                if target_url in line:
                    # Assuming IP address is the first element in each line (adjust as needed)
                    parts = line.split()  # Split the line by spaces
                    if parts:  # Check if the line isn't empty
                        ip_address = parts[0]
                        print(ip_address)

    except FileNotFoundError:
        print(f"Error: {log_file} not found.")

# Example usage:
log_file_path = "access.log"  # Replace with your log file path
target_url = "/admin"  # Replace with the URL you're looking for

extract_ips_from_log(log_file_path, target_url)

# Example access.log file contents for testing.
# 192.168.1.10 - - [20/Oct/2023:10:00:00] "GET /admin HTTP/1.1" 200 1234
# 10.0.0.5 - - [20/Oct/2023:10:01:00] "GET /home HTTP/1.1" 200 5678
# 192.168.1.11 - - [20/Oct/2023:10:02:00] "GET /admin HTTP/1.1" 200 9012
# 172.16.0.1 - - [20/Oct/2023:10:03:00] "GET /admin HTTP/1.1" 404 3456
# 10.0.0.6 - - [20/Oct/2023:10:04:00] "GET /contact HTTP/1.1" 200 7890