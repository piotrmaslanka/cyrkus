# Read configuration
import struct, json, socket, time

def run(cfg):
    plugins = {}                    # Immutable plugins DB
    for pluginname, confs in cfg['reporter']['plugins'].iteritems():
        pluginname = str(pluginname)
        p = __import__('cyrkus.reporter.plugins.'+pluginname, fromlist=['Plugin'])
        plugins[pluginname] = p.Plugin(confs)

    def get_json(cfg, plugins):
        p = {}

        for pluginname, objct in plugins.iteritems():
            p[pluginname] = objct.get()

        p = {
            'data': p,
            'nodename': cfg['nodename'],
        }

        jd = json.dumps(p).encode('utf8')
        jd = struct.pack('!L', len(jd))+jd  # data to send

        try:            # send the data to redaction
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(tuple(cfg['reporter']['redaction_address']))
            s.sendall(jd)
            s.close()
        except socket.error:
            try:
                s.close()
            except:
                pass

    while True:
        time.sleep(cfg['reporter']['reporting_interval'])
        get_json(cfg, plugins)
