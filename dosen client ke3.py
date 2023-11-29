import socket
import logging
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
from pandastable import Table

class BankClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Data Nasabah Bank ABC")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#add8e6")

        # Calculate the center position of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 450
        window_height = 400
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

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
        ttk.Button(self.root, text="Tambah Data", command=self.add_data(self, entries)).pack(side=tk.TOP, anchor=tk.CENTER, pady=10, padx=70, fill=tk.X)
        ttk.Button(self.root, text="Update Data", command=self.update_data).pack(pady=10)
        ttk.Button(self.root, text="Delete Data", command=self.delete_data).pack(pady=10)
        ttk.Button(self.root, text="Search Data", command=self.search_data).pack(pady=10)
        ttk.Button(self.root, text="Help", command=self.show_help).pack(pady=10)
        ttk.Button(self.root, text="Exit App", command=self.exit_app).pack(pady=10)

        self.root.geometry("450x400")  # Set the size and position of the window

    def display_data(self):
        self.send_data_to_server("display_data")
        data = self.receive_data_from_server()
        self.show_data_table(data)

    def add_data(self, entries):
        # Mendapatkan nilai dari entry
        values = [entry.get() for entry in entries]

        # Mengirim perintah ke server untuk menambahkan data baru
        self.send_data_to_server("add_data")
    
        # Mengirim data baru ke server
        new_data = pd.DataFrame([values], columns=self.data.columns)
        self.send_data_to_server(new_data.to_json(orient='split'))

        # Menampilkan pesan info (Opsional, tergantung kebutuhan)
        messagebox.showinfo("Tambah Data", "Permintaan penambahan data telah dikirim ke server.")


    def update_data(self):
        # Implement the update data functionality
        pass

    def delete_data(self):
        # Implement the delete data functionality
        pass

    def search_data(self):
        # Implement the search data functionality
        pass

    def show_help(self):
        # Membuat jendela baru untuk menampilkan pusat bantuan
        new_window = tk.Toplevel(self.root)
        new_window.title("Pusat Bantuan")
        help_text = (
            "Pilihan 'Tampilkan Data' akan menampilkan seluruh data nasabah yang ada pada database.\n"
            "Pilihan 'Tambah Data' akan memberi akses kepada admin untuk menambah data nasabah pada database.\n"
            "Pilihan 'Perbarui Data' akan memberi akses kepada admin untuk memperbarui data nasabah yang sudah ada.\n"
            "Pilihan 'Hapus Data' akan memberi akses kepada admin untuk menghapus data nasabah pada database.\n"
            "Pilihan 'Cari Data' akan memberi akses kepada admin untuk mencari data nasabah sesuai nama, umur, dan pekerjaan.\n"
            "Pilihan 'Help' akan menampilkan pusat bantuan.\n"
            "Pilihan 'Keluar' akan keluar dari aplikasi."
        )
        # Membuat widget LabelFrame untuk menampilkan teks bantuan dengan lebih baik
        help_frame = ttk.LabelFrame(new_window, text="Help", padding=(10, 10))
        help_frame.pack(padx=20, pady=20)

        # Membuat widget Label untuk menampilkan teks bantuan
        help_label = ttk.Label(help_frame, text=help_text, justify=tk.LEFT, font=("Helvetica", 10))
        help_label.grid(row=0, column=0, padx=10, pady=10)


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
