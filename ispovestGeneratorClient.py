import uuid
import socket
import constants
import pika


class IspovestGenerationRpcClient(object):
    def __init__(self, ispovestId):
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

    def call(self, prefix):
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
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode('UTF-8')


def generateIspovest(prefix, ispovestId):
    ispovestGenerationRpcClient = IspovestGenerationRpcClient(ispovestId)
    response = ispovestGenerationRpcClient.call(prefix)
    return response


def getQueueLength():

    params = pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=pika.credentials.PlainCredentials('guest', 'guest'),
    )

    # Open a connection to RabbitMQ on localhost using all default parameters
    connection = pika.BlockingConnection(parameters=params)

    # Open the channel
    channel = connection.channel()

    # Re-declare the queue with passive flag
    res = channel.queue_declare(
        queue=constants.GENERATION_QUEUE_NAME,
        passive=True
    )
    return(res.method.message_count)
