import socket
import threading
import tkinter

# Создаем окно сервера
window = tkinter.Tk()
window.title("Chat Server")

# Создаем текстовое поле для отображения информации о подключениях
connections_text = tkinter.Text(window)
connections_text.pack()

# Создаем сокет и начинаем прослушивание входящих подключений
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.110', 55555))
server_socket.listen()

# Список для хранения соединений с клиентами
client_sockets = []

# Функция для обработки входящих подключений
def accept_connections():
    while True:
        # Принимаем входящее соединение
        client_socket, address = server_socket.accept()

        # Добавляем соединение в список
        client_sockets.append(client_socket)

        # Получаем никнейм клиента
        nickname = client_socket.recv(1024).decode()

        # Отображаем информацию о новом подключении
        connections_text.insert(tkinter.END, f"{nickname} has joined the chat\n")

        # Запускаем обработку входящих сообщений от клиента в отдельном потоке
        thread = threading.Thread(target=handle_client_messages, args=(client_socket, nickname))
        thread.start()

# Функция для обработки входящих сообщений от клиента
def handle_client_messages(client_socket, nickname):
    while True:
        try:
            # Получаем сообщение от клиента
            message = client_socket.recv(1024).decode()

            # Отправляем сообщение всем клиентам, кроме отправителя
            for socket in client_sockets:
                if socket != client_socket:
                    socket.sendall(f"{nickname}: {message}".encode())
        except:
            # Если возникает ошибка, удаляем соединение из списка и закрываем его
            client_sockets.remove(client_socket)
            connections_text.insert(tkinter.END, f"{nickname} has left the chat\n")
            client_socket.close()
            break

# Запускаем обработку входящих подключений в отдельном потоке
thread = threading.Thread(target=accept_connections)
thread.start()

# Запускаем цикл обработки событий в графическом интерфейсе
window.mainloop()