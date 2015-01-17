"""
Standard SYStem MONitoring tool
"""
import multiprocessing, os

class Plugin(object):
    def __init__(self, config):
        """@param config: configuration, as seen in config.json"""
        self.config = config

    def get(self):
        """Return a JSON-able dictionary with parameters gathered from this unit"""

        cores = multiprocessing.cpu_count()

        with open('/proc/loadavg', 'rb') as f: x = f.read()[:-1]

        m1f, m5f, m10f, procs, lastpid = x.split(' ')
        procs_running, procs_total = procs.split('/')

        with open('/proc/meminfo', 'rb') as f: x = f.read()[:-1]

        o = [k.split(':') for k in x.split('\n')]

        p = {}
        for k, v in ((a, b.strip().split(' ')[0]) for a, b, in o):
            try:
                int(v)
            except ValueError:
                pass
            else:
                p[k] = v

        fst = os.statvfs('/')

        return {
            "cores": cores,
            "loadavg": [float(m1f), float(m5f), float(m10f)],
            "total_processes": int(procs_total),
            "running_processes": int(procs_running),
            "total_memory": p['MemTotal'],                        # kB
            "free_memory": p['MemFree'],                          # kB
            "buffers_memory": p['Buffers'],                       # kB
            "cached_memory": p['Cached'],                         # kB
            "total_swap": p['SwapTotal'],                         # kB
            "free_swap": p['SwapFree'],                           # kB
            "free_disk": fst.f_bfree * fst.f_frsize / 1024,       # kB
            "total_disk": fst.f_blocks * fst.f_frsize / 1024,     # kB
        }
