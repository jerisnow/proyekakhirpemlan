import socket
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading


class BankClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        self.root = tk.Tk()
        self.root.title("Bank Client")
        self.root.geometry("300x200")

        self.setup_gui()

    def setup_gui(self):
        ttk.Button(self.root, text="Display Data", command=self.display_data).pack(pady=10)
        ttk.Button(self.root, text="Add Data", command=self.add_data).pack(pady=10)
        ttk.Button(self.root, text="Exit", command=self.exit_app).pack(pady=10)

    def send_request(self, request):
        self.client_socket.send(request.encode())
        response = self.client_socket.recv(1024).decode()
        return response

    def display_data(self):
        response = self.send_request("DISPLAY_DATA")
        messagebox.showinfo("Data Display", response)

    def add_data(self):
        response = self.send_request("ADD_DATA")
        messagebox.showinfo("Add Data", response)

    def exit_app(self):
        self.client_socket.close()
        self.root.destroy()


if __name__ == '__main__':
    client = BankClient("10.200.18.137", 5005)
    client.root.mainloop()
