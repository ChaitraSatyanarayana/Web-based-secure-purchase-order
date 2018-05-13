import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email_credentials import *


def send_email(toaddr,status):
    fromaddr = orderdepartment_mail

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "[secure] Approval Status"

    if(status=="Verified"):
        body = "Dear User," +"\n" +"You order has been Confirmed and Approved "
    else:
        body= "Dear User"+"\n" + " Unfortunately your order has been cancelled due to Authentication failure " +"\n"+ "Please Login to Website and Purchase the items again "

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, orderdepartment_password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
