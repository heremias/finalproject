#!/usr/bin/env python3

import os
import requests
import json
from datetime import date
import reports
import emails

def process_descriptions(directory):
    """
    Processes all .txt files in the directory, creating a dictionary for each
    and uploading it to the web service.
    """
    fruit_data = []
    total_weight = 0
    url = "http://<your-django-ip>/fruits/" # TODO: Change to your Django endpoint

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            base_name = os.path.splitext(filename)[0]
            image_name = f"{base_name}.jpeg"

            with open(filepath, 'r') as f:
                lines = f.read().strip().split('\n')
                name = lines[0]
                weight_str = lines[1]
                weight = int(weight_str.replace(" lbs", ""))
                description = " ".join(lines[2:])

                fruit_dict = {
                    "name": name,
                    "weight": weight,
                    "description": description,
                    "image_name": image_name
                }

                # Upload to web service
                response = requests.post(url, json=fruit_dict)
                response.raise_for_status()  # Raise an exception for bad status codes
                print(f"Uploaded {name}. Status: {response.status_code}")

                fruit_data.append({"name": name, "weight": weight})
                total_weight += weight

    return fruit_data, total_weight

if __name__ == "__main__":
    description_dir = "supplier-data/descriptions/"
    processed_data, total_weight_lbs = process_descriptions(description_dir)

    # Generate PDF Report
    today = date.today().strftime("%B %d, %Y")
    report_title = f"Processed Update on {today}"
    report_body = "<br/>".join([f"name: {item['name']}<br/>weight: {item['weight']} lbs" for item in processed_data])
    reports.generate_report("/tmp/processed.pdf", report_title, report_body)

    # Send Email Notification
    email_subject = f"Upload Completed - {total_weight_lbs} lbs"
    email_body = "All fruits are uploaded to our website successfully. A summary is attached to this email."
    message = emails.generate_email("automation@example.com", "supplier@example.com", email_subject, email_body, "/tmp/processed.pdf")
    emails.send_email(message)
