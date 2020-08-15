# send a mail from one account to another/multiple account
import smtplib

gmail_server = "smtp.gmail.com"
port = 25
server = smtplib.SMTP(gmail_server, port)