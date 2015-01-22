# Read configuration
import struct, json, socket, time
from satella.unix import daemonize, hang_until_sig
from cyrkus.redaction.logic import RSHL

def run(cfg):
    plugins = {}                    # Immutable plugins DB
    for pluginname, confs in cfg['redaction']['plugins'].iteritems():
        pluginname = str(pluginname)
        p = __import__('cyrkus.redaction.plugins.'+pluginname, fromlist=['Plugin'])
        plugins[pluginname] = p.Plugin(confs)


    rshl = RSHL(tuple(cfg['listen_interface']), plugins)

    rshl.start()




    hang_until_sig()

    rshl.terminate()
    rshl.join()
