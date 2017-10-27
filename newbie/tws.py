from twisted.internet import protocol,reactor
from time import ctime

PORT = 12345

class TSServProtocol(protocol.Protocol):
    def connectionMade(self):
        clnt = self.clnt = self.transport.getPeer().host
        print '...connected from :',clnt
    def dataReceived(self,data):
        self.transport.write('[%s]:%s' % (ctime(),data))

fac = protocol.Factory()
fac.protocol = TSServProtocol
print 'waiting for connection...'
reactor.listenTCP(PORT,fac)
reactor.run()
