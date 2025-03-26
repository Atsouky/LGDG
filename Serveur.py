import socket
from threading import Thread
import pickle
import csv



class Server:
    clients = []
    def __init__(self, ip, port):
        self.serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur.bind((ip, port))
        self.serveur.listen(2)
        print('Server online')
    
    def listen(self):
        
        while True:
            client, address = self.serveur.accept()
            Client = {'ip':address, 'client':client , 'name':None}
            self.clients.append(Client)
            Thread(target=self.handle_new_client, args=(Client, )).start()
    
    def broadcast(self, message):
        for client in self.clients:
                client['client'].send(pickle.dumps(message))
    
    def receve(self, client):
        global pioche
        while True:
            message = pickle.loads(client['client'].recv(2048))
            if message == 'q':
                self.clients.remove(client)
                break             
            elif message.split(' ')[0] == '/name':
                client['name'] = message.split(' ')[1]
            
            elif message == '¤pioche':
                message =pioche.piocher()
                self.broadcast(message)
            
            
            
            
    def handle_new_client(self, client):
        print(f'Connection from {client["ip"]}')
        Thread(target=self.receve, args=(client, )).start()
        self.broadcast(f'{client["ip"]} connected')


import pygame
from random import shuffle




class Card:
    def __init__(self, x ,y, name, image, pv, mp, pa, pw, classe, lien=[], camps=None, pw_value=None,is_Stratège=False, is_hiden=True, scale=0.25):
        self.data = {
            'x': x,
            'y': y,
            'name': name,
            'image': image,
            'pv': pv,
            'mp': mp,
            'pa': pa,
            'pw': pw,
            'classe': classe,
            'lien': lien,    
            'camps': camps,
            'pw_value': pw_value,
            'is_Stratège': is_Stratège,
            'is_hiden': is_hiden ,   
            'scale': scale
        }
                    
class Pioche:
    def __init__(self, cartes,scale,win_w):
        self.scale = scale
        self.win_w = win_w
        self.cartes: list = cartes
        self.mélanger()
        self.x = win_w//2
        self.y = 0
        self.image = pygame.image.load('data/dos/DosPioche.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale//1.5, self.image.get_height() * scale//1.5))
        self.collision = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
    def piocher(self):
        if self.cartes:
            carte = self.cartes.pop()
            carte.x, carte.y=self.win_w//2+carte.width+carte.width//2,0
            return carte
        print("La pioche est vide")
        return None

    def mélanger(self):
        shuffle(self.cartes)
        
    def draw(self, surface):
        surface.blit(self.image, (self.x,self.y))
        
    def handle_events(self, surface, event):
        if self.collision.collidepoint(pygame.mouse.get_pos()):
            self.draw(surface)
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

def load_carde(scale):
    cartes = []
    with open('DataPerso.csv', 'r') as file:
        reader = csv.reader(file, skipinitialspace=True,delimiter=',', quoting=csv.QUOTE_NONE)
        for id,row in enumerate(reader):
            if id == 0 or id == 1 or row == [] :
                continue
            else:
                cartes.append(Card(0,0,row[0],row[1],row[2],row[3],row[4],row[5],row[6],scale = scale))
    return cartes






def main():
    global pioche
    scale = 0.10
    cartes = load_carde(scale)
    win_w = 1366
    pioche = Pioche(cartes,scale,win_w)

    server = Server('127.0.0.1', 5555)
    Thread(target=server.listen).start()
    print('server on')
    
    
if __name__ == '__main__':
    main()

"""if __name__ == '__main__':
    server = Server('127.0.0.1', 5555)
    Thread(target=server.listen).start()
    while True:
        message = input('> ')
        if message != '':
            message = 'Admin : '+message
            server.broadcast(message)"""