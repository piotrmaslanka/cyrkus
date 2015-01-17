# Read configuration
import struct, json, socket, time
from satella.unix import daemonize, hang_until_sig
from cyrkus.redaction.logic import RSHL

def run(cfg):
    rshl = RSHL(tuple(cfg['listen_interface']))

    rshl.start()

    hang_until_sig()

    rshl.terminate()
    rshl.join()
