#!/usr/bin/python
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import sys

sys.path.insert(
    0, '/home/tyler/Documents/Coding/Stock-Report/Stock-Report/Functions')
my_email = 'tlrrn5@gmail.com'


def send_email():
    from read_config import export_variables
    email, password, crypto_api = export_variables(
        env_location='/home/tyler/Documents/Coding/Stock-Report/Data/.env')
    print(password)
    msg = MIMEMultipart()

    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'Stock Report'

    body = """
    <html>
        <head></head>
        <body>
            <h1>Stock/Crypto Report</h1>
            <p>This stock/crypto triggered this email.</p>
            <img src="cid:img1"
            style = "width:250px;">
        </body>
    </html>

    """
    msg.attach(MIMEText(body, "html"))

    file_image = open(
        '/home/tyler/Documents/Coding/Stock-Report/Stock-Report/Functions/Email/stock_image.png', 'rb')
    email_image = MIMEImage(file_image.read())
    file_image.close()

    email_image.add_header("Content-ID", "<image1>")
    msg.attach(email_image)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg.as_string())
    server.quit()

    return 0


if __name__ == '__main__':
    send_email()
