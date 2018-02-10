FROM alpine

RUN apk -U upgrade && \
    apk add \
        curl \
        openssl \
        py-pip \
        python
RUN pip install qhue
WORKDIR /root
ADD code .

# Run in loop
CMD sh run.sh

# Run once
#CMD python hue2rpi.py