try:
    import pika
    import json
except Exception as e:
    print("Some modules are missing {}".format(e))


def callback(ch, method, properties, body):
    body=body.decode()
    body=body.replace("\'","\"")
    body=json.loads(body)
    print("recieved body",json.dumps(body,indent=4))
    ch.basic_ack(delivery_tag=method.delivery_tag)


credentials = pika.PlainCredentials('test', 'test1234')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.1.62',credentials=credentials))

channel = connection.channel()

while True:
    print("Consuming Message")
    channel.queue_declare(queue='hello', durable=False)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='hello', on_message_callback=callback)
    channel.start_consuming()
