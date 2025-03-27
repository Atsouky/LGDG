import socket
from threading import Thread
import pickle
import pygame
import csv


class Carte:
    def __init__(self,emplacement,nom,imagepath,stats,camps=None,hiden=False):
        self.emplacement = emplacement
        self.nom = nom
        self.pv, self.pm, self.pa, self.pw = stats
        self.img = pygame.image.load(self.imagepath)
        self.dosimg = pygame.image.load('data/dos/DosPioche.png')
        self.collision = pygame.Rect(self.emplacement[0],self.emplacement[1],self.img.get_width(),self.img.get_height())
        self.imagepath = imagepath
        self.camps = camps
        self.hiden = hiden
    def draw(self,surface):
        if not self.hiden:
            surface.blit(self.img,(self.emplacement[0],self.emplacement[1]))
        else:
            surface.blit(self.dosimg,(self.emplacement[0],self.emplacement[1]))
            
    def handle_events(self):
        if self.collision.collidepoint(pygame.mouse.get_pos()):
            return True


class Pioche:
    def __init__(self,x,y):
        self.img = pygame.image.load('data/dos/DosPioche.png')
        self.collision = pygame.Rect(x,y,self.img.get_width(),self.img.get_height())
    def draw(self,surface):
        surface.blit(self.img,(self.collision.x,self.collision.y))
        if self.collision.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True




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
        global win_w, win_h
        while True:
            message = pickle.loads(self.client.recv(2048))
            if isinstance(message, dict):
                if message['type'] == 'Start':
                    self.client_data['player'] = message['player']
                    self.send({'type':'Start', 'resolution':(win_w,win_h), 'name': 'Atsouky'})
                                    
                if message['type'] == 'Pioche':
                    carte = load_cartes(message['data'])
                    in_game_cartes.append(carte)
                
            else:
                print(message)

def load_cartes(carte):
    return Carte(
        carte['emplacement'],
        carte['nom'],
        carte['imagepath'],
        carte['stats'],
        carte['camps'],
        carte['hiden']
    )

            
connected = False

in_game_cartes = []

pygame.init()
window = pygame.display.set_mode((0,0),pygame.RESIZABLE)
win_w,win_h = pygame.display.get_window_size()

pioche= Pioche(win_w//2,0)

while not connected:
    try:
        client = Client('127.0.0.1', 5555)
        connected = True
    except:
        pass


Thread(target=client.receve).start()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                client.send('q')
                pygame.quit()
                quit()
            elif event.key == pygame.K_RETURN:
                message = input('Entrez votre message : ')
                client.send(message)
        
    
    if pioche.draw(window):
        client.send({"type": "Pioche", "data": None, "player": client.client_data['player']})
    
    for carte in in_game_cartes:
        carte.draw(window)
    
    pygame.display.update()

