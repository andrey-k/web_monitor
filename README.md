Simple program that monitors web sites and reports their availability.

Script reads a list of web pages and page requirements from a json file. For each site from list periodically makes an HTTP request. Verifies matches between response and the content requirements. Measures the time it took for the web server. Writes a log file with the progress. Also serve single-page HTTP server.

monitor.py - is the starting point. It has the main function which starts web monitoring, config parser to get data from config.ini file and argument parser to get data from command line. Also it has flag -s or --start_server. In that case script will start simple HTTP server with the address 127.0.0.1:PORT. The page shows status and has ajax call for data updates.

webmonitor.py contains main class of he monitor

sitedata.py has class to work with sites. get request, content and verify it

server.py is the HTTP server

sites.json includes list of sites and their requirements. script can detect text on the page, tag or tag attribute all together.

USAGE:
python monitor.py [-f FILE, --file FILE] [-t TIME_INTERVAL, --time_interval TIME_INTERVAL] [-s, --start_server]

NOTE:
To check existence of the class write "class_" in requirements
