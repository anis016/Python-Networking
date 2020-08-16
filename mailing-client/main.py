# send a mail from one account to another/multiple account
import logging
import smtplib
import ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from commons import secure, common

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

server = None
message = None

_, project_name = common.get_project_dir_name()

gmail_server = "smtp.gmail.com"
gmail_ssl_port = 465

from_mail = 'sayed.hoque016@gmail.com'
from_name = 'Sayed Hoque'
to_mail = ['anis.cuet016@gmail.com']


def encode_secrets():
    secure.secure_secrets(project_name)


def login_to_server():
    global server
    try:
        keys = secure.read_secrets(project_name)
        context = ssl.create_default_context()
        password = keys['password']
        server = smtplib.SMTP_SSL(gmail_server, gmail_ssl_port, context=context)
        server.ehlo()  # can be omitted
        server.login(user=from_mail, password=password)
        logging.info("login is success")
    except Exception as exception:
        print(exception)


def add_header_and_body():
    global message
    message = MIMEMultipart()
    message['From'] = from_name
    message['To'] = ", ".join(to_mail)
    message['Subject'] = "Just a Mail sent using Python"

    with open("message.txt", "r") as f:
        body_message = f.read()

    message.attach(MIMEText(body_message, "plain"))
    logging.info("added header and body to the mail")


def add_attachment():
    global message
    filename = "cat-3699032_1280.jpg"
    payload = MIMEBase('application', 'octet-stream')

    with open(filename, 'rb') as attachment:
        payload.set_payload(attachment.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', f'attachment; filename={filename}')
        message.attach(payload)
    logging.info("added attachment to the mail")


def send_mail():
    global server, message
    text = message.as_string()
    server.sendmail(
        from_mail,
        ', '.join(to_mail),
        text
    )
    server.close()
    logging.info("sent mail successfully")


if __name__ == "__main__":
    encode_secrets()
    login_to_server()
    add_header_and_body()
    add_attachment()
    send_mail()
