"""Simple HTTP server.
This class will handles any incoming request from the browser
"""
from BaseHTTPServer import BaseHTTPRequestHandler
from os import curdir, sep
import json


class CustomHandler(BaseHTTPRequestHandler):

    def __init__(self, server, sites_data, *args, **kwargs):
        self.data = sites_data
        BaseHTTPRequestHandler.__init__(self, server, *args, **kwargs)

    # Handler for the GET requests. Return HTML page or jsor data.
    def do_GET(self):
        try:
            if self.path in ['/', '/monitor.html']:
                self.path = '/monitor.html'
                with open(curdir + sep + self.path) as html_file:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(html_file.read())
            elif self.path == '/get_data':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps([{
                    'name': site.name,
                    'url': site.url,
                    'time': '{0:.2f}'.format(site.time_elapsed),
                    'status': site.status_code,
                    'requirement': site.has_requirement
                    } for site in self.data if site.time_elapsed]))
            else:
                print(self.path)
                self.send_error(404, 'Wrong url: %s' % self.path)
            return

        except IOError:
            self.send_error(404, 'Wrong url: %s' % self.path)
