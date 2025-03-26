import socket
from threading import Thread
import pickle
import csv

nb_joueurs = 0


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
            Client = {'ip':address, 'client':client , 'name':None, 'scale': None, 'isJoueur': None }
            self.clients.append(Client)
            Thread(target=self.handle_new_client, args=(Client, )).start()
    
    def broadcast(self, message):
        for client in self.clients:
                client['client'].send(pickle.dumps(message))
                
    def broadcast_to(self, message, cliente):
        
        for client in self.clients:
            if client['ip'] == cliente['ip']:
                message.data['camps'] = client['isJoueur']
                message.data['is_hiden'] = False
                client['client'].send(pickle.dumps(message))
                
            else:
                message.data['is_hiden'] = True
                client['client'].send(pickle.dumps(message))
            
    
    def Send(self, message, client):
        client['client'].send(pickle.dumps(message))
    def receve(self, client):
        global pioche, nb_joueurs
        while True:
            message = pickle.loads(client['client'].recv(2048))
            
            if message == 'q':
                self.Send('q',client)
                nb_joueurs -= 1
                self.clients.remove(client)
                break
            
            elif message[0] == '?':
                client['scale'] = float(message.split(' ')[1])
                print(client['scale'])  
                
            elif message[0] == '¤':
                
                if message.split(' ')[0] == '¤pioche':
                    print(message)
                    messages = pioche.piocher()
                    for i in self.clients:
                        if str(i['isJoueur']) == message.split(' ')[1]:
                            self.broadcast_to(messages,i)
                            
                if isinstance(message, dict):
                    if message["type"] == 'move':
                        name , x, y = message['carte'].name, message['carte'].x ,message['carte'].y
                        carte_piocher[name].x , carte_piocher[name].y = x , y
                        di={
                            'carte': carte_piocher[name],
                            'type': 'move',
                            'isJoueur': message['isJoueur']
                        }
                        self.broadcast(di)
                    
            
            
                   
            elif message.split(' ')[0] == '/name':
                client['name'] = message.split(' ')[1]
            
            
            
            
            
            
            
    def handle_new_client(self, client):
        global nb_joueurs
        print(f'Connection from {client["ip"]}')
        
        self.Send('?scale',client)
        while client['scale'] == None or client['scale'] == '':
            message = pickle.loads(client['client'].recv(2048))
            client['scale'] = message
        nb_joueurs += 1
        client['isJoueur'] = nb_joueurs
        self.Send('¤j '+str(nb_joueurs),client)
        Thread(target=self.receve, args=(client, )).start()
        self.broadcast(f'{client["ip"]} connected')


import pygame
from random import shuffle




class Packet_carte:
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
    def __repr__(self):
        return 'Packet carte send or receive '
                    
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
            carte.x, carte.y=self.win_w//2+200,0
            carte_piocher[str(carte.data['name'])] = carte
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
                cartes.append(Packet_carte(0,0,row[0],row[1],row[2],row[3],row[4],row[5],row[6],scale = scale))
    return cartes



carte_piocher = {}

from pyngrok import ngrok
def main():
    global pioche
    
    scale = 0.10
    cartes = load_carde(scale)
    win_w = 1366
    pioche = Pioche(cartes,scale,win_w)
    localhost = '127.0.0.1'
    server = Server(localhost, 5555)
    Thread(target=server.listen).start()
    
    
    
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