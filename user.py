from flask import Flask, request, render_template,redirect,url_for
import MySQLdb
import rsa 
import cPickle as pickle
from handle_db import *
from articles import article
from email_credentials import *
from handle_email import *
import os

#Global variables
KEY_LENGTH = 2048
EMAIL=""
PW=""
PO = ""

#article costs 
laptop =article(800)
bag = article(50)
book = article(5)
pen =article(1)

app = Flask(__name__)

def send_emails():
    send_email(supervisor_mail,msg)
    send_email(orderdepartment_mail)
    return 
# opens PO.txt and writes the encrypted msg into it 
def open_file_write(msg):
    fh = open ("PO.txt","w")
    write(msg)
    fh.close()

def process_po():
    global PO 
    private_user = get_privatekey(EMAIL)
    signature_user = rsa.sign(PO,private_user,'SHA-512')	
    msg = (str(PO) + 'SSSSS'+str(signature_user))
    public_supervisor = get_publickey(supervisor_mail)
    public_orderdept = get_publickey(orderdepartment_mail)
    encrypted_supervisor =  rsa.encrypt(msg,public_supervisor)
    open_file_write(encrypted_supervisor)
    send_email(supervisor_mail)
    return

@app.route('/confirm_order',methods=['POST','GET'])
def confirm_order(): 
    if request.method== 'POST':
       if (request.form['Confirm']=='Confirm'): 
            pid = os.fork()
            if (pid == 0):
                print ("in the child process")
                process_po()     
            return render_template('confirm_done.html')
       if (request.form['Back']=='Back'):
            return redirect(url_for('purchase_order'))

#renders wrong password information to 
@app.route('/wrong_pw',methods=['POST','GET'])
def wrong_pw():
    print ("wrong_pw")
    if request.method== 'POST':
           return
    return render_template('wrong_pw.html')


#extract purchase order 
@app.route('/purchase_order',methods=['POST','GET'])
def purchase_order():
    if request.method== 'POST': 
        global PO
        laptop.quantity=int( request.form['laptopq'])
        bag.quantity=int( request.form['bagq'])
        book.quantity=int( request.form['bookq'])
        pen.quantity=int( request.form['penq'])
        laptop.total = laptop.quantity* laptop.cost
        bag.total = bag.quantity * bag.cost
        book.total = book.quantity*book.cost
        pen.total = pen.quantity*pen.cost   
        total_amount =laptop.total+bag.total+book.total+pen.total
        PO = "Email:"+EMAIL+"\nLaptop("+str(laptop.quantity)+" no's): $"+str(laptop.total)+"\nBag("+str(bag.quantity)+" no's): $"+str(bag.total)+"\nBook("+str(book.quantity)+" no's): $"+str(book.total)+"\nPen("+str(pen.quantity)+" no's): $"+str(pen.total)+"\nTotal Amount= "+str(total_amount)
        print PO
        return render_template('confirm_order.html',laptopt=laptop.total,bagt=bag.total,bookt=book.total,pent=pen.total,amount=total_amount,laptopq=laptop.quantity,penq=pen.quantity,bagq=bag.quantity,bookq=book.quantity)
    return render_template('purchase_order.html')

# generate public and private keys and insert in credetials and public library tables
@app.route('/insert_data')
def insert_data():
   print ("insert_data")
   global EMAIL, PW
   (db,cursor)= open_db()
   (public,private)=rsa.newkeys(KEY_LENGTH)   #generate public and private keys
   public_str = pickle.dumps(public)           #convert public key object into string - pickling
   private_str = pickle.dumps(private)        #convert private key object into string - pickling
   cursor.execute("""INSERT INTO Cred VALUES (%s,%s,%s)""",(EMAIL,PW,private_str))    #insert credentials
   db.commit()
   cursor.execute("""INSERT INTO PublicKeyDir VALUES (%s,%s)""",(EMAIL,public_str))         #insert public key in public key directory 
   db.commit()
   close_db(db,cursor)
   return redirect(url_for('purchase_order'))

# checks if there is an entry in the database -check password -make an entry
@app.route('/verify')
def verify_pw():
   global EMAIL,PW
   (db,cursor)= open_db()
   cursor.execute("""select Password from Cred where EmailID=%s""",(EMAIL,))
   pw =cursor.fetchone()
   close_db(db,cursor)
   if (pw==None):            #no entry in db
       return redirect(url_for('insert_data'))
   elif  (pw[0] != PW):             #wrong password
       return redirect(url_for('wrong_pw'))
   return redirect(url_for('purchase_order')) 

#Index page for credentials  
@app.route('/',methods=['POST','GET'])
def login():
    global EMAIL,PW
    if request.method== 'POST':
        EMAIL= request.form['EmailID']
        PW = request.form['Password']
        return redirect(url_for('verify_pw'))
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()

