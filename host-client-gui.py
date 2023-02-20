import socket
import threading
import tkinter

# Константы для настройки подключения
HOST = '127.0.0.1'
PORT = 55555

# Создание клиентского сокета и подключение к серверу
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Предварительно запросить имя пользователя, которое будет использоваться в чате
nickname = input("Введите ваш никнейм: ")

# Отправить имя пользователя на сервер
client_socket.send(nickname.encode('utf-8'))


def receive_message():
    """
    Функция для получения сообщений от сервера
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'NICK':
                # Получить никнейм пользователя и отправить его на сервер
                client_socket.send(nickname.encode('utf-8'))
            else:
                # Отобразить сообщение в списке сообщений с никнеймом пользователя
                message_listbox.insert(tkinter.END, message)
        except OSError:
            break


def send_message():
    """
    Функция для отправки сообщений на сервер
    """
    message = message_entry.get()
    message_entry.delete(0, tkinter.END)
    client_socket.send(f'{nickname}: {message}'.encode('utf-8'))


# Создание графического интерфейса
root = tkinter.Tk()
root.title("Чат")

# Создание фрейма для сообщений
message_frame = tkinter.Frame(root)
message_scrollbar = tkinter.Scrollbar(message_frame)
message_listbox = tkinter.Listbox(
    message_frame,
    height=15,
    width=50,
    yscrollcommand=message_scrollbar.set
)
message_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
message_listbox.pack()
message_frame.pack()

# Создание фрейма для ввода сообщений
input_frame = tkinter.Frame(root)
message_entry = tkinter.Entry(input_frame, width=50)
send_button = tkinter.Button(input_frame, text="Отправить", command=send_message)
message_entry.pack(side=tkinter.LEFT)
send_button.pack(side=tkinter.RIGHT)
input_frame.pack()

# Создание потока для получения сообщений от сервера
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

# Запуск графического интерфейса
root.mainloop()

# Закрытие сокета при выходе из программы
client_socket.close()
