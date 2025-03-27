import socket
from threading import Thread
import pickle
import pygame
import csv


class Carte:
    def __init__(self,emplacement,imagepath,camps=None,hiden=False):
        self.emplacement = emplacement
        self.img = pygame.image.load(self.imagepath)
        self.dosimg = pygame.image.load('data/dos/DosPioche.png')
        self.imagepath = imagepath
        self.camps = camps
        self.hiden = hiden
    def draw(self,surface):
        if not self.hiden:
            surface.blit(self.img,(self.emplacement[0],self.emplacement[1]))
        else:
            surface.blit(self.dosimg,(self.emplacement[0],self.emplacement[1]))
            







class Client:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
        self.client_data = {
            'ip': '127.0.0.1',
            'port': 5555,
            "name": None,
            'player': None
        }
    def send(self, message):
        self.client.send(pickle.dumps(message))
    def receve(self):
        while True:
            message = pickle.loads(self.client.recv(2048))
            if isinstance(message, dict):
                if message['type'] == 'Start':
                    message["data"] = input('Entrez votre nom : ')
                    message['resolution'] = (win_w,win_h)
                    self.client_data['name'] = message["data"]
                    self.client_data['player'] = message["player"]
                
                    self.send(message)
            else:
                print(message)
            
connected = False

pygame.init()
window = pygame.display.set_mode((0,0),pygame.RESIZABLE)
win_w,win_h = pygame.display.get_window_size()


while not connected:
    try:
        client = Client('127.0.0.1', 5555)
        connected = True
    except:
        pass


Thread(target=client.receve).start()
while True:
    message = input('> ')
    if message != '':
        client.send(message)

