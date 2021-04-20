FROM python:3.7-slim-buster
MAINTAINER Dominik Kotarski dojitza@gmail.com
COPY generator.requirements.txt ispovestGeneratorServer.py constants.py .
COPY checkpoint/ /checkpoint/
RUN pip3 install -r generator.requirements.txt
CMD ["python3", "ispovestGeneratorServer.py"]
EXPOSE 8080
#todo dodati port za rabbitmq, napraviti docker'compose i testirati sve skupa