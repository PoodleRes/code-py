from SocketServer import (TCPServer as TCP,StreamRequestHandler as SRH)
from time import ctime

HOST = '127.0.0.1'
PORT = 12345
ADDR = (HOST,PORT)

class MyRequestHandlers(SRH):
    def handle(self):
        print 'Connected:',self.client_address
        self.wfile.write('%s:%s' % (str(ctime()),self.rfile.readline()))

tcpServ = TCP(ADDR,MyRequestHandlers)
print 'waiting for connection...'
tcpServ.serve_forever()
