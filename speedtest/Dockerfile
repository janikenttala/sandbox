FROM alpine

RUN apk -U upgrade && \
    apk add \
        py-pip \
        python
RUN pip install speedtest-cli
WORKDIR /root
ADD cloud4rpi.py example.json speed2cloud4rpi.py run.sh ./

# Run in loop
CMD sh run.sh
