import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import defaultdict
# Automox API details
api_key = 'c60bbd82-3123-4bb0-9c5d-2ed3bccb91ee'
org_id = '103787'
# List of server IDs to check
server_info = {
    '2543995': 'commandent-db',
    '3357461': 'cvsimpana',
    '2821898': 'dataedo-web',
    '3054405': 'db01prd',
    '3054344': 'db01-prd',
    '3054410': 'db01qa',
    '3054418': 'db02prd',
    '3054421': 'db02qa',
    '3061058': 'ivs-sql-center',
    '3061071': 'ivs-sql-count',
    '2520754': 'ivs-sql-xdb01',
    '2520758': 'ivs-sql-xdb02',
    '3061078': 'ivs-sql-xdbqa1',
    '3061083': 'ivs-sql-xdbqa2',
    '3061131': 'JDS0023R01',
    '3061153': 'JDS0023R02',
    '3978708': 'JDS1115R01',
    '3978714': 'JDS1115R02',
    '3057747': 'JDS1142R01',
    '3202904': 'maxxess-200',
    '2956199': 'maxxess-201',
    '2956180': 'maxxess-202',
    '2956222': 'maxxess-203',
    '2956225': 'maxxess-204',
    '3230909': 'MFP-DB',
    '3060516': 'mfp-qa-db',
    '3159895': 'mfp-stage-db',
    '3747255': 'mfp-tst-db',
    '3744754': 'MFP-TST-UI',
    '3044763': 'middb-finl-prd',
    '2458390': 'middb-finl-stg',
    '3044783': 'middb-macys-prd',
    '2458415': 'middb-macys-stg',
    '3050675': 'oriondb',
    '2810449': 'Papercut01',
    '2845443': 'proship-db',
    '2490107': 'proship-db-dev',
    '2490124': 'proship-db-test',
    '2845457': 'prsh-r-db',
    '2489976': 'prsh-r-db-dev',
    '2489999': 'prsh-r-db-test',
    '2844314': 'Pyr-Prod',
    '2490136': 'pyr-uat',
    '3050852': 'recondb',
    '2461131': 'recon-test97db',
    '4095883': 'reportsdb',
    '3027216': 'soti-dc',
    '2385062': 'soti-dc-test',
    '2837728': 'taxdb',
    '2509445': 'taxdb-test',
    '3061089': 'xofficeapp00',
    '2946792': 'xofficeappdev21',
    '2947101': 'xofficedbdev21',
    '2947107': 'xofficewebdev21',
}
# Email configuration (adapted from your setup)
smtp_from = 'Patching Alert' + "<alert@finishline.com>"
email_to = ["<jabrown@finishline.com>", "<sqladmins@finishline.com>"]
smtp_subject = "SQL Patches Available"
smtp_server = "smtp.finishline.com"
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