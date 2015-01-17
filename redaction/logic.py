from satella.channels.sockets import SelectHandlingLayer, ServerSocket
from socket import socket, AF_INET, SOCK_STREAM
from satella.threads import BaseThread
from cyrkus.shared import DataReceiverSocket

class RSHL(SelectHandlingLayer, BaseThread):
    def __init__(self, lsport):
        SelectHandlingLayer.__init__(self)
        BaseThread.__init__(self)
        ss = socket(AF_INET, SOCK_STREAM)
        ss.bind(lsport)
        self.server_channel = ServerSocket(ss)
        self.server_channel.listen(backlog=60)

        self.register_channel(self.server_channel)

    def on_readable(self, channel):
        if channel == self.server_channel:
            nc = self.server_channel.read()
            nc = DataReceiverSocket(nc)
            self.register_channel(nc)
        else:
            # We have actual data in this shit
            if channel.is_finished and channel.readed_data != None:
                # process that
                print 'Received %s' % (repr(channel.readed_data), )

    def run(self):
        while not self._terminating:
            self.select(timeout=5)
