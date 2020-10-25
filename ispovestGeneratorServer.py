import gpt_2_simple as gpt2
import os
import time
import socket
import pika

import constants

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1')


def generateIspovest(prefix):
    text = gpt2.generate(sess,
                         length=256,
                         prefix=prefix,
                         temperature=0.7,
                         nsamples=1,
                         batch_size=1,
                         top_k=40,
                         truncate='\n',
                         return_as_list=True
                         )
    return text[0]


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=constants.GENERATION_QUEUE_NAME)


def on_request(ch, method, props, body):
    print('received: ' + body.decode('UTF-8'))
    response = generateIspovest(body.decode('UTF-8'))
    print('done with: ' + response)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=constants.GENERATION_QUEUE_NAME,
                      on_message_callback=on_request)
print('serving')
channel.start_consuming()
