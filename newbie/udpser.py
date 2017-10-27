from socket import *
from time import ctime

Host = ''
Port = 12345
Bufsize = 1024
Addr = (Host,Port)

UDPSerSock = socket(AF_INET,SOCK_DGRAM)
UDPSerSock.bind(Addr)

while True:
    print 'Waiting for massage...'
    data,cli = UDPSerSock.recvfrom(Bufsize)
    UDPSerSock.sendto("[%s]:%s" % (str(ctime()),data),cli)
    print 'Received from and returned to:',cli

UDPSerSock.close()
