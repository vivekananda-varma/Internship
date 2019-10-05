# Internship
A study on Diffe hellman key exchange protocol

Problem statement:-
Establish a 128-bit shared secret key between two processes in different machines with the help of Authenticated Diffie-Hellman key establishment protocol. That is, the processes already have a shared secret key, and they want to establish a new shared secret key ensuring perfect forward secrecy. For authentication, you can use any of the MAC function (CMAC or HMAC). The program should use the following group to establish the shared secret key.
•	Multiplicative residue group Zp*, where p is a 512-bit prime number.
For this case you need to get a prime subgroup of Zp*, where Diffie-Hellman key establishment protocol can be run. The program should display the common key established in a separate window for each process, and the time required to compute the key (excluding communication delay) in each of the group. Each process must be executed in a separate terminal and these two processes should communicate with each other using TCP or UDP protocol.
