"""
Quoridor Online
Quentin Deschamps, 2020
"""
import socket
import pickle


class Network:
    """Manage communication between client and server"""
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)

    def connect(self):
        """Connect to the server"""
        try:
            self.client.connect(self.addr)
        except socket.error as e:
            print(e)

    def recv(self):
        """Receive data from server"""
        try:
            return self.client.recv(2048).decode().split(';')
        except socket.error as e:
            print(e)

    def send(self, data):
        """Send data to server"""
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            print(e)

    def get_game(self):
        """Get the game"""
        return pickle.loads(self.client.recv(2048))
