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

    def send(self, alert):
        """Message sending interface"""
        alert = alert.replace(u'ł', 'l').replace(u'Ł', 'L') # because normalize NFD sucks at this char
        alert = unicodedata.normalize('NFD', alert).encode('ascii', 'ignore')

        conn = httplib.HTTPSConnection('api1.multiinfo.plus.pl', '443', cert_file=self.config['certfile'])

        data = urllib.urlencode({
                'login': self.config['login'],
                'password': self.config['password'],
                'serviceId': self.config['serviceId'],
                'text': alert,
                'dest': self.config['target'],
                'orig': self.config['orig']
        })

        conn.request('GET', '/sendsms.aspx?'+data)
        conn.getresponse()
