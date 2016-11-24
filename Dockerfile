FROM alpine:3.4
MAINTAINER "Adam Dodman <adam.dodman@gmx.com>"

RUN apk add --no-cache python py-pip \
 && pip install --upgrade pip \
 && pip install paho-mqtt scapy \
 && mkdir dash \
 && ln -s /config/dash.cfg /dash/dash.cfg

ADD main.py /config

CMD ["python","/dash/main.py"]