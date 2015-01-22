# coding=UTF-8
"""
SMS Plus GSM MultiInfo gateway
"""
from __future__ import division
from hashlib import sha1
import unicodedata, httplib, urllib, urlparse, json, BaseHTTPServer, time
from satella.threads import BaseThread
from cyrkus.redaction.plugins.httpifc.format import fformat

class HttpServerThread(BaseThread):
    class HTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def __init__(self, request, client_address, server):
            BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
            self.request = request

        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=UTF-8')
                self.end_headers()

                self.wfile.write(fformat(self.server.plugin.last_data, self.server.plugin.last_records))
            else:
                self.send_response(404)

        def do_POST(self):
            nodename = self.path[1:]

            try:
                ld = self.server.plugin.last_data[nodename]
                lr = self.server.plugin.last_records[nodename]
            except KeyError:
                self.send_error(404)
                return

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()


            self.wfile.write(json.dumps(
                    {
                        'node': ld,
                        'secs_ago': int(time.time() - lr)
                    }
            ))

    def __init__(self, calling_plugin, listening_ifc):
        BaseThread.__init__(self)
        self.plugin = calling_plugin
        self.listen_ifc = tuple(listening_ifc)

    def run(self):
        httpd = BaseHTTPServer.HTTPServer(self.listen_ifc, HttpServerThread.HTTPRequestHandler)
        httpd.plugin = self.plugin
        httpd.serve_forever()

class Plugin(object):
    def __init__(self, config, plugins):
        """@param config: configuration, as seen in config.json"""
        self.config = config
        self.plugins = plugins

        self.last_data = {}     # nodename => data dict
        self.last_records = {}  # nodename => last transmit time (timestamp)

        self.http_server = HttpServerThread(self, config['listen_interface'])
        self.http_server.start()

    def on_received_report(self, data):
        """Received a report from other node"""
        self.last_data[data['nodename']] = data
        self.last_records[data['nodename']] = time.time()
