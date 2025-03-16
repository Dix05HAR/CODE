from confluent_kafka import Producer

# Настройки продюсера
conf = {
    'bootstrap.servers': 'localhost:9092',  # Адрес вашего Kafka брокера
    'client.id': 'python-producer'
}

# Создание продюсера
producer = Producer(conf)

# Функция для обработки успешной отправки сообщения
def delivery_report(err, msg):
    if err is not None:
        print('Сообщение не отправлено: {}'.format(err))
    else:
        print('Сообщение отправлено в {} [{}]'.format(msg.topic(), msg.partition()))

# Отправка сообщения
topic = 'test_topic'
message = 'Hello Kafka from Python!'

producer.produce(topic, message, callback=delivery_report)

# Ждем, пока все сообщения будут отправлены
producer.flush()