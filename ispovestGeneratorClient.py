import uuid
import socket
import constants
import pika
import collections

clientDict = collections.OrderedDict()


class IspovestGenerationClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(
            queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def generate(self, prefix):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=constants.GENERATION_QUEUE_NAME,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=prefix)
        # todo if not started return false
        return True

    def poll(self):
        self.connection.process_data_events()
        if self.response is not None:
            return self.response.decode('UTF-8')
        else:
            return None


def generateIspovest(prefix, authorIdHash):
    ispovestGenerationClient = IspovestGenerationClient()
    clientDict[authorIdHash] = ispovestGenerationClient
    started = ispovestGenerationClient.generate(prefix)
    return started


"""
returns ispovest text if finished, none if not finished
"""


def pollGeneratedIspovest(authorIdHash):
    try:
        ispovestGenerationClient = clientDict[authorIdHash]
        retval = ispovestGenerationClient.poll()
        if retval is not None:
            clientDict.pop(authorIdHash, None)
        return retval
    except KeyError:
        print('nope')
        return None


def getQueueLength():
    return len(clientDict.keys())


def getQueuePosition(authorIdHash):
    return list(clientDict.keys()).index(authorIdHash)
