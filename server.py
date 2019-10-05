import socket
import random
import hmac
from hashlib import md5
from time import sleep
import time
Host='127.0.0.1'
port=65432


def function(key,mess):
	l=str(key)
	l=l.encode()
	k=str(mess)
	k=k.encode()
	
	digest_make=hmac.new(l,k,md5)
	return digest_make.hexdigest()


def bitlen(n):
	length=0
	while(n):
		n>>=1
		length=length+1
	return length

def pow_mod(x, y, z):
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1
        x = x * x % z
    return number

def cutbits(n):
	r=0
	for i in range (0,128):
		k=n%2
		n=n//2
		r=r | (k<<i)
	return r


def check(n):
	if(bitlen(n)==128):
		return n
	elif(bitlen(n)!=128):
		x=bitlen(n)
		y=128-x
		n=n<<y
		return n


def secretno(p):
	secret=int(random.randint(1,p-1))
	return secret
	


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((Host,port))
s.listen()
print('server started and listening')
conn,addr=s.accept()
print('connected by',addr)
ssk=320254980808577290166329208873035182523
while 1:
	start=time.time()
	p=conn.recv(1024).decode()
	q=conn.recv(1024).decode()
	p=int(p)
	g=int(q)
	print('primitive root is: ',g)
	print('Public keys are ready!')
	b=secretno(p)
	y1=pow_mod(g,b,p)
	hm=function(ssk,y1)
	y1=str(y1)
	hm=str(hm)
	sleep(0.5)
	conn.send(y1.encode())
	sleep(0.5)
	x1=conn.recv(1024).decode()
	sleep(0.5)
	conn.send(hm.encode())
	sleep(0.5)
	hm1=conn.recv(1024).decode()
	sleep(0.5)
	x1=int(x1)
	hm2=function(ssk,x1)
	if(hm1!=hm2):
		print('hash value did not match')
		break
	print('meassge authenticated')
	y=pow_mod(g,b,p)
	y=str(y)
	conn.send(y.encode())
	x=conn.recv(1024).decode()
	x=int(x)
	key=pow_mod(x,b,p)
	key=cutbits(key)
	key=check(key)
	end=time.time()
	print('shared secret key is: ',key)
	ssk=key



conn.close()
s.close()
				

