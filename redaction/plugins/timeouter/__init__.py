# coding=UTF-8
"""
SMS Plus GSM MultiInfo gateway
"""
import time
from hashlib import sha1
import unicodedata, httplib, urllib

class Plugin(object):
    def __init__(self, config, plugins):
        """@param config: configuration, as seen in config.json"""
        self.config = config

        self.timeout_intervals = {} # plugin name => reporting_interval
        self.last_reports = {}      # plugin name => timeout of last reporting
        self.plugins = plugins
        
        self.problems = set()   # names of node with problems

    def timepulse(self):
        """Called periodically"""
        now = time.time()

        for nodename in self.last_reports.iterkeys():

            is_offline = self.last_reports[nodename] + self.timeout_intervals[nodename]*3 < now

            if is_offline and nodename not in self.problems:
                # new offliner
                self.problems.add(nodename)
                for plugin in self.plugins.itervalues():
                    try:
                        plugin.send('Offline: '+nodename)
                    except AttributeError:
                        pass

            elif not is_offline and nodename in self.problems:
                # back online
                self.problems.remove(nodename)
                for plugin in self.plugins.itervalues():
                    try:
                        plugin.send('Online: '+nodename)
                    except AttributeError:
                        pass

    def on_received_report(self, data):
        """Received a report from other node"""
        nodename = data['nodename']

        self.timeout_intervals[nodename] = data['reporting_interval']
        self.last_reports[nodename] = time.time()
