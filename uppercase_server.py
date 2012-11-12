from twisted.internet import reactor, protocol, endpoints


class UpperProtocol(protocol.Protocol):

    def connectionMade(self):
        self.transport.write("Hi! Send me text to convert to uppercase\n")

    def connectionLost(self, reason):
        pass

    def dataReceived(self, data):
        self.transport.write(data.upper())
        self.transport.loseConnection()


factory = protocol.ServerFactory()
factory.protocol = UpperProtocol

endpoints.serverFromString(reactor, "tcp:8000").listen(factory)
reactor.run()
