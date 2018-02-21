import urllib2
import json
import sys
def init(data, token):
    confurl = "https://cloud4rpi.io/api/devices/%s/config" % token
    req = urllib2.Request(url=confurl, data=json.dumps(data), headers={"Content-Type": 
                                                        "application/json"})

    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        sys.stderr.write("cloud4rpi device init failed.\n")
        sys.stderr.write("  Error code: %d for URL: %s\n" % (e.getcode(), e.geturl()))
        sys.exit(1)

def tocloud4rpi(data, token):
    confurl = "https://cloud4rpi.io/api/devices/%s/data" % token
    data = json.dumps(data)
    try:
        req = urllib2.Request(url=confurl, data=data, headers={"Content-Type": 
                                                        "application/json"})
    except urllib2.HTTPError, e:
        sys.stderr.write("Upload to cloud4rpi failed.\n")
        sys.stderr.write("  %r\n" % e)
        sys.exit(1)
    response = urllib2.urlopen(req)
    print "Data update:",response.read()