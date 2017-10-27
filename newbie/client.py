from socket import *

Host = '127.0.0.1'
Port = 12345
Bufsize = 2048
Addr = (Host,Port)

while True:
    TcpCliSock = socket(AF_INET,SOCK_STREAM)
    TcpCliSock.connect(Addr)
    data = raw_input('> ')
    if not data:
        break
    TcpCliSock.send(data)
    data = TcpCliSock.recv(Bufsize)
    if not data:
        break
    print data
    TcpCliSock.close()
