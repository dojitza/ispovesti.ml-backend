dockerfile FROM python:3.8-slim-buster
MAINTAINER Dominik Kotarski dojitza@gmail.com
RUN apt-get update && apt-get install -y \
  && rm -rf /var/lib/apt/lists/*
RUN pip3 install -r service.requirements.txt
CMD [gunicorn, main:app, ---bind, 0.0.0.0:8080]
