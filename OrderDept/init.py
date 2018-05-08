import MySQLdb
import rsa
from email_credentials import *
import cPickle as pickle

def create_keys(email,pw):
     (public,private) = rsa.newkeys(2048)
     public_str = pickle.dumps(public)
     private_str = pickle.dumps(private)
     db = MySQLdb.connect(host="c7001",user="root",passwd="Passw0rd!")
     cursor = db.cursor()
     cursor.execute("""use spo""")
     cursor.execute("""INSERT INTO Cred VALUES (%s,%s,%s)""",(email,pw,private_str))    #insert credentials
     db.commit()
     cursor.execute("""INSERT INTO PublicKeyDir VALUES (%s,%s)""",(email,public_str))         #insert public key in public key directory
     db.commit()
     cursor.close()
     db.close()

db = MySQLdb.connect(host="c7001",user="root",passwd="Passw0rd!")
cursor = db.cursor()
cursor.execute("""Create database spo""") #create student purchase order database
cursor.execute("""use spo""")
cursor.execute("""CREATE TABLE Cred (      
    EmailID varchar(255),
    Password varchar(255),
    PrivateKey varchar(5000)
    )""")        #create Cred Table

cursor.execute("""CREATE TABLE PublicKeyDir (
    EmailID varchar(255),
    PublicKey varchar(5000)
    )""")       #create Public Key directory table

create_keys(purchasecenter_mail,purchasecenter_password)  #create keys for purchase center and store it in database
create_keys(supervisor_mail,supervisor_password)   #create keys for supervisor and store it in database
create_keys(orderdepartment_mail,orderdepartment_password)                   #create keys for order department and store it in database
cursor.close()
db.close()