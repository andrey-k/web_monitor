"""Site class. Class has methods to test site availability, get its content,
check requirements and write result into log-file."""
import socket
import urllib2
import time
import logging

from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('web_monitor.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s [%(name)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


class Site:

    def __init__(self, name, url, requirement):
        self.name = name
        self.url = url
        self.requirement = requirement
        self.time_elapsed = None
        self.status_code = 599
        self.has_requirement = False

    def __str__(self):
        return '{}({})'.format(self.name, self.url)

    def __repr__(self):
        return 'Site({}, {}, {})'.format(self.name, self.url, self.requirement)

    def check_site(self):
        start_time = time.time()

        self.time_elapsed = 0.0
        self.status_code = 599
        self.has_requirement = False

        site_content = self.get_content()
        if site_content:
            self.check_requirement(site_content)
        self.time_elapsed = time.time() - start_time

        logger.info('{} status: {} time: {:.2f}s requirement:{}'
                    .format(self.url, self.status_code,
                            self.time_elapsed, self.has_requirement))

    def get_content(self):
        html_content = None
        request = urllib2.Request(self.url)

        try:
            response = urllib2.urlopen(request, timeout=5)
        except urllib2.URLError as e:
            # Could have more specific check to see
            # is it a HTTPError or URLError
            self.status_code = e.code
        except socket.timeout as e:
            # 599 Network connect timeout error
            # Microsoft HTTP proxies use that code
            # but this status code is not specified in any RFCs
            self.status_code = 599
        else:
            self.status_code = response.code
            html_content = response.read()
            response.close()

        return html_content

    def check_requirement(self, content):
        soup = BeautifulSoup(content)
        tag_name = self.requirement.get('tag', None)
        attr_data = {key: value
                     for key, value in self.requirement.items()
                     if key != 'tag'}

        if (soup.find_all(tag_name, **attr_data)):
            self.has_requirement = True
