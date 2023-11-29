import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket

class BankMarketingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Data Nasabah Bank ABC")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        pastel_blue = "#add8e6"
        self.root.configure(bg=pastel_blue)
    
        # Nama file CSV untuk menyimpan data
        self.filename = 'new-bank.csv'

        # Buat file CSV jika tidak ada
        self.create_csv_file()

        # Fungsi untuk mengimpor data dari file CSV
        self.data = self.import_data_from_csv()

        # Inisialisasi login
        self.login_frame()

    def add_data_to_server(self, entries):
        try:
            # your existing code to get values from entries

            # Connect to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((socket.gethostname(), 5005))

                # Send the command to the server
                s.sendall(b'add_data')

                # Send the data to the server
                s.sendall(data.encode())

                # Receive and print the response from the server
                response = s.recv(1024)
                print(response.decode())

        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Failed to add data to the server.")

    # Other methods...

if __name__ == "__main__":
    root = tk.Tk()
    app = BankMarketingGUI(root)
    root.mainloop()
