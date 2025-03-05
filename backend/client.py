import requests

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    sender_email = 'abuabdul4peace@gmail.com'
    receiver_email = 'nightingale9ja@gmail.com'  # Replace with recipient's email address
    password = 'solidStreams5050'

    message = MIMEMultipart("alternative")
    message["Subject"] = "Test Email"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Hi,
    This is a test email from Python."""
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           This is a test email from <b>Python</b>.<br>
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 465)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")


send_email()

