FROM alpine:latest
MAINTAINER Maël Auzias <docker@mael.auzias.net>


# python3
RUN adduser -S python
RUN apk --no-cache add python3

# pip3
RUN apk --no-cache add curl \
    ca-certificates \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py

# 0bin https://github.com/sametmax/0bin
RUN pip install zerobin \
    && chown python:root -R /usr/lib/python3.5/site-packages/zerobin/

USER python

ENTRYPOINT [ "zerobin", "--host=0.0.0.0" ]
