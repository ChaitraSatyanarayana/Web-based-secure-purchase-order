import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from email_credentials import *


def send_email(toaddr): 
    fromaddr = purchasecenter_mail
 
    msg = MIMEMultipart()
 
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "[secure]Encrypted Email" 
 
    body = "This is a secure message sent by Purchase Center"
 
    msg.attach(MIMEText(body, 'plain'))
 
    filename = "PO.txt"
    attachment = open("/home/chaitra/Desktop/209/purchase_center/PO.txt", "rb")
 
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
    msg.attach(part)
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, purchasecenter_password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
