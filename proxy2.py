from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic

import urllib2
import time

class ProxyProtocol(basic.LineReceiver):

        def lineReceived(self, line):


                    if line.startswith("say:"):
                                    
                                    self.transport.write("this line is say")
                                            
                                                    elif line.startswith("message:"):
                                                                
                                                                    self.transport.write("this line is message")
                                                                            
                                                                                    elif line.startswith("http://"):
                                                                                                    
                                                                                                    start = time.time()
                                                                                                                print "Fetching", line
                                                                                                                            data = urllib2.urlopen(line).read()
                                                                                                                                        print "Fetched", line
                                                                                                                                                    self.transport.write(data)
                                                                                                                                                                self.transport.loseConnection()
                                                                                                                                                                            print "Took", time.time() - start

                                                                                                                                                                            factory = protocol.ServerFactory()
                                                                                                                                                                            factory.protocol = ProxyProtocol

                                                                                                                                                                            endpoints.serverFromString(reactor, "tcp:8000").listen(factory)
                                                                                                                                                                            reactor.run()
