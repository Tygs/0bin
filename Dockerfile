FROM jfloff/alpine-python:3.4-onbuild

WORKDIR /
EXPOSE 8000

ADD zerobin /app/zerobin

CMD PYTHONPATH=/app python -mzerobin runserver 0.0.0.0