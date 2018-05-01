import MySQLdb

db = MySQLdb.connect(host="localhost",user="root",passwd="Welcome1")
cursor = db.cursor()
cursor.execute("""Create database spo""")
cursor.execute("""use spo""")
cursor.execute("""CREATE TABLE Cred (
    Email varchar(255),
    Password varchar(255),
    PrivateKey varchar(5000)
    )""")

cursor.execute("""CREATE TABLE PublicKeyDir (
    Email varchar(255),
    PublicKey varchar(5000)
    )""")
cursor.close()
db.close()
