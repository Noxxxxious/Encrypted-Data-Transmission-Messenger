import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from ChatInterface import ChatInterface
from Message import Message
from rsa_funcs import *
from ecb_funcs import *
from cbc_funcs import *


class Client:
    def __init__(self, host, send_port, receive_port):
        self.interface = ChatInterface(self.send_message, self.connect)
        self.interface.protocol("WM_DELETE_WINDOW", self.close_connection)

        self.host = host
        self.send_port = send_port
        self.receive_port = receive_port

        self.receive_socket = socket(AF_INET, SOCK_STREAM)
        self.receive_socket.bind((self.host, self.receive_port))
        self.receive_socket.listen(1)

        self.public_key, self.private_key = generate_key_pair()
        self.peer_public_key = None
        self.session_key = None

        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()

    def start(self):
        self.interface.mainloop()

    def connect(self):
        while self.session_key is None:
            self.send_message(Message(self.public_key, "public-key"))
        self.interface.connection_successful()

    def receive_messages(self):
        while True:
            try:
                conn, addr = self.receive_socket.accept()
                message = Message.from_json(conn.recv(1024).decode("utf8"))
                if message.msg_type == "public-key":
                    self.peer_public_key = message.text
                elif message.msg_type == "session-key":
                    self.session_key = rsa_decode(message.text, self.private_key).encode()
                else:
                    if message.cipher_type == "ECB":
                        message.text = ecb_decrypt(message.text, self.session_key)
                    elif message.cipher_type == "CBC":
                        message.text = base64.b64decode(message.text.encode())
                        message.text = cbc_decrypt(message.text, self.session_key)
                    self.interface.message_listbox.insert(tk.END, "Stranger: " + message.text)
                conn.close()
            except OSError:
                break

    def send_message(self, message):
        send_socket = socket(AF_INET, SOCK_STREAM)
        try:
            send_socket.connect((self.host, self.send_port))
            if message.msg_type == "text":
                self.interface.message_listbox.insert(tk.END, "You: " + message.text)
            if message.cipher_type == "ECB":
                message.text = ecb_encrypt(message.text, self.session_key)
                message.text = base64.b64encode(message.text).decode()
            elif message.cipher_type == "CBC":
                message.text = cbc_encrypt(message.text, self.session_key)
                message.text = base64.b64encode(message.text).decode()
            send_socket.send(bytes(message.to_json(), "utf8"))
        except ConnectionRefusedError:
            print("Waiting for connection")

    def close_connection(self):
        self.receive_socket.close()
        self.interface.close_window()
