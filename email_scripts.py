## Script that will send an email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import defaultdict 

# Email configuration
smtp_from = 'Reports' + "<email you want it to send from>"
#email_to = ["test email"]  # List of recipients
email_to = ["email1", "email2", "email3"]
smtp_subject = "Report"
smtp_server = "smtp hostname"

def send_link_email(link, subject="Subject", body="Message:"): 
    """Sends an email with the provided link."""

    msg = MIMEMultipart()
    msg["From"] = smtp_from
    msg["To"] = ", ".join(email_to)  # Join email addresses with commas
    msg["Subject"] = subject

    html_body = f"""
    <html>
    <head></head>
    <body>
        <p>{body}<br>
            <a href="{link}">{link}</a>
        </p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_body, "html"))  # Use HTML for the link

    try:
        with smtplib.SMTP(smtp_server) as server:
            server.sendmail(smtp_from, email_to, msg.as_string())
            print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    link_to_send = input("Enter the link you want to email: ")
    send_link_email(link_to_send)  
