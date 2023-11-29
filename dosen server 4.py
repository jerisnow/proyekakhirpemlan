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
        self.filename = 'server-bank.csv'
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
    
    def send_csv_to_client(self, client_socket):
        try:
            with open(self.filename, 'rb') as file:
                data = file.read()
                client_socket.send(data)
        except FileNotFoundError:
            client_socket.send(b'')

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
                self.send_search_results_to_client(client_socket, data.split(":")[1])
            elif data == "get_csv":
                self.send_csv_to_client(client_socket)
            elif data == "exit_app":
                break

        client_socket.close()

    def send_data_to_client(self, client_socket):
        data = self.import_data_from_csv()
        serialized_data = data.to_json(orient='split')
        client_socket.send(serialized_data.encode())

    def receive_data_and_update(self, operation, client_socket):
        # Receive data from the client
        data = client_socket.recv(4096).decode()
        received_data = pd.read_json(data, orient='split')

        # Perform the requested operation
        if operation == "add_data":
            current_data = self.import_data_from_csv()
            updated_data = pd.concat([current_data, received_data], ignore_index=True)
            self.export_data_to_csv(updated_data)
        elif operation == "update_data":
            # Assume the client sends both the original and updated rows
            original_data, updated_data = received_data.iloc[0], received_data.iloc[1]
            current_data = self.import_data_from_csv()
            current_data = current_data.mask(current_data.eq(original_data)).fillna(updated_data)
            self.export_data_to_csv(current_data)
        elif operation == "delete_data":
            current_data = self.import_data_from_csv()
            current_data = current_data[~current_data.isin(received_data)].dropna()
            self.export_data_to_csv(current_data)

    def send_search_results_to_client(self, client_socket, search_term):
        data = self.import_data_from_csv()

        if search_term == "all":
            search_results = data
        else:
            search_results = data[data['Nama'].str.contains(search_term, case=False)]

        serialized_results = search_results.to_json(orient='split')
        client_socket.send(serialized_results.encode())

    def start(self):
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Accepted connection from {client_address}")

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    host = "10.200.18.137"
    port = 5005
    server = BankServer(host, port)
    server.start()
