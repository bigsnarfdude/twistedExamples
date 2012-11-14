#! /usr/bin/env python

"""
This program is a simple webserver built with Twisted without the HTTP subclass
"""


from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from twisted.web import client

import time

class WebserverProtocol(basic.LineReceiver):
    def writeDataAndLoseConnection(self, data, url, starttime):
        print "Fetched", url,
        self.transport.write(data)
        self.transport.loseConnection()
        print "Took", time.time() - starttime
    
    def lineReceived(self, line):
        if line.startswith("say:"):
            self.transport.write("this line is say")
        elif line.startswith("message:"):
            self.transport.write("this line is message")
        deferredData = client.getPage(line)
        deferredData.addCallback(writeDataAndLoseConnection, line, self.transport, start)

    def _get_or_head(self, request_string):
        request_method = request_string.split(' ')[0]
        print "Method: ", request_method
        print "Request body: ", request_string

        if (request_method == 'GET') | (request_method == 'HEAD'):
            file_requested = request_string.split(' ')
            file_requested = file_requested[1]

            file_requested = file_requested.split('?')[0]

            if (file_requested == '/'):
                file_requested = '/index.html'

            file_requested = self.www_directory + file_requested
            print "Serving web page [",file_requested,"]"
    
    def _generate_headers(self, code):
        header_server = ''
        if (code == 200):
            header_server = 'HTTP/1.1 200 OK\n'
        elif(code == 404):
            header_server = 'HTTP/1.1 404 Not Found\n'
        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header_server += 'Date: ' + current_date +'\n'
        header_server += 'Server: HTTPTwisted-Server\n'
        header_server += 'Connection: close\n\n'  
        return header_server




test_request = """GET /favicon.ico HTTP/1.1\r\nHost: localhost:8888\r\nConnection: keep-alive\r\nAccept: */*\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: en-US,en;q=0.8\r\nAccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3\r\n\r\n"""


factory = protocol.ServerFactory()
factory.protocol = WebserverProtocol

endpoints.serverFromString(reactor, "tcp:8000").listen(factory)
reactor.run()

