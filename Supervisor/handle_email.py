import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email_credentials import *


def send_email(toaddr): 
    fromaddr = supervisor_mail
 
    msg = MIMEMultipart()
 
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "[secure]Encrypted Email" 
 
    body = "This is a secure message sent by Supervisor"
 
    msg.attach(MIMEText(body, 'plain'))
 
    filename = "PO_supervisor.txt"
    attachment = open("/home/nischala/Documents/Project/Supervisor/PO_supervisor.txt", "rb")
 
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
    msg.attach(part)
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, supervisor_password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
