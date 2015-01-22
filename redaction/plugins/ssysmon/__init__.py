# coding=UTF-8
"""
SMS Plus GSM MultiInfo gateway
"""
from hashlib import sha1
import unicodedata, httplib, urllib

class Plugin(object):
    def __init__(self, config):
        """@param config: configuration, as seen in config.json"""
        self.config = config


        self.problem_occurred = set()

    def on_received_report(self, data, plugins):
        """Received a report from other node"""
        nodename = data['nodename']

        if 'ssysmon' not in data['data']:
            return

        f = data['data']['ssysmon']

        # ok, let's roll with a failure

        # --------------  Checking CPU problems
        cpu_problem = f['loadavg'][2] > f['cores']  # CPU overusage

        # --------------  Checking free memory
        freemem = f['free_memory'] + f['buffers_memory'] + f['cached_memory']
        lowmem_problem = freemem < 102400   # less than 100 MB available memory

        # --------------  Check free swap
        lowswap_problem = f['free_swap'] < 102400  # less than 100 MB swap

        # --------------  Check free disk
        lowdisk_problem = f['free_disk'] < 102400   # less than 100 MB free disk

        anyproblem = cpu_problem or lowmem_problem or lowswap_problem or lowdisk_problem

        if cpu_problem:
            k = 'CPU problem'
        elif lowmem_problem:
            k = 'RAM problem'
        elif lowswap_problem:
            k = 'SWAP problem'
        elif lowdisk_problem:
            k = 'disk problem'

        if anyproblem:
            # A problem has occurred
            if nodename in self.problem_occurred:
                return      # error already flagged
            else:
                # Error not flagged
                self.problem_occurred.add(nodename)
                for plugin in plugins.itervalues():
                    try:
                        plugin.send('Error: '+nodename+': '+k)
                    except AttributeError:
                        pass
        else:
            if nodename in self.problem_occurred:
                self.problem_occurred.remove(nodename)
                for plugin in plugins.itervalues():
                    try:
                        plugin.send('Safe: '+nodename)
                    except AttributeError:
                        pass
