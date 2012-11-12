from twisted.internet import reactor, protocol, endpoints


class UpperProtocol(protocol.Protocol):
    

    def connectionMade(self):
        self.factory.count += 1
        self.transport.write("Hi! Send me text to convert to uppercase, count = %s \n" % self.factory.count)

    def connectionLost(self, reason):
        self.factory.count -= 1

    def dataReceived(self, data):
        self.transport.write(data.upper())
        self.transport.loseConnection()


class CountingFactory(protocol.ServerFactory):

    protocol = UpperProtocol
    count = 0

endpoints.serverFromString(reactor, "tcp:8000").listen(CountingFactory())
reactor.run()
