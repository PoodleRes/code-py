from socket import *
from time import ctime

Host = gethostname()
Port = 12345
Bufsize = 2048
Addr = (Host,Port)

TcpSerSock = socket(AF_INET,SOCK_STREAM)
TcpSerSock.bind(Addr)

TcpSerSock.listen(5)

while True:
    print 'Waiting for connection...'
    TcpCliSock ,cli = TcpSerSock.accept()
    print 'connection from:',cli

    while True:
        data = TcpCliSock.recv(Bufsize)
        if not data:
            break
        TcpCliSock.send('[%s]:%s' % (str(ctime()),data))
    TcpCliSock.close()
TcpSerSock.close()
