from socket import *

Host = 'localhost'
Port = 12345
Bufsize = 1024
Addr = (Host,Port)

UDPCliSock = socket(AF_INET,SOCK_DGRAM)

while True:
    data = raw_input('>')
    if not data:
        break
    UDPCliSock.sendto(data,Addr)
    data,Addr = UDPCliSock.recvfrom(Bufsize)
    if not data:
        break
    print data

UDPCliSock.close()
