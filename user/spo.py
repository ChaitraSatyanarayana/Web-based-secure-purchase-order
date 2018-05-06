from flask import Flask, request, render_template,redirect,url_for
import MySQLdb
import rsa 
import cPickle as pickle
from handle_db import open_db, close_db
from articles import article
from email_credentials import *
from handle_email import *

#Global variables
KEY_LENGTH = 2048

#article costs 
laptop =article(800)
bag = article(50)
book = article(5)
pen =article(1)

app = Flask(__name__)
  

@app.route('/confirm_order',methods=['POST','GET'])
def confirm_order(): 
    if request.method== 'POST':
       if (request.form['Confirm']=='Confirm'): 
            send_confirm_email()      
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
        laptop.quantity=int( request.form['laptopq'])
        bag.quantity=int( request.form['bagq'])
        book.quantity=int( request.form['bookq'])
        pen.quantity=int( request.form['penq'])
        laptop.total = laptop.quantity* laptop.cost
        bag.total = bag.quantity * bag.cost
        book.total = book.quantity*book.cost
        pen.total = pen.quantity*pen.cost   
        total_amount =laptop.total+bag.total+book.total+pen.total
        return render_template('confirm_order.html',laptopt=laptop.total,bagt=bag.total,bookt=book.total,pent=pen.total,amount=total_amount,laptopq=laptop.quantity,penq=pen.quantity,bagq=bag.quantity,bookq=book.quantity)
    return render_template('purchase_order.html')
	
# generate public and private keys and insert in credetials and public library tables
@app.route('/insert_data/<email>/<password>')
def insert_data(email,password):
   print ("insert_data")
   (db,cursor)= open_db()
   (public,private)=rsa.newkeys(KEY_LENGTH)   #generate public and private keys
   public_str = pickle.dumps(public)           #convert public key object into string - pickling
   private_str = pickle.dumps(private)        #convert private key object into string - pickling
   cursor.execute("""INSERT INTO Cred VALUES (%s,%s,%s)""",(email,password,private_str))    #insert credentials
   db.commit()
   cursor.execute("""INSERT INTO PublicKeyDir VALUES (%s,%s)""",(email,public_str))         #insert public key in public key directory 
   db.commit()
   close_db(db,cursor)
   return redirect(url_for('purchase_order'))

# checks if there is an entry in the database -check password -make an entry
@app.route('/verify/<mail>/<password>')
def verify_pw(mail,password):
   (db,cursor)= open_db()
   cursor.execute("""select Password from Cred where EmailID=%s""",(mail,))
   pw =cursor.fetchone()
   close_db(db,cursor)
   if (pw==None):            #no entry in db
       return redirect(url_for('insert_data',email=mail,password=password))
   elif  (pw[0] != password):             #wrong password
       return redirect(url_for('wrong_pw'))
   return redirect(url_for('purchase_order',email=mail)) 
   
  
#Index page for credentials  
@app.route('/',methods=['POST','GET'])
def login():
    if request.method== 'POST':
        email= request.form['EmailID']
        pw = request.form['Password']
        return redirect(url_for('verify_pw',mail=email,password=pw))
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()





