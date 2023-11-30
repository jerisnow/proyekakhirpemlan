import io
import socket
import threading
import pandas as pd
import os

class BankServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.filename = 'new-bank2.csv'
        self.create_csv_file()

    def create_csv_file(self):
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=["Nama", "Umur", "Pekerjaan", "No_Telp", "Status", "Alamat"])
            df.to_csv(self.filename, index=False)

    def import_data_from_csv(self):
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            return df
        return pd.DataFrame()

    def export_data_to_csv(self, data):
        data.to_csv(self.filename, index=False)

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode()

            if not data:
                break

            if data == "display_data":
                self.send_data_to_client(client_socket)
            elif data == "add_data":
                self.receive_data_and_update("add_data", client_socket)
            elif data == "update_data":
                self.receive_data_and_update("update_data", client_socket)
            elif data == "delete_data":
                self.receive_data_and_update("delete_data", client_socket)
            elif data.startswith("search_data"):
                search_term = data.split(":")[1]
                self.send_search_results_to_client(client_socket, search_term)
            elif data == "exit_app":
                break

        client_socket.close()

    def send_data_to_client(self, client_socket):
        data = self.import_data_from_csv()
        serialized_data = data.to_csv(index=False).encode()
        client_socket.send(serialized_data)

    # Inside the BankServer class
    # Modify the receive_data_and_update method
    def receive_data_and_update(self, operation, client_socket):
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode()

            # Debugging: Print received data
            print(f"Received data: {data}")

            # Assuming columns is defined somewhere in your code
            columns = ["Nama", "Umur", "Pekerjaan", "No_Telp", "Status", "Alamat"]

            # Split data and create DataFrame
            split_data = data.split(',')

            # Check if the number of columns matches and there is non-empty data
            if len(split_data) == len(columns) and any(split_data):
                received_data = pd.DataFrame([split_data], columns=columns)

                # Perform the requested operation
                if operation == "add_data":
                    self.add_data_to_dataframe(received_data)
            else:
                print("Invalid data received.")

        except Exception as e:
            print(f'Error during data reception and update: {e}')

    # Modify the add_data_to_dataframe method
    def add_data_to_dataframe(self, data):
        # Menambahkan data baru ke DataFrame
        current_data = self.import_data_from_csv()
        updated_data = pd.concat([current_data, data], ignore_index=True)

        # Menyimpan DataFrame ke file CSV
        self.export_data_to_csv(updated_data)


    def send_search_results_to_client(self, client_socket, search_term):
        data = self.import_data_from_csv()

        if search_term == "all":
            search_results = data
        else:
            search_results = data[data['Nama'].str.contains(search_term, case=False)]

        serialized_results = search_results.to_csv(index=False).encode()
        client_socket.send(serialized_results)

    def start(self):
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Accepted connection from {client_address}")

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    host = "10.200.145.246"
    port = 5010
    server = BankServer(host, port)
    server.start()
