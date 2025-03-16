import logging
from confluent_kafka import Producer

# Включить логирование для Kafka
logging.basicConfig(level=logging.DEBUG)

# Настройки продюсера
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'python-producer'
}

# Создание продюсера
producer = Producer(conf)

# Функция для обработки успешной отправки сообщения
def delivery_report(err, msg):
    if err is not None:
        logging.error(f'Сообщение не отправлено: {err}')
    else:
        logging.info(f'Сообщение отправлено в {msg.topic()} [{msg.partition()}]')

# Отправка сообщений
topic = 'test_topic'
message = 'Hello Kafka from Python!'

producer.produce(topic, message, callback=delivery_report)

# Периодически вызываем poll() для обработки сообщений асинхронно
producer.poll(0)

# Даем время на завершение отправки сообщений
producer.flush()
