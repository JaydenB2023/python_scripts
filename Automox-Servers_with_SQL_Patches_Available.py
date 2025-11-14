### Pulls available SQL patches for servers from Automox
## Requires Automox Patching Platform with API access
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import defaultdict
# Automox API details
api_key = '[api key]'
org_id = '[Automox Organization ID]'
# List of server IDs to check
server_info = {
    '[server1 ID (found in automox)]': '[server1 name]',
    '[server2 ID (found in automox)]': '[server2 name]',
    '[server3 ID (found in automox)]': '[server3 name]',
    
}
# Email configuration 
smtp_from = 'Patching Alert' + "<[email sender]>"
email_to = ["<[email recipient]>"]
smtp_subject = "SQL Patches Available"
smtp_server = "[smtp server hostname]"
# Headers for the API request
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
# Function to check for SQL patches on a specific server
def check_sql_patches(server_id, server_name):
    url = f'https://console.automox.com/api/servers/{server_id}/packages?page=0&limit=5000'
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        patches = response.json()
        # Dictionary to store patches by software name
        sql_software = defaultdict(dict)
        # Group patches by software name
        for patch in patches:
            if 'SQL' in patch['display_name'].upper():
                software_name = patch['display_name']
                if patch.get('installed'):
                    sql_software[software_name]['current_version'] = patch['version']
                else:
                    sql_software[software_name]['available_version'] = patch['version']
        report = ''
        if sql_software:
            sql_report_found = False
            for software_name, versions in sql_software.items():
                if 'available_version' in versions:  # Only include if there's an update available
                    if not sql_report_found:
                        report = f"<strong style='color:black;'>SQL patches available for server {server_name}:</strong><br>"
                        sql_report_found = True
                    current_version = versions.get('current_version', 'Unknown')
                    available_version = versions['available_version']
                    report += (
                        f"<span style='color:black;'>Software: {software_name}</span><br>"
                        f"<span style='color:black;'>   - Installed Version: {current_version}</span><br>"
                        f"<span style='color:black;'>   - Available Version: {available_version}</span><br><br>"
                    )
        return report if report else None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred for server {server_name} ({server_id}): {err}")

# Function to send the email
def send_email(report):
    msg = MIMEMultipart()
    msg['From'] = smtp_from
    msg['To'] = ", ".join(email_to)
    msg['Subject'] = smtp_subject
    msg.attach(MIMEText(report, 'html'))
    try:
        server = smtplib.SMTP(smtp_server)
        server.sendmail(smtp_from, email_to, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Collect reports for each server
full_report = ''
for server_id, server_name in server_info.items():
    report = check_sql_patches(server_id, server_name)
    if report:
        full_report += report

# Send the email only if there are SQL patches available
if full_report:
    send_email(full_report)
else:
    print("No SQL patches available on any servers.")
