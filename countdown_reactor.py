class Countdown (object):

    counter = 5

    def count(self):
        if self.counter == 0:
            reactor.stop()
        else:
            print self.counter, '...'
            self.counter -= 1
            time.sleep(1)
            reactor.callLater(1, self.count)

from twisted.internet import reactor
import time

reactor.callWhenRunning(Countdown().count)
reactor.run()
