from flask import Flask, request, render_template, redirect, url_for
import MySQLdb
import os
from flask_wtf import Form
from werkzeug.utils import secure_filename
from wtforms import StringField
from handle_db import *
from email_credentials import *
from handle_email import *

UPLOAD_FOLDER = '/Users/narendrabidari/Desktop/cmpe 209/Project'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class TestForm(Form):
    test = StringField('Test field')

# Send Approval status mail to user
@app.route('/sendMail', methods=['POST'])
def sendMail():
    print("Send mail")
    if request.method == 'POST':
        if(request.form and request.form['status']):
            status = request.form['status']
            send_email(usr_email,status)
            print(status)
    return render_template('mailsent.html')

# Check hash(PO_user) = hash(PO_supervisor)
def authenticate(POtext1,POtext2):
     privatekey1 = get_privatekey(orderdepartment_mail)
     hash_user = rsa.sign(POtext1, privatekey1, 'MD5')
     privatekey2 = get_privatekey(orderdepartment_mail)
     hash_sup = rsa.sign(POtext2, privatekey2, 'MD5')
     if (hash_user == hash_sup):
         return True
     else:
         return False

 # Verification: verify(message, signature, pub_key)
def verifySign(plaintext,signText,str):
        mailid=get_mailid(plaintext,str)
        publicKey = get_publickey(mailid)
        if(rsa.verify(plaintext, signText, publicKey)):
            return True
        else:
            return False

# Get mail id of user or supervisor
def get_mailid(plaintext,str):
    global usr_email
    # Fecthing mail id of usr or supervisor
    if(str =='user'):
        lst1 = plaintext.split("Email:")
        lst2 = lst1[1].split("\n")
        usr_email=lst2[0]
        return (lst2[0])
    else:
        return supervisor_mail

# Decrypt ciphertext
def decrypt(encryptedText):
        # Split by SSSS, decrypt and verify
        list = encryptedText.split("SSSS")
        privateKey =get_privatekey(orderdepartment_mail)
        POtext= rsa.decrypt(list[0],privateKey)
        POtext= POtext.decode('utf8')
        index,signText = 1,""
        for index in range(index,(len(list))):
            signText += rsa.decrypt(list[index], privateKey)
        # sign1 = rsa.decrypt(list[1], privateKey)
        # sign2 = rsa.decrypt(list[2], privateKey)
        # signText = sign1 + sign2
        return POtext, signText

#  Check verification (decrypt,sign)
def verify(encryptedText1, encryptedText2):
     # Decrypt plaintext and signature of user and Supervisor
     POtext_usr, signText_usr= decrypt(encryptedText1)
     POtext_sup, signText_sup = decrypt(encryptedText2)

     #Verify Signature of user and Supervisor
     verified_usr=verifySign(POtext_usr,signText_usr,"user")
     verified_sup = verifySign(POtext_sup, signText_sup, "supervisor")
     verified_flag=(verified_usr and verified_sup)
     auth=authenticate(POtext_usr,POtext_sup)
     if(verified_flag and auth):
        return "Verified"
     else:
        return "Authentication Failed"

# Read the uploaded file from the saved directory
def read_uploaded_secure_file(filename):
    try:
        if filename:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
                return f.read()
    except IOError:
        pass
    return "Unable to read file"

# Upload and call for authentication
@app.route('/authenticate_PD', methods=['POST','GET'])
def authenticate_PD():
    print ("inside file upload'")
    if request.method == 'GET':
        return render_template('authenticate_PD.html')
    if request.method == 'POST':
        print ("inside post file upload")
        if(request.files and request.files['file1'] and request.files['file2']):
            file1 = request.files['file1']
            file2 = request.files['file2']
            # read and upload
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

            encryptedText1 = read_uploaded_secure_file(filename1)
            encryptedText2 = read_uploaded_secure_file(filename2)
            verify_status=verify(encryptedText1,encryptedText2)
            # myfile=open("PO.txt")
            # message=myfile.read()
            # verify_status=verify(message,message)
            result = ("Files " + filename1 + "\t"+" and " + filename2 + " Uploaded sucessfully")
            return render_template('result.html',result=result,status=verify_status)
        else:
            return render_template('Bad_Upload.html')

@app.route('/wrong_credentials', methods=['GET'])
def wrong_credentials():
    return render_template('wrong_credentials.html')


# email and pwd verification
@app.route('/verify/<mail>/<password>')
def verify_pw(mail, password):
    if (mail == orderdepartment_mail and password == "ord209"):
        return redirect(url_for('authenticate_PD'))
    else:
        print ("pwd wrong")
        return redirect(url_for('wrong_credentials'))

# Login Page, enter email and password
@app.route("/", methods=['POST', 'GET'])
def home():
    print ("enter")
    if request.method == 'POST':
        email = request.form['EmailID']
        pw = request.form['Password']
        print (email, " ", pw)
        return redirect(url_for('verify_pw', mail=email, password=pw))
    return render_template('login.html')

if __name__ == '__main__':
     app.run()