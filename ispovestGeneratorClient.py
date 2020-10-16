import uuid
import socket
import constants
import pika


def generateIspovest(prefix):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((constants.GENERATOR_HOST, constants.GENERATOR_PORT))
        s.sendall(bytes(prefix, 'UTF-8'))
        data = s.recv(1024)
    return data


class IspovestGenerationRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
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
            routing_key='ispovestGeneration',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=prefix)
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode('UTF-8')


def generateIspovestAlt(prefix):
    ispovestGenerationRpcClient = IspovestGenerationRpcClient()
    response = ispovestGenerationRpcClient.call(prefix)
    return response
