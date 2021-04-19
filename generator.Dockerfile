FROM python:3.8-slim-buster
MAINTAINER Dominik Kotarski dojitza@gmail.com
RUN apt-get update && apt-get install -y \
  && rm -rf /var/lib/apt/lists/*
COPY service.requirements.txt constants.py db.py helpers.py ispovestGeneratorClient.py main.py wsgi.py migrations.py .
RUN pip3 install -r service.requirements.txt
RUN python3 migrations.py
CMD ["python3", "ispovestGeneratorServer.py"]
EXPOSE 8080
#todo, dodati dl modela s google drajva