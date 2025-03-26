import socket
from threading import Thread
import pickle




class Client:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
    def send(self, message):
        self.client.send(pickle.dumps(message))
    def receve(self):
        while True:
            
            message = pickle.loads(self.client.recv(2048))
            if isinstance(message, str):
                print(message)
            else:
                print(message)
            
        
  
"""
if __name__ == '__main__':
    client = Client('127.0.0.1', 5555)
    Thread(target=client.receve).start()
    while True:
        message = input('> ')
        if message != '':
            client.send(message)"""
    