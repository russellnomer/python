import subprocess
import os
import hashlib

def run_command(command):
    """Runs a shell command and returns the output."""
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        return stdout, stderr, process.returncode
    except Exception as e:
        return None, str(e), 1

def check_disk_health(output_file):
    """Checks disk health and writes results to the output file."""
    output_file.write("\n--- Disk Health Checks ---\n")

    disks_stdout, disks_stderr, disks_returncode = run_command("diskutil list | grep 'disk[0-9]'")
    if disks_returncode == 0:
        disks = [line.split()[0] for line in disks_stdout.splitlines()]
        for disk in disks:
            verify_stdout, verify_stderr, verify_returncode = run_command(f"diskutil verifyDisk {disk}")
            output_file.write(f"\n{disk} verification:\n{verify_stdout}\n")
            if verify_stderr:
                output_file.write(f"Errors: {verify_stderr}\n")

            smart_info_stdout, smart_info_stderr, smart_info_returncode = run_command(f"smartctl --info {disk}")
            if smart_info_returncode == 0:
                smart_health_stdout, smart_health_stderr, smart_health_returncode = run_command(f"smartctl --health {disk}")
                if smart_health_returncode == 0:
                    output_file.write(f"\n{disk} SMART Health:\n{smart_health_stdout}\n")
                else:
                    output_file.write(f"SMART Health check failed for {disk} : {smart_health_stderr}\n")
            else:
                output_file.write(f"SMART Info check failed for {disk} : {smart_info_stderr}\n")

    else:
        output_file.write(f"Disk listing failed: {disks_stderr}\n")

def check_file_integrity(output_file):
    """Checks file integrity for potentially suspicious files."""
    output_file.write("\n--- Potential Suspicious Files ---\n")
    suspicious_extensions = [".sh", ".py", ".bin", ".dylib", ".so"] # add more as needed
    suspicious_permissions = "u+s,g+s"
    suspicious_size = "+100M"

    for ext in suspicious_extensions:
        find_stdout, find_stderr, find_returncode = run_command(f"find / -type f -name '*{ext}'")
        if find_returncode == 0 and find_stdout:
            output_file.write(f"\nFiles with extension {ext}:\n{find_stdout}\n")

    find_perm_stdout, find_perm_stderr, find_perm_returncode = run_command(f"find / -type f -perm /{suspicious_permissions}")
    if find_perm_returncode == 0 and find_perm_stdout:
        output_file.write(f"\nFiles with suspicious permissions:\n{find_perm_stdout}\n")

    find_size_stdout, find_size_stderr, find_size_returncode = run_command(f"find / -type f -size {suspicious_size}")
    if find_size_returncode == 0 and find_size_stdout:
        output_file.write(f"\nLarge files (>{suspicious_size}):\n{find_size_stdout}\n")

def check_network_connections(output_file):
    """Checks network connections and writes results to the output file."""
    output_file.write("\n--- Network Connections ---\n")

    netstat_stdout, netstat_stderr, netstat_returncode = run_command("netstat -an")
    if netstat_returncode == 0:
        output_file.write(f"netstat -an:\n{netstat_stdout}\n")
    else:
        output_file.write(f"netstat failed: {netstat_stderr}\n")

    lsof_stdout, lsof_stderr, lsof_returncode = run_command("lsof -i")
    if lsof_returncode == 0:
        output_file.write(f"lsof -i:\n{lsof_stdout}\n")
    else:
        output_file.write(f"lsof failed: {lsof_stderr}\n")

def main():
    """Main function to orchestrate the checks."""

    output_filename = "system_analysis_report.txt"
    with open(output_filename, "w") as output_file:
        output_file.write("--- System Analysis Report ---\n")
        check_disk_health(output_file)
        check_file_integrity(output_file)
        check_network_connections(output_file)
    print(f"System analysis report written to {output_filename}")

if __name__ == "__main__":
    main()