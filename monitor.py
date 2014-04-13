#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Simple program that monitors web sites and reports their availability."""
import sys
import signal
import time
import argparse

from ConfigParser import ConfigParser
from BaseHTTPServer import HTTPServer

from webmonitor import WebMonitor
from server import CustomHandler


def createParser():
    """Command line arguments parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default='sites.json')
    parser.add_argument('-t', '--time_interval', type=int)
    parser.add_argument('-s', '--start_server', action='store_const',
                        const=True, default=False)

    return parser


def main(namespace):
    """Main entry point for the script."""

    config = ConfigParser()
    config.read('config.ini')

    timeout = config.getint('DEFAULT', 'timeout')

    if namespace.time_interval:
        # set time interval if it was provided from command line
        time_interval = namespace.time_interval
    else:
        # or take it from INI file
        time_interval = config.getint('DEFAULT', 'time_interval')

    def signal_handler(*args):
        # Ctrl+C handler to stop monitor
        # TODO: FIXME: fix shutting down server
        print(' wait end of the thread')
        web_monitor.stop()
        #server.socket.close()
        sys.exit()

    web_monitor = WebMonitor(namespace.file, timeout, time_interval)
    web_monitor.start()

    signal.signal(signal.SIGINT, signal_handler)

    def customHandler(server, *args, **kwargs):
        """Quick hack to pass monitoring result to the server.
        Web monitor doesn't store any data except log-file. We don't care
        about monitoring history and we need only fresh data
        that is why it is enough to have data only
        while web monitor is alive.
        """
        CustomHandler(server, web_monitor.sites, *args, **kwargs)

    if namespace.start_server:
        server = HTTPServer(('', config.getint('SERVER', 'port')),
                            customHandler)
        print 'Started httpserver on port ', config.getint('SERVER', 'port')

        #Wait forever for incoming htto requests
        server.serve_forever()
    else:
        while True:
            signal.pause()


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    sys.exit(main(namespace))
