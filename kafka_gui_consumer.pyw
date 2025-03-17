import sys
import threading
from kafka import KafkaConsumer
import tkinter as tk
from tkinter import scrolledtext

class KafkaConsumerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kafka Consumer")
        self.root.geometry("600x400")

        # Создаем элементы интерфейса
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=20)
        self.text_area.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text="Получить сообщение", command=self.get_message)
        self.button.pack(pady=10)

        # Создаем consumer для Kafka
        self.consumer = KafkaConsumer(
            'Test_topic',  # Тема, из которой будем получать сообщения
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',  # Начинать с самого начала
            group_id='my-group'  # Название группы
        )

        # Поток для прослушивания сообщений
        self.thread = threading.Thread(target=self.listen_to_kafka, daemon=True)
        self.thread.start()

    def listen_to_kafka(self):
        # Вечный цикл, слушаем сообщения в фоне
        for message in self.consumer:
            message_text = message.value.decode('utf-8')
            self.text_area.insert(tk.END, f"Получено сообщение: {message_text}\n")
            self.text_area.yview(tk.END)  # Прокрутка вниз
            self.root.update_idletasks()  # Обновление интерфейса

    def get_message(self):
        # Запускаем обработчик для получения сообщения
        pass

if __name__ == "__main__":
    root = tk.Tk()
    gui = KafkaConsumerGUI(root)
    root.mainloop()
