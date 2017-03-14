FROM jfloff/alpine-python:3.4-onbuild

WORKDIR /
EXPOSE 8000
USER nobody
ENV HOME /data

ADD zerobin /app/zerobin

CMD PYTHONPATH=/app python -mzerobin runserver --host=0.0.0.0 --root=/data