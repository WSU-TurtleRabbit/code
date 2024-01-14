### This is an example file on simple Client-Server Communication.a

import socket


IP = "127.0.0.1"
PORT = 2024
serverSock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((IP, PORT))

while True:
    data,addr = serverSock.recvfrom(1024)
    print(str(data))
    msg = b'status check'
    serverSock.sendto(msg,addr)