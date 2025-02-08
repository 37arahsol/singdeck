import asyncio
import tkinter as tk
from tkinter import ttk
from network import start_server, start_client

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sync Screen App")
        self.geometry("400x300")
        self.configure(bg="#2b2b2b")

        self.create_widgets()

    def create_widgets(self):
        self.style = ttk.Style(self)
        self.style.configure("TLabel", background="#2b2b2b", foreground="#ffffff", font=("Arial", 14))
        self.style.configure("TButton", background="#3c3c3c", foreground="#ffffff", borderwidth=0, padding=10, font=("Arial", 12))
        self.style.map("TButton", background=[("active", "#4c4c4c")])

        self.label = ttk.Label(self, text="Выберите режим работы:")
        self.label.pack(pady=20)

        self.server_button = ttk.Button(self, text="Запустить сервер", command=self.start_server_mode)
        self.server_button.pack(pady=10)

        self.client_button = ttk.Button(self, text="Подключиться к серверу", command=self.start_client_mode)
        self.client_button.pack(pady=10)

        self.status_label = ttk.Label(self, text="")
        self.status_label.pack(pady=20)

    def start_server_mode(self):
        self.status_label.config(text="Сервер активирован. Ждем подключение парного устройства...")
        asyncio.create_task(start_server(self))

    def start_client_mode(self):
        self.status_label.config(text="Подключено!")
        asyncio.create_task(start_client(self))

if __name__ == "__main__":
    app = App()
    app.mainloop()
