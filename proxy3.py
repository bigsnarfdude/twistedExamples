#! /usr/bin/env python
"""
This program is a proxy server and holds cached webpages
"""

from twisted.web.client import getPage
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from twisted.internet import defer

class CacheServerProxyProtocol(basic.LineReceiver):
    
    def __init__(self, cache={}):
        self.cache = cache

    def lineReceived(self, line):
        if not line.startswith("http://"):
            return
        
        if line in self.cache:
            page = self.cache[line]
            return self.results_to_client(page)

        else:
            result = getPage(line)
            return self.results_to_client(result)
    
    @addCallback.inline
    def addCache(self, url, page):
        self.cache[url] = page
        return page
    
    @addCallback.inline
    def results_to_client(self, page):
        self.transport.write(page)
        self.transport.loseConnection()

         
factory = protocol.ServerFactory()
factory.protocol = CacheServerProxyProtocol()

endpoints.serverFromString(reactor, "tcp:8000").listen(factory)
reactor.run()

