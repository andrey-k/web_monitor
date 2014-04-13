"""WebMonitor class. Class runs in separate thread. Read list of sites with
requirements and test it."""
import json

from threading import Thread
from threading import Event

from sitedata import Site


class WebMonitor(Thread):

    def __init__(self, file_name, timeout=30, time_interval=10):
        Thread.__init__(self)
        self.event = Event()
        self.timeout = timeout
        self.time_interval = time_interval
        self.sites = []
        self._sites = []
        self.data_file = file_name

    def __str__(self):
        return 'WebMonitor.source_file = {}'.format(self.file_name,
                                                    self.timeout,
                                                    self.time_interval)

    def __repr__(self):
        return 'WebMonitor({})'.format(self.file_name,
                                       self.timeout,
                                       self.time_interval)

    def run(self):
        self.get_data_from_file()
        self.check_sites()
        # use self.sites for public access
        self.sites = self._sites

        while not self.event.wait(self.time_interval):
            print('start')
            self.get_data_from_file()
            self.check_sites()
            print('wait')

    def get_data_from_file(self):
        """ Read data from file every time before check. In that case file
        with list of sites can be modified without restarting monitor
        which should be on forever (in theory).
        """
        data = {}
        self.sites = self._sites
        try:
            with open(self.data_file) as data_file:
                data = json.load(data_file)
        except ValueError, e:
            print('invalid data file')
        except IOError, e:
            print('no such file')
            self.stop()

        self._sites = [Site(site['name'], site['url'], site['requirement'])
                       for site in data]

    def check_sites(self):
        for site in self._sites:
            site.check_site()

    def stop(self):
        print('stoped')
        self.event.set()
