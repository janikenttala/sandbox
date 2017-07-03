#!/usr/bin/env python3
"""Serve github timeline """
# based on example at:
# https://daanlenaerts.com/blog/2015/06/03/create-a-simple-http-server-with-python-3/

from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.request
import time
import json

import timelineparse
# HTTPRequestHandler class

lastCache = 0
raw_timeline = ""

class timelineServer(SimpleHTTPRequestHandler):
    """blah"""
    def __init__(self, request, client_address, server):
        self.raw_timeline = ""
        SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def err(self):
        self.send_response(404)
        self.send_header('Content-type', "text/html")
        self.end_headers()
        message = "ERRR" + self.path
        self.wfile.write(bytes(message, "utf8"))

    def _send(self, message, content_type):
        """ blah """
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(bytes(message + "\n", "utf8"))
        return

    def do_GET(self):
        # Investigate: initialising self.raw_timeline to "" and assigning
        # value to it is not preserved, next do_GET it is empty again.
        global raw_timeline

        allowed = ["/timeline.html", "/timeline.css", "/timeline.js"]
        #allowed.append("/data/timeline.json") # test data

        if self.path in allowed:
            SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == "/data/timeline.json":
            timeline = list()
            if cache_expired(10):
                timeline = list()
                raw_timeline = getgit("evilon",
                                      "<key>",
                                      debug=False)
            for line in parsetimeline(raw_timeline):
                timeline.append(line)

            self._send(json.dumps(timeline), "application/json")
        else:
            self.err()


def run():
    """ Start the webserver """
    print('starting server...')
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, timelineServer)
    print('running server...')
    httpd.serve_forever()

def cache_expired(cache_time):
    """ Retrieve only if cache_time has passed """
    global lastCache
    now = time.time()
    if now - lastCache > cache_time:
        lastCache = now
        return True

    return False

def parsetimeline(timeline):
    timeline = timeline.encode('utf-8')
    timelineindex = dict()

    for line in timelineparse.parse(timeline):
        if len(line) == 0:
            continue
        linedict = json.loads(line)
        index = linedict["time"] + "-" + str(time.time())

        timelineindex[index] = linedict

    #sort here
    for key in sorted(timelineindex,reverse=True):
        yield timelineindex[key]


def getgit(user, key, debug=False):
    """ Retrieve git timeline """
    if debug:
        debug_json = open("./data/1.json", "r").read()
        return debug_json

    url = "https://api.github.com/users/%s/events?page=$i&per_page=100" % (user)
    headers = {'Authorization': 'token %s' % key}
    myrequest = urllib.request.Request(url, headers=headers)
    print("REQUESTING", url)
    with urllib.request.urlopen(myrequest) as handle:
        timeline_data = handle.read().decode('utf-8')
    return timeline_data

run()
