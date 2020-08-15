# send a mail from one account to another/multiple account
import os
import logging
import smtplib
from commons import secure
from commons import common

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
gmail_server = "smtp.gmail.com"
port = 25
server = None
_, project_name = common.get_project_dir_name()


def encode_secrets():
    secure.secure_secrets(project_name)


def login_to_server():
    keys = secure.read_secrets(project_name)
    username = keys['username']
    password = keys['password']
    server = smtplib.SMTP(gmail_server, port)
    server.ehlo()
    server.login(user=username, password=password)


if __name__ == "__main__":
    encode_secrets()
    login_to_server()

