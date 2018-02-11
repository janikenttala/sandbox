import qhue
import json
import urllib2
import datetime
import sys
import requests
import os

def init_token(data, token):
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

def get_cloud4rpi_device_and_token(name):
    try:
        import config
    except ImportError:
        return {"device" : "default" }

    device = None
    for device_name in config.devices:
        if name in config.devices[device_name]:
            device = device_name
            break
    if device == None:
        device = "default"

    return {"device": device}

def temperaturesensor(sensor, name):
    data = {"type": "temperature", "value": sensor["state"]["temperature"] / 100.0}
    data.update(get_cloud4rpi_device_and_token(name))
    return data

def ambientsensor(sensor, name):
    data  = {"type": "ambient light", "value": sensor["state"]["lightlevel"]}
    data.update(get_cloud4rpi_device_and_token(name))
    return data

def motion(sensor, name):
    data = {"type": "motion", "value": sensor["state"]["status"], "last update": sensor["state"]["lastupdated"]}
    data.update(get_cloud4rpi_device_and_token(name))
    return data


def main():
    
    try:
        import config
        huetoken = os.getenv("huetoken", config.huetoken)
        bridge_ip = os.getenv("bridge_ip", config.bridge_ip)
        cloud4rpi_device_token = os.getenv("cloud4rpi_device_token", config.cloud4rpi_device_token)
    except ImportError:
        huetoken = os.getenv("huetoken", None)
        bridge_ip = os.getenv("bridge_ip", None)
        cloud4rpi_device_token = os.getenv("cloud4rpi_device_token", None)
        if huetoken == None or bridge_ip == None or cloud4rpi_device_token == None:
            sys.stderr.write("huetoken: %s\n" % huetoken)
            sys.stderr.write("bridge_ip: %s\n" % bridge_ip)
            sys.stderr.write("cloud4rpi_device_token: %s\n" % cloud4rpi_device_token)
            sys.stderr.write("One of the settings was not set. See README.md on how to do it.\n")
            sys.exit(1)


    received_data = list()
    bridge = qhue.Bridge(bridge_ip, huetoken)
    try:
        sensors = bridge.sensors()
    except (qhue.qhue.QhueException, requests.exceptions.InvalidURL) as  e:
        sys.stderr.write("Hue API request failed. Did you add correct values to config.py?\n")
        sys.stderr.write("  %r\n" % e)
        sys.exit(1)

    payload = dict()
    for i in sensors:
        name = sensors[i]["name"]
        if "Motion" in name:
            data = motion(sensors[i], name)
        elif "ambient" in name:
            data  = ambientsensor(sensors[i], name)
        elif "temperature" in name: 
            data = temperaturesensor(sensors[i], name)
        else:
            continue
        
        device = data["device"]

        payload.update({ device + " " + data["type"]: data["value"] })

    init_list = list()
    for k,v in payload.iteritems():
        init_dict = {"name": k, "type":"numeric"}
        init_list.append(init_dict)
    
    # Make sure the device is initialized for the to-be-sent dataset
    init_token(init_list, cloud4rpi_device_token)

    # Send
    package = {"ts": datetime.datetime.utcnow().isoformat(), "payload": payload}
    tocloud4rpi(package, cloud4rpi_device_token)
    

if __name__ == "__main__":
    main()