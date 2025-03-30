import socket
from threading import Thread
import pickle,csv
import pygame
from win32api import GetSystemMetrics
win_w = GetSystemMetrics(0)
win_h = GetSystemMetrics(1)

class Carte:
    def __init__(self,x,y, name, image, stats, classes,camps=None, hiden=False, is_strategy=False):
        self.x = x
        self.y = y
        self.name = name
        self.image = image
        self.classes = classes
        self.pv, self.pm, self.pa, self.pw = stats
        self.camps = camps
        self.hiden = hiden
        self.is_strategy = is_strategy
        self.collision = None

        
        
    def get_all_info(self):
        return {
            'x': self.x,
            'y': self.y,
            'name': self.name,
            'image': self.image,
            'stats': (self.pv, self.pm, self.pa, self.pw),
            'camps': self.camps,
            'hiden': None
        }



    
    
class Pioche_server:
    def __init__(self):
        self.cartes = self.load_cartes()
        self.mélanger()
    
    def mélanger(self):
        import random
        random.shuffle(self.cartes)
        
    def piocher(self):
        if self.cartes == []:
            return None
        return self.cartes.pop()

    def load_cartes(self):
        cartes = []
        with open('DataPerso.csv', 'r') as file:
            reader = csv.reader(file, skipinitialspace=True,delimiter=',', quoting=csv.QUOTE_NONE)
            for id,row in enumerate(reader):
                if id == 0 or id == 1 or row == [] :
                    continue
                else:
                    cartes.append(Carte(0,row[0],row[1],(row[2],row[3],row[4],row[5]),row[6]))
        return cartes

class Players:
    def __init__(self, player1, player2):
        
        
        self.pioche = Pioche_server()    
        
        pl= [player1,player2]
        players = {'1':None,'2':None}
        for i in pl:
            if i['player'] == 1:
                players['1'] = i
            else:
                players['2'] = i
            
        
        
        
        
        
        self.img = pygame.image.load('data/image/Ariane.png')
        self.img = pygame.transform.scale(self.img, (self.img.get_width() * 0.10, self.img.get_height() * 0.10))
        w,h = self.img.get_width(),self.img.get_height()  
          
        cx,cy = win_w-w-115, win_h-h
        
        self.emplacement2 = (cx-w-20, win_h-h, w, h)
        self.emplacement1 = (cx, cy, w, h)
        self.emplacement3 = (cx-w*2-40, win_h-h, w, h)
        self.emplacement4 = (cx-w//2-10, win_h-h*2-15, w, h)
        self.emplacement5 = (cx-w//2-w-30, win_h-h*2-15, w, h)
        self.emplacement6 = (cx-w-20, win_h-h*3-30, w, h)

        self.emplacements = [self.emplacement1, self.emplacement2, self.emplacement3, self.emplacement4, self.emplacement5, self.emplacement6]

        cx,cy = win_w-w-115, 20
        self.emplacement1e = (cx, cy, w, h)
        self.emplacement2e = (cx-w-20, cy, w, h)
        self.emplacement3e = (cx-w*2-40, cy, w, h)
        self.emplacement4e = (cx-w//2-10, cy+h+15, w, h)
        self.emplacement5e = (cx-w//2-w-30, cy+h+15, w, h)
        self.emplacement6e = (cx-w-20, cy+h*2+30, w, h)

        self.emplacementsE = [self.emplacement1e, self.emplacement2e, self.emplacement3e, self.emplacement4e, self.emplacement5e, self.emplacement6e]
        
        dx,dy = cx-w*4, win_h-h
        s=20
        self.deck1 = (dx, dy, w, h)
        self.deck2 = (dx-w-s, dy, w, h)
        self.deck3 = (dx-w*2-s*2, dy, w, h)
        self.deck4 = (dx-w*3-s*3, dy, w, h)
        self.deck5 = (dx-w*4-s*4, dy, w, h)
        self.deck6 = (dx-w*5-s*5, dy, w, h)
        self.deck7 = (dx-w*6-s*6, dy, w, h)
        
        self.decks = [self.deck1, self.deck2, self.deck3, self.deck4, self.deck5, self.deck6, self.deck7]
        
        dx,dy = cx-w*4, 20
        s=3
        self.decke1 = (dx, dy, w, h)
        self.decke2 = (dx-w-s, dy, w, h)
        self.decke3 = (dx-w*2-s*2, dy, w, h)
        self.decke4 = (dx-w*3-s*3, dy, w, h)
        self.decke5 = (dx-w*4-s*4, dy, w, h)
        self.decke6 = (dx-w*5-s*5, dy, w, h)
        self.decke7 = (dx-w*6-s*6, dy, w, h)
        
        self.decksE = [self.decke1, self.decke2, self.decke3, self.decke4, self.decke5, self.decke6, self.decke7]
        
        self.player1 = player1
        self.p1deck = []
        self.p1plateau = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None
        }
        self.player2 = player2
        self.p2deck = []
        self.p2plateau = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None
        }
        
    def piocher(self,Player):
        carte = self.pioche.piocher()
        if carte != None:
            if Player == 1:
                if self.p1deck<=7:
                    carte.x, carte.y = self.decks[len(self.p1deck)][0], self.decks[len(self.p1deck)][1]
                    self.p1deck.append(carte)
            else:
                if self.p2deck<=7:
                    carte.x, carte.y = self.decksE[len(self.p2deck)]
                    self.p2deck.append(carte)
    
    def update(self):
        data = {
            'p1plateau': self.p1plateau,
            'p2plateau': self.p2plateau,
            'p1deck': self.p1deck,
            'p2deck': self.p2deck
        }
        return data
        

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
            Client = {'ip':address, 'client':client , 'name':None, 'scale': None, 'player': None , 'resolution': None}
            self.clients.append(Client)
            Thread(target=self.handle_new_client, args=(Client, )).start()
    
    def broadcast(self, message):
        if isinstance(message, dict):
            if message['type'] == 'Pioche':
                client_in = message['player']
                
                for client in self.clients:
                    print(client_in, client['player'])
                    if client_in == client['player']:
                        message['data']['hiden'] = False
                        message['data']['camps'] = client_in
                        client['client'].send(pickle.dumps(message))
                    elif client_in != client['player']:
                        
                        message['data']['hiden'] = True
                        message['data']['camps'] = client_in
                        client['client'].send(pickle.dumps(message))
                    else:
                        print("error pioche")
        else:
            for client in self.clients:
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
            
            elif isinstance(message, dict):
                
                if message["type"] == 'Start':
                    client["name"] = message["name"]
                    client['resolution'] = message['resolution']
                    client['player'] = message['player']
                
                elif message["type"] == 'Pioche':
                    carte = self.pioche.piocher()
                    if carte != None:
                        pass
                        
            
            else:
                self.broadcast(message)

    def handle_new_client(self, client):
        global nb_joueurs
        print(f'Connection from {client["ip"]}')
        nb_joueurs += 1
        self.Send({'type':'Start', 'player':nb_joueurs}, client)
        Thread(target=self.receve, args=(client, )).start()
        self.broadcast({'type':'info', 'data':client["ip"]})
        if nb_joueurs == 2:
            Js = Players(self.clients[0], self.clients[1])
            

Js = None
 
server = Server('127.0.0.1', 5555)
Thread(target=server.listen).start()

while True:
    message = input('> ')
    if message != '':
        if message == 'q':
            server.broadcast(message)