import json
import sys
import cloud4rpi
import os

data = json.loads(sys.stdin.read())

ping = data["ping"]
timestamp = data["timestamp"]
download = data["download"]
upload = data["upload"]
ip = data["client"]["ip"]
host = data["server"]["host"]


cloud4rpi_device_token = os.getenv("cloud4rpi_device_token", None)

if cloud4rpi_device_token == None:
    sys.stderr.write("Please set cloud4rpi_device_token environment variable.\n")
    sys.exit()

payload = {"ping": ping, "download": download, "upload": upload, "ip":ip, "host":host }
package = {"ts": timestamp, "payload": payload }

init_list = list()
for k,v in payload.iteritems():
    datatype = "numeric"
    if k == "IP" or k == "host": datatype = "string"
    init_dict = {"name": k, "type": datatype}
    init_list.append(init_dict)

print init_list
cloud4rpi.init(init_list, cloud4rpi_device_token)
cloud4rpi.tocloud4rpi(package, cloud4rpi_device_token )