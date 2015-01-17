import struct, json, zlib
from satella.channels.sockets import Socket, SelectHandlingLayer

class DataReceiverSocket(Socket):
    """
    A data-receiving endpoint of the socket. Spawned mostly on redaction
    to receive incoming information about node state, but can also
    be expressed in reporters - when redaction issues the commands.

    This is common both for redaction and reporter.
    """

    def __init__(self, sck):
        Socket.__init__(self, sck)
        self.is_finished = False    # whether reception process was completed
        self.readed_data = None     # to be filled in with readed data

    def on_readable(self):
        Socket.on_readable(self)

        if len(self.rx_buffer) < 4:     # Must at least read the header in
            return

        datalen = str(self.read(4, less=False, peek=True))
        datalen, = struct.unpack("!L", datalen)

        if len(self.rx_buffer) < 4+datalen:
            return      # Not enough data!!!

        self.read(4)        # skip the header
        data = self.read(datalen)   # read rest of the data

        try:
            obj = json.loads(zlib.decompress(buffer(data)))
        except: # Failure occurred in recovering the information
            obj = None

        self.readed_data = obj
        self.is_finished = True

        self.close()
