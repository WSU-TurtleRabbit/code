import socket

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Robot_id = 1
IP = "127.0.0.1"
PORT = 2024

msg = bytes(Robot_id)
clientSock.sendto(msg,(IP, PORT))

data,addr = clientSock.recvfrom(1024)
print(str(data))
clientSock.close()

