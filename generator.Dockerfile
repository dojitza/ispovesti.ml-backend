FROM python:3.7-slim-buster
MAINTAINER Dominik Kotarski dojitza@gmail.com
RUN apt-get update && apt-get install -y wget
COPY generator.requirements.txt ispovestGeneratorServer.py constants.py .
RUN pip3 install -r generator.requirements.txt
RUN wget https://github.com/dojitza/ispovesti.ml-backend/releases/download/v2.0/trained_model.tar && tar -xf trained_model.tar && rm trained_model.tar
CMD ["python3", "ispovestGeneratorServer.py"]