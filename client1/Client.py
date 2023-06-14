import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from ChatInterface import ChatInterface
from threading import Thread


class Client:
    def __init__(self, host, send_port, receive_port):
        self.interface = ChatInterface(self.send_message)
        self.interface.protocol("WM_DELETE_WINDOW", self.close_connection)

        self.receive_socket = socket(AF_INET, SOCK_STREAM)

        self.host = host
        self.send_port = send_port
        self.receive_port = receive_port

        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()

    def start(self):
        self.interface.mainloop()

    def receive_messages(self):
        self.receive_socket.bind((self.host, self.receive_port))
        self.receive_socket.listen(1)
        while True:
            try:
                conn, addr = self.receive_socket.accept()
                message = conn.recv(1024).decode("utf8")
                print(message)
                self.interface.message_listbox.insert(tk.END, message)
                conn.close()
            except OSError:
                break

    def send_message(self, message):
        send_socket = socket(AF_INET, SOCK_STREAM)
        send_socket.connect((self.host, self.send_port))
        send_socket.send(bytes(message, "utf8"))

    def close_connection(self):
        self.receive_socket.close()
