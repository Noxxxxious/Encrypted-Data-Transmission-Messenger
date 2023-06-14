import tkinter as tk


class ChatInterface(tk.Tk):
    def __init__(self, send_callback):
        super().__init__()
        self.title("Chat App")

        self.message_listbox = tk.Listbox(self, height=15, width=50)
        self.message_listbox.pack()

        self.message_entry = tk.Entry(self, width=50)
        self.message_entry.bind("<Return>", self.send_message)
        self.message_entry.pack()

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack()

        self.send_callback = send_callback

    def send_message(self, event=None):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        self.send_callback(message)
        if message == "{quit}":
            self.quit()
