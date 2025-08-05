#!/usr/bin/env python3

import psutil
import socket
import emails

def check_cpu_usage():
    """Returns True if CPU usage is over 80%"""
    return psutil.cpu_percent(1) > 80

def check_disk_usage(disk="/"):
    """Returns True if available disk space is less than 20%"""
    du = psutil.disk_usage(disk)
    percent_free = 100 * du.free / du.total
    return percent_free < 20

def check_available_memory():
    """Returns True if available memory is less than 500MB"""
    available_mb = psutil.virtual_memory().available / (1024 * 1024)
    return available_mb < 500

def check_localhost():
    """Returns True if localhost cannot be resolved to 127.0.0.1"""
    try:
        localhost_ip = socket.gethostbyname('localhost')
        return localhost_ip != '127.0.0.1'
    except socket.error:
        return True

def main():
    checks = {
        check_cpu_usage: "Error - CPU usage is over 80%",
        check_disk_usage: "Error - Available disk space is less than 20%",
        check_available_memory: "Error - Available memory is less than 500MB",
        check_localhost: "Error - localhost cannot be resolved to 127.0.0.1"
    }

    for check, error_message in checks.items():
        if check():
            sender = "automation@example.com"
            # TODO: Change to your admin's email
            recipient = "admin@example.com"
            message = emails.generate_email(sender, recipient, error_message, "Please check your system and resolve the issue as soon as possible.")
            emails.send_email(message)
            break # Send only one alert at a time

if __name__ == "__main__":
    main()
