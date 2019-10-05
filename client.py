import socket
import random
from random import randrange,getrandbits
import hmac
from hashlib import md5
from time import sleep
import time

def sum_digits(n):
   r = 0
   while n:
       r, n = r + n % 10, n // 10
   return r
   


def pow_mod(x, y, z):
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1
        x = x * x % z
    return number

Host='127.0.0.1'
port=65432


def bitlen(n):
	length=0
	while(n):
		n>>=1
		length=length+1
	return length



def getprim(p):
	k=1
	if((p%10)==0):
		k=k*10
	if((sum_digits(p)%9)==0):
		k=k*9
	if(((p%1000)%8)==0):
		k=k*8
	if((p%7)==0):
		k=k*7
	if((p%10)==0 and ((p%1000)%8)==0):
		k=k/2
	if(((p%10)%2)==0 and (sum_digits(p)%3)==0):
		if((k%6)!=0):
			k=k*6
	if((p%10)==0 and ((p%1000)%8)==0 and ((p%10)%2)==0 and (sum_digits(p)%3)==0 and (sum_digits(p)%9)!=0):
		k=k/2
	if((p%10)!=0 and ((p%1000)%8)!=0 and ((p%10)%2)==0 and (sum_digits(p)%3)==0 and (sum_digits(p)%9)==0):
		k=k/3
	if((p%10)==0 and ((p%1000)%8)!=0 and  ((p%10)%2)==0 and (sum_digits(p)%3)==0):
		k=k/2
	if((p%10)==0 or (p%10)==5):
		if((k%5)!=0):
			k=k*5
	if(((p%100)%4)==0):
		if((k%4)!=0):
			k=k*4
	if((sum_digits(p)%3)==0):
		if((k%3)!=0):
			k=k*3
	if(((p%10)%2)==0):
		if((k%2)!=0):
			k=k*2
	
	return k
	
		
	


def get_primitive_root(p):
	while(1):
		p=p-1
		z=getprim(p)
		q=int(p//z)
		k=is_prime(q,20)
		if(k==True):
			p=p+1
			a=int((p-1)/q)
			while(1):
				h=int(random.randint(1,p-1))
				g=pow_mod(h,a,p)
				if(g>1):
					return g
				else:
					continue
		else:
			p=p+1
			while(1):
				p=p+2
				a=is_prime(p,20)
				if(a==True):
					break
				else:
					continue
			
def function(key,mess):
	l=str(key)
	l=l.encode()
	k=str(mess)
	k=k.encode()
	
	digest_make=hmac.new(l,k,md5)
	return digest_make.hexdigest()
		
def is_prime(n,k):
	if n==2 or n==3:
		return  True
	if n<=1 or n%2==0:
		return False
	s=0
	r=n-1
	while r & 1 == 0:
		s+=1
		r//=2
	for _ in range(k):
		a=randrange(2,n-1)
		x=pow_mod(a,r,n)
		if x!=1 and x!=n-1:
			j=1
			while j<s and x!=n-1:
				x=pow_mod(x,2,n)
				if x==1:
					return False
				j=j+1
			if x!=n-1:
				return False
	return True

def generate_prime_candidate(length):
	p=getrandbits(length)
	p|= (1 << length-1) | 1
	
	return p

def generate_prime_number(length=512):
	p=4
	while not is_prime(p,80):
		 p=generate_prime_candidate(length)
	return p

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

def check1(n):
	if(bitlen(n)==512):
		return n
	elif(bitlen(n)!=512):
		x=bitlen(n)
		y=512-x
		n=n<<y
		return n

def secretno(p):
	secret=int(random.randint(1,p-1))
	return secret


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((Host,port))
p=generate_prime_number()
start=time.time()
q=get_primitive_root(p)
end=time.time()
print('Time to get primitive root is: ',end-start)
q=check1(q)
ssk=320254980808577290166329208873035182523
while 1:
	k=input('Press ''enter'' to generate new shared secret key:')
	if k=='exit':
		break
	start=time.time()
	p=str(p)
	q=str(q)
	s.send(p.encode())
	s.send(q.encode())
	p=int(p)
	g=int(q)
	print('primitive root is: ',g)
	print('Public keys loaded!')
	a=secretno(p)
	x1=pow(g,a,p)
	hm=function(ssk,x1)
	x1=str(x1)
	hm=str(hm)
	sleep(0.5)
	s.send(x1.encode())
	sleep(0.5)
	y1=s.recv(1024).decode()
	sleep(0.5)
	s.send(hm.encode())
	sleep(0.5)
	hm1=s.recv(1024).decode()
	sleep(0.5)
	y1=int(y1)
	hm2=function(ssk,y1)
	if(hm1!=hm2):
		print('hash value did not match')
		break
	print('Meessage authenticated!!')
	x=pow_mod(g,a,p)
	x=str(x)
	s.send(x.encode())
	y=s.recv(1024).decode()
	y=int(y)
	key=pow_mod(y,a,p)
	key=cutbits(key)
	key=check(key)
	end=time.time()
	print('secret key is: ',key)
	ssk=key
	
s.close()


