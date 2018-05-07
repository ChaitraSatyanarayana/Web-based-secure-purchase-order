import rsa
from handle_db import * 
from email_credentials import * 

#returns the message and signature 
def get_sign_msg():
    with open('PO.txt', 'r') as myfile:
        data=myfile.read()    #read the data from the file 
    lst = data.split("SSSS")         # split the content by the delimeter SSSS
    private = get_privatekey(orderdepartment_mail)      # extract private key of supervisor or (order department)
    message = rsa.decrypt(lst[0],private)    
    message = message.decode('utf8')  
    sign1 = rsa.decrypt(lst[1],private)
    sign2 =  rsa.decrypt(lst[2],private)
    signature = sign1+sign2
    return (message,signature)

def get_user_email(msg):         #extracts the user Email ID from PO
    lst1 = msg.split("Email:")
    lst2 = lst1[1].split("\n")
    return (lst2[0])
      

message,signature = get_sign_msg() 
user_email = get_user_email(message)
public = get_publickey(user_email)
if(rsa.verify(message, signature, public)):
    # do when signature and message match
    print("signature verified)








    


