import MySQLdb
import cPickle as pickle
import rsa 

def open_db():
    db = MySQLdb.connect(host="localhost",user="root",passwd="Welcome1",db="spo")  #connect to db
    #prepare a cursor object
    cursor = db.cursor()
    return (db,cursor)

def close_db(db,cursor):
   cursor.close()
   db.close()

def get_privatekey(email):
    (db,cursor)=open_db()#open database 
    cursor.execute("""select PrivateKey from Cred where EmailID=%s""",(email,))
    private_key_str = cursor.fetchone()   #get private key
    private_key = pickle.loads(private_key_str[0])      #private key string to private key object 
    close_db(db,cursor)    #close db 
    return private_key
    
def get_publickey(email):
    (db,cursor)=open_db()#open database 
    cursor.execute("""select PublicKey from PublicKeyDir where EmailID=%s""",(email,))
    public_key_str = cursor.fetchone()   #get public key key
    public_key = pickle.loads(public_key_str[0])      #private key string to private key object 
    close_db(db,cursor)    #close db 
    return public_key
