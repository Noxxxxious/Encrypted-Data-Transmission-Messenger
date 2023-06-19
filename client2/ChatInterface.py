import tkinter as tk
from Message import Message
from threading import Thread


class ChatInterface(tk.Tk):
    def __init__(self, send_callback, connect_callback):
        super().__init__()
        self.title("Safe messenger")
        self.font = ("Courier new", 12)

        self.message_listbox = tk.Listbox(self, height=15, width=50)
        self.message_listbox.config(font=self.font)
        self.message_listbox.pack()

        self.message_entry = tk.Entry(self, width=50)
        self.message_entry.config(font=self.font)
        self.message_entry.insert(0, "Establish connection to start texting")
        self.message_entry.bind("<Return>", self.send_message)
        self.message_entry.config(state="disabled")
        self.message_entry.pack()

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(side="left")
        self.send_button.config(state="disabled", font=self.font)

        self.connect_button = tk.Button(self, text="Connect", command=self.connect)
        self.connect_button.pack(side="right")
        self.connect_button.config(font=self.font)

        self.cipher_selection = tk.StringVar()
        self.cipher_selection.set("ECB")
        self.ecb_radio = tk.Radiobutton(self, text="ECB", variable=self.cipher_selection, value="ECB")
        self.ecb_radio.pack()
        self.ecb_radio.config(font=self.font)
        self.cbc_radio = tk.Radiobutton(self, text="CBC", variable=self.cipher_selection, value="CBC")
        self.cbc_radio.pack()
        self.cbc_radio.config(font=self.font)

        self.send_callback = send_callback
        self.connect_callback = connect_callback

    def send_message(self, event=None):
        message_text = self.message_entry.get()
        message = Message(message_text, "text", self.cipher_selection.get())
        self.send_callback(message)
        self.message_entry.delete(0, tk.END)

    def connect(self):
        if self.connect_button["state"] == "normal":
            self.connect_button["state"] = "disabled"
            t = Thread(target=self.connect_callback)
            t.start()

    def connection_successful(self):
        self.message_entry.config(state="normal")
        self.send_button.config(state="normal")
        self.message_entry.delete(0, tk.END)

    def close_window(self):
        self.destroy()
        exit()
