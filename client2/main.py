import tkinter as tk
from threading import Thread
from socket import AF_INET, socket, SOCK_STREAM


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf8")
            message_listbox.insert(tk.END, message)
        except OSError:
            break


def send_message(event=None):
    message = message_entry.get()
    message_entry.delete(0, tk.END)
    client_socket.send(bytes(message, "utf8"))
    if message == "{quit}":
        client_socket.close()
        root.quit()


def connect():
    global client_socket
    host = "localhost"
    port = 5500
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((host, port))

    receive_thread = Thread(target=receive_messages)
    receive_thread.start()


root = tk.Tk()
root.title("Chat App")

message_listbox = tk.Listbox(root, height=15, width=50)
message_listbox.pack()

message_entry = tk.Entry(root, width=50)
message_entry.bind("<Return>", send_message)
message_entry.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

connect_button = tk.Button(root, text="Connect", command=connect)
connect_button.pack()

root.mainloop()
