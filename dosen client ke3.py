import socket
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from pandastable import Table

class BankClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Data Nasabah Bank ABC")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        pastel_blue = "#add8e6"
        self.root.configure(bg=pastel_blue)

        self.host = "10.200.18.137"
        self.port = 5005

        self.create_connection()

        self.setup_gui()

    def create_connection(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_data_to_server(self, data):
        self.client_socket.send(data.encode())

    def receive_data_from_server(self):
        data = self.client_socket.recv(1024).decode()
        return pd.read_json(data, orient='split')

    def setup_gui(self):
        ttk.Button(self.root, text="Display Data", command=self.display_data).pack(pady=10)
        ttk.Button(self.root, text="Add Data", command=self.add_data).pack(pady=10)
        ttk.Button(self.root, text="Update Data", command=self.update_data).pack(pady=10)
        ttk.Button(self.root, text="Delete Data", command=self.delete_data).pack(pady=10)
        ttk.Button(self.root, text="Search Data", command=self.search_data).pack(pady=10)
        ttk.Button(self.root, text="Exit App", command=self.exit_app).pack(pady=10)

    def display_data(self):
        self.send_data_to_server("display_data")
        data = self.receive_data_from_server()
        self.show_data_table(data)

    def add_data(self):
        # Implement the add data functionality
        pass

    def update_data(self):
        # Implement the update data functionality
        pass

    def delete_data(self):
        # Implement the delete data functionality
        pass

    def search_data(self):
        # Implement the search data functionality
        pass

    def exit_app(self):
        self.send_data_to_server("exit_app")
        self.root.destroy()

    def show_data_table(self, data):
        new_window = tk.Toplevel(self.root)
        new_window.title("Data Nasabah")

        frame = ttk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)
        pt = Table(frame, dataframe=data, showtoolbar=False, showstatusbar=True, editable=False)
        pt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankClientGUI(root)
    root.mainloop()
