import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config


class EmailSender:
    def __init__(self):
        self.config = Config()

    def send_email(self, new_items):
        """
        Send an email with the list of new items.
        """
        sender_email, sender_pass, recipient_email = self.config.get_email_config()

        subject = "New Items Found on Yaga"
        body = "New items have been found:\n\n"
        for item in new_items:
            body += f"Link: {item['link']}, Price: {item['price']} €"
            if item['brand']:
                body += f", Brand: {item['brand']}\n"
            else:
                body += "\n"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_pass)
                server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email. Error: {e}")
