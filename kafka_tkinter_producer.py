import tkinter as tk
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic

# Конфигурация Kafka
KAFKA_BROKER = 'localhost:9092'  # Адрес брокера Kafka
DEFAULT_TOPIC = 'Test_topic'  # Топик по умолчанию

# Функция для получения списка топиков
def get_topics():
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
        return list(admin_client.list_topics())
    except Exception as e:
        status_label.config(text=f"Ошибка загрузки топиков: {e}", fg="red")
        return [DEFAULT_TOPIC]

# Функция для обновления выпадающего списка топиков
def update_topic_menu():
    menu = topic_menu["menu"]
    menu.delete(0, "end")  # Очищаем меню
    topics.clear()
    topics.extend(get_topics())  # Обновляем список топиков
    for topic in topics:
        menu.add_command(label=topic, command=lambda t=topic: topic_var.set(t))
    topic_var.set(topics[0] if topics else DEFAULT_TOPIC)

# Функция создания топика
def create_topic():
    topic_name = entry_topic.get().strip()
    if not topic_name:
        status_label.config(text="Ошибка: введите название топика!", fg="red")
        return

    try:
        admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
        topic_list = [NewTopic(name=topic_name, num_partitions=1, replication_factor=1)]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        update_topic_menu()  # Обновляем список топиков
        status_label.config(text=f"Топик '{topic_name}' создан!", fg="green")
    except Exception as e:
        status_label.config(text=f"Ошибка при создании топика: {e}", fg="red")

# Функция удаления топика
def delete_topic():
    selected_topic = topic_var.get()
    if not selected_topic:
        status_label.config(text="Ошибка: выберите топик для удаления!", fg="red")
        return

    try:
        admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
        admin_client.delete_topics([selected_topic])
        update_topic_menu()  # Обновляем список топиков
        status_label.config(text=f"Топик '{selected_topic}' удалён!", fg="green")
    except Exception as e:
        status_label.config(text=f"Ошибка при удалении топика: {e}", fg="red")

# Функция отправки сообщения
def send_message():
    message_text = entry.get().strip()
    selected_topic = topic_var.get()

    if not message_text:
        status_label.config(text="Ошибка: сообщение пустое!", fg="red")
        return

    try:
        producer.send(selected_topic, value=message_text.encode('utf-8'))
        producer.flush()
        status_label.config(text="Сообщение отправлено!", fg="green")
        entry.delete(0, tk.END)
    except Exception as e:
        status_label.config(text=f"Ошибка при отправке сообщения: {e}", fg="red")

# Инициализация Kafka Producer
try:
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
except Exception as e:
    producer = None
    print(f"Ошибка инициализации Kafka Producer: {e}")

# Инициализация списка топиков
topics = get_topics()

# Создание GUI с Tkinter
root = tk.Tk()
root.title("Kafka GUI Producer")
root.geometry("500x350")

# Поле для ввода нового топика
tk.Label(root, text="Название нового топика:").pack(pady=5)
entry_topic = tk.Entry(root, width=50)
entry_topic.pack(pady=5)
create_topic_button = tk.Button(root, text="Создать топик", command=create_topic)
create_topic_button.pack(pady=5)

# Выбор топика
tk.Label(root, text="Выберите топик:").pack(pady=5)
topic_var = tk.StringVar(root)
topic_var.set(topics[0] if topics else DEFAULT_TOPIC)
topic_menu = tk.OptionMenu(root, topic_var, *topics)
topic_menu.pack(pady=5)

# Кнопка удаления топика
delete_topic_button = tk.Button(root, text="Удалить топик", command=delete_topic, fg="red")
delete_topic_button.pack(pady=5)

# Поле для ввода сообщения
tk.Label(root, text="Введите сообщение для Kafka:").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# Кнопка отправки сообщения
send_button = tk.Button(root, text="Отправить сообщение", command=send_message)
send_button.pack(pady=10)

# Статус
status_label = tk.Label(root, text="", fg="black")
status_label.pack()

# Запуск Tkinter GUI
root.mainloop()
