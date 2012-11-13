from twisted.web.client import getPage
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from twisted.internet import defer

import time

class ProxyProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        if not line.startswith("http://"):
            return
        self.getPage(line)

    @defer.inlineCallbacks
    def getPage(self, url):
        starttime = time.time()
        print "Fetching", url
        page = yield getPage(url)
        print "Fetched", url
        self.transport.write(page)
        self.transport.loseConnection()
        print "Took", time.time() - starttime


factory = protocol.ServerFactory()
factory.protocol = ProxyProtocol

endpoints.serverFromString(reactor, "tcp:8000").listen(factory)
reactor.run()

