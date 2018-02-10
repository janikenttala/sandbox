
# Hue2Cloud4RPi

Get data from Hue bridge and upload it to Cloud4rpi

## Instructions

1. You need to know the address of your Hue bridge. [Philips lists some options](https://developers.meethue.com/documentation/getting-started). I just used ```tcpdump -ni <interface> -A multicast```
1. You need an api key for your bridge. See again [Philips documentation](https://developers.meethue.com/documentation/getting-started)
1. You need cloud4rpi device token. You can get it by creating a [new cloud4rpi device](https://cloud4rpi.io/devices)

## Configure

First clone this repository to yourself.
Copy ```code/config.py.example``` to ```code/config.py``` and add your configuration.
See "Instructions" section to figure out correct values.

## Build & Run

You need to build every time you change configuration. If you have a working
setup, you can just run.

```!shell
docker build -t riphue .
docker run -ti --rm riphue
```

## References

* <https://github.com/quentinsf/qhue>
* <https://developers.meethue.com/documentation/getting-started>

Kudos to Turmi0 for pointers and examples.