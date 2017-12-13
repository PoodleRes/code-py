#-*- coding: utf-8 -*
import socket

class Server:
    def __init__(self,ip,port):
        self.addr = (ip,port)
        self.BUFSIZE = 25600
        print "[+]Init Successfully"


    def bind(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.addr)
        self.sock.listen(5)
        print "[+]Listening...Address:%s:%s"%self.addr

    def start(self):
        while True:
            print "[+]Waiting..."
            cli, (ip, port) = self.sock.accept()
            print "[+]Connect from:", ip, ':', port
            while True:
                try:
                    print "%s:%s>"%(ip,port),
                    sendmsg = raw_input()
                    cli.send(sendmsg)
                    recvmsg = cli.recv(self.BUFSIZE)
                    print recvmsg
                except Exception as e:
                    print "[-]Disconnect..."
                    break
            cli.close()



def main():
    ss = Server('45.77.218.223',12314)
    ss.bind()
    ss.start()

if __name__ == '__main__':
    main()