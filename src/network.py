import socket
import threading
import json

class NetworkManager:
    def __init__(self, host, port, is_server=False):
        self.host = host
        self.port = int(port)
        self.is_server = is_server
        self.socket = None
        if self.is_server:
            self._start_server()
        else:
            self._connect_to_server()

    def _start_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        threading.Thread(target=self._accept_clients, daemon=True).start()
        self.clients = []

    def _accept_clients(self):
        while True:
            client_socket, addr = self.socket.accept()
            print(f"Client connected: {addr}")
            self.clients.append(client_socket)
            threading.Thread(target=self._handle_client, args=(client_socket,), daemon=True).start()

    def _handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode('utf-8'))
                print("received:", message)
            except Exception as e:
                print("Error while receiving data:", e)
                break
        client_socket.close()

    def _connect_to_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        threading.Thread(target=self._receive_messages, daemon=True).start()

    def _receive_messages(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode('utf-8'))
                print("Received from server:", message)
            except Exception as e:
                print("Error:", e)
                break

    def send_message(self, message):
        try:
            msg_str = json.dumps(message)
            if self.is_server:
                for client in self.clients:
                    client.send(msg_str.encode('utf-8'))
            else:
                self.socket.send(msg_str.encode('utf-8'))
        except Exception as e:
            print("Error while sending:", e)

if __name__ == "__main__":
    NM = NetworkManager("192.168.100.9", 9999, is_server=True)
    while True:
        continue
