import socket
import threading
import pandas as pd
import os

class BankServer:
    def __init__(self, host, port, filename='new-bank.csv'):
        self.host = host
        self.port = port
        self.filename = filename
        self.create_csv_file()
        self.data = self.import_data_from_csv()

    def create_csv_file(self):
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=["Nama", "Umur", "Pekerjaan", "No_Telp", "Status", "Alamat"])
            df.to_csv(self.filename, index=False)

    def import_data_from_csv(self):
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            return df
        return pd.DataFrame()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()

        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client, address = server.accept()
            print(f"Connection from {address} established.")
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client_socket):
        while True:
            request = client_socket.recv(1024).decode()

            if not request:
                print("Connection closed.")
                break

            if request == "EXPORT_DATA":
                self.export_data(client_socket)
            elif request == "IMPORT_DATA":
                self.import_data(client_socket)

    def export_data(self, client_socket):
        data_str = self.data.to_csv(index=False)
        client_socket.send(data_str.encode())

    def import_data(self, client_socket):
        received_data = client_socket.recv(1024).decode()
        df = pd.read_csv(pd.compat.StringIO(received_data))
        self.data = pd.concat([self.data, df], ignore_index=True)
        self.data.to_csv(self.filename, index=False)

        client_socket.send("Data imported successfully.".encode())

if __name__ == "__main__":
    host = "your_server_ip"  # Replace with your actual server IP
    port = 5000  # Choose a port

    server = BankServer(host, port)
    server.start_server()
