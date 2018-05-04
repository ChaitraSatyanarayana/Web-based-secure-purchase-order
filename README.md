# Web-based-secure-purchase-order  ;
Project Description 

A secure purchase order system that allows the user to enter a purchase request and routes it (by secure email) to a supervisor for signature and then to the purchasing department.
•All user interactions will be Web based.
•All connections between parties will be preceded by public key mutual authentication.
•The signatures of both the purchaser and the supervisor will be public key based, and will be performed  on a hash of the purchase order. If an order is approved by the supervisor, the orders department can cross check the digest signed by the supervisor with the digest signed by the purchaser. The signature and time stamping is obviously important in preventing  repudiation. I am purposely ignoring the possibility that a user will "publish" their key to back up a repudiation. Ideally, the user 's key will not be easily accessible and, since the whole process takes place in one organization, the possible means of revealing a key are very limited. The biggest threat is a user using another user's machine the forge an order.
•All messages will be encrypted using RSA public key cryptography. Depending on performance (and time) this might be optimized by using RSA to only send a one time secret key.


Follow the following steps

1) download ‘rsa’ module for various cryptographic functions

               sudo pip install rsa

2) install ‘flask’ module

           sudo  pip install Flask

3) Install ‘pickle’

            sudo pip install flask
       
           
4)  install ‘mysql’
        
            sudo apt-get update
      sudo apt-get install mysql-server
for configuring mydql use the below link
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04

 
