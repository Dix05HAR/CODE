import json
import tkinter as tk
from kafka import KafkaProducer

# Конфигурация Kafka
KAFKA_BROKER = 'localhost:9092'  # Адрес брокера Kafka
TOPIC_NAME = 'Test_topic'  # Топик для отправки сообщений

# Создание Kafka-продюсера
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    
)


# Функция отправки сообщения
def send_message():
    message_text = entry.get().strip()

    if not message_text:
        status_label.config(text="Ошибка: сообщение пустое!", fg="red")
        return

    message = {"text": message_text}
    producer.send(TOPIC_NAME, value=message_text.encode('utf-8'))  # Отправляем просто строку
    producer.flush()

    status_label.config(text="Сообщение отправлено!", fg="green")
    entry.delete(0, tk.END)


# Создание GUI с Tkinter
root = tk.Tk()
root.title("Kafka GUI Producer")
root.geometry("400x200")

label = tk.Label(root, text="Введите сообщение для Kafka:")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

send_button = tk.Button(root, text="Отправить сообщение", command=send_message)
send_button.pack(pady=10)

status_label = tk.Label(root, text="", fg="black")
status_label.pack()

# Запуск Tkinter GUI
root.mainloop()
