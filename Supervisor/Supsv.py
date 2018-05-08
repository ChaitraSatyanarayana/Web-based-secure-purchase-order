#Author: Nischala Raja Shekar

from flask import Flask, request, render_template, redirect, url_for
import MySQLdb
import os
import rsa
import cPickle as pickle
from werkzeug import secure_filename
from articles import article
from email_credentials import *
from handle_email import *
from handle_db import *
import os
import hashlib
import sys 

UPLOAD_FOLDER = '/home/nischala/Documents/Project/Supervisor'
ALLOWED_EXTENSIONS = set(['txt','pdf','png'])

#Global variables
KEY_LENGTH = 2048
EMAIL=""
PW=""
PO_supervisor = ""
PO=""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#returns the message and signature 
def get_sign_msg():
    with open('PO.txt', 'r') as myfile:
        data=myfile.read()    #read the data from the file 
    lst = data.split("SSSS")         # split the content by the delimeter SSSS
    private = get_privatekey(supervisor_mail)      # extract private key of supervisor
    message = rsa.decrypt(lst[0],private)    
    message = message.decode('utf8')  
    sign1 = rsa.decrypt(lst[1],private)
    sign2 =  rsa.decrypt(lst[2],private)
    signature = sign1+sign2
    f1 = open ("PO_supervisor.txt","w") #write the cotents of message in new file
    f1.write(message)
    f1.close()
    return (message,signature)

def get_user_email(msg):         #extracts the user Email ID from PO
    lst1 = msg.split("Email:")
    lst2 = lst1[1].split("\n")
    return (lst2[0])

# opens PO.txt and writes the encrypted msg into it 
def open_file_write(msg):
    fh = open ("PO_supervisor.txt","w")
    fh.write(msg)
    fh.close()

# creates content for the email file attachment : encrypt(signature(hash(PO))+PO)
def get_attachment(msg,private,public):
    global KEY_LENGTH
    signature = rsa.sign(msg,private,'MD5') # hash with MD5 and sign with the private key of the user
    N = 2048/8
    # encrypt((sign(hash(PO))+PO), reciepient_public)
    crypto = rsa.encrypt(msg.encode('utf8'),public)+"SSSS"+rsa.encrypt(signature[0:N-11],public)+"SSSS"+rsa.encrypt(signature[N-11:],public)
    return crypto #crypted data for email attachment
   
#process purchase and forward via mail 
def process_po():
    global KEY_LENGTH
    private_user = get_privatekey(EMAIL)           #get the private key of the user for signature 
    public_orderdept = get_publickey(orderdepartment_mail)
    with open('PO_supervisor.txt', 'r') as myfile:	
        msg=myfile.read()    #read the data from the file
    crypto_orderdept = get_attachment(msg,private_user,public_orderdept)     #crypted data for  attachment of mail to order department
    open_file_write(crypto_orderdept)      #create file for attachment of mail to order department
    send_email(orderdepartment_mail)        # send mail to order department
    os.remove("PO_supervisor.txt")

@app.route('/approved', methods=['POST','GET'])
def approved():
    return render_template('approved.html')

@app.route('/display_po',methods=['POST','GET'])
def display_po(): 
    global PO
    if request.method == 'POST':
        if(request.form['Verify & Sign'] == 'Verify & Sign'):
            process_po()
        return render_template('approved.html')
    return render_template('display_po.html')

#display contents of purchase order
@app.route('/confirm_order',methods=['POST','GET'])
def confirm_order():
    if request.method == 'POST':
        if (request.form['Yes']=='Yes'):
            message,signature = get_sign_msg() 
            user_email = get_user_email(message)
            public = get_publickey(user_email)
            if(rsa.verify(message, signature, public)):
            # do when signature and message match
                print ("Signature verified")
            return render_template('display_po.html',message_html = message)
    return render_template('confirm_order.html')

#upload the dowloaded encrypted file
@app.route('/authenticate_po',methods=['POST','GET'])
def authenticate_po():
    print ("inside file upload'")
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #save the file in path defined in UPLOAD_FOLDER
            return redirect(url_for('confirm_order'))
    return render_template('authenticate_po.html')

#displays error messgae for wrong credentials   
@app.route('/wrong_credentials',methods=['GET'])
def wrong_credentials():
    return render_template('wrong_credentials.html')

#email and pwd verification
@app.route('/verify')
def verify_pw():
    global EMAIL,PW
    if (EMAIL == "supervisor.spcenter@gmail.com" and PW == "sup@209"):
        return redirect(url_for('authenticate_po'))
    else:
        return redirect(url_for('wrong_credentials'))    

#Login Page, enter email and password
@app.route("/",methods=['POST','GET'])
def home():
    global EMAIL,PW
    print ("enter")
    if request.method == 'POST':
        EMAIL = request.form['EmailID']
        PW = request.form['Password']
        print (EMAIL, " ", PW)
        return redirect(url_for('verify_pw'))
    return render_template('login.html')        

if __name__ == '__main__':
    app.debug == True
    app.run()
