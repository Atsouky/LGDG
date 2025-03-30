import socket
from threading import Thread
import pickle,csv,pygame
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
            'classes': self.classes,
            'stats': (self.pv, self.pm, self.pa, self.pw),
            'camps': self.camps,
            'hiden': None,
            'is_strategy': self.is_strategy
        }


class Game:
    def __init__(self):
        self.all_carte = self.load_cartes()
        self.pioches = self.load_cartes()
        self.img = pygame.image.load('data/image/Ariane.png')
        self.img = pygame.transform.scale(self.img, (self.img.get_width() * 0.10, self.img.get_height() * 0.10))
        w,h = self.img.get_width(),self.img.get_height()  
          
        cx,cy = win_w-w-115, win_h-h
        cx1,cy1 = win_w-w-115, 20
        dx,dy = cx-w*4, win_h-h
        s=20
        dx1,dy1 = cx-w*4, 20
        s1=3
        self.plateau = {
            "1": {
                    'Emp': {
                        'e1': {'x':cx-w-20,'y': win_h-h, 'carte': None},
                        'e2': {'x':cx,'y': cy, 'carte': None},
                        'e3': {'x':cx-w*2-40,'y': win_h-h, 'carte': None},
                        'e4': {'x':cx-w//2-10,'y': win_h-h*2-15, 'carte': None},
                        'e5': {'x':cx-w//2-w-30,'y': win_h-h*2-15, 'carte': None},
                        'e6': {'x':cx-w-20,'y': win_h-h*3-30, 'carte': None},
                    },
                    'Deck'  : {
                        'd1': {'x':dx,'y': dy, 'carte': None},
                        'd2': {'x':dx-w-s,'y': dy, 'carte': None},
                        'd3': {'x':dx-w*2-s*2,'y': dy, 'carte': None},
                        'd4': {'x':dx-w*3-s*3,'y': dy, 'carte': None},
                        'd5': {'x':dx-w*4-s*4,'y': dy, 'carte': None},
                        'd6': {'x':dx-w*5-s*5,'y': dy, 'carte': None},
                        'd7': {'x':dx-w*6-s*6,'y': dy, 'carte': None},
                    }
                },
        
            "2": {
                    'Emp': {
                        'e1': {'x':cx1,'y': cy1, 'carte': None},
                        'e2': {'x':cx1-w-20,'y': cy1, 'carte': None},
                        'e3': {'x':cx1-w*2-40,'y': cy1, 'carte': None},
                        'e4': {'x':cx1-w//2-10,'y': cy+h+15, 'carte': None},
                        'e5': {'x':cx1-w//2-w-30,'y': cy+h+15, 'carte': None},
                        'e6': {'x':cx1-w-20,'y': cy+h*2+30, 'carte': None},
                    },
                    'Deck'  : {
                        'd1': {'x':dx1,'y': dy1, 'carte': None},
                        'd2': {'x':dx1-w-s1,'y': dy1, 'carte': None},
                        'd3': {'x':dx1-w*2-s1*2,'y': dy1, 'carte': None},
                        'd4': {'x':dx1-w*3-s1*3,'y': dy1, 'carte': None},
                        'd5': {'x':dx1-w*4-s1*4,'y': dy1, 'carte': None},
                        'd6': {'x':dx1-w*5-s1*5,'y': dy1, 'carte': None},
                        'd7': {'x':dx1-w*6-s1*6,'y': dy1, 'carte': None},
                    },
                }
            }
        
        
    def load_cartes(self):
        cartes = []
        with open('DataPerso.csv', 'r') as file:
            reader = csv.reader(file, skipinitialspace=True,delimiter=',', quoting=csv.QUOTE_NONE)
            for id,row in enumerate(reader):
                if id == 0 or id == 1 or row == [] :
                    continue
                else:
                    cartes.append(Carte(0,0,row[0],row[1],(row[2],row[3],row[4],row[5]),row[6]))
        return cartes
    
    
    def set_coord(self):
        for i,j in self.plateau.items():
            for k,l in j.items():
                for m,n in l.items():
                    if n['carte'] != None:
                        n['carte'].x, n['carte'].y = n['x'], n['y']
                        
    def plateau_to_transfer(self):
        for i,j in self.plateau.items():
            for k,l in j.items():
                for m,n in l.items():
                    if n['carte'] != None:
                        n['carte'] = n['carte'].get_all_info()
    
    def pioche(self,player):
        carte = self.pioches.pop(0)
        for i in self.plateau[player]['Deck']['d1'].values():
            if i == None:
                i['carte'] = carte
        
        print(self.plateau[player]['deck'])
        
    def update(self,nb_joueurs):
        self.pioche(nb_joueurs)
        self.set_coord()
        self.plateau_to_transfer()
        return self.plateau
        
                    
        

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
            Client = {'ip':address, 'client':client , 'name':None, 'scale': None, 'Nb_joueurs': None }
            self.clients.append(Client)
            Thread(target=self.handle_new_client, args=(Client, )).start()
    
    def broadcast(self, message):
        for client in self.clients:
                client['client'].send(pickle.dumps(message))
                
    def receve(self, client):
        global game
        while True:
            message = pickle.loads(client['client'].recv(2048))
            if isinstance(message, str):
                if message == 'q':
                    
                    client['client'].send(pickle.dumps('q'))
                    self.broadcast(f'{client["ip"]} disconnected')
                    client['client'].close()
                    
                    break
                elif message == "Start":
                    client['client'].send(pickle.dumps(client['Nb_joueurs']))
                else:
                    message = str(client['ip'])+' : '+message
                    self.broadcast(message)
            if isinstance(message, dict):
                if message['type'] == 'Pioche':
                    self.broadcast({'type':'Game', 'data':game.update(message['player'])})
            
    def handle_new_client(self, client):
        global nb_joueurs
        nb_joueurs += 1
        client['Nb_joueurs'] = nb_joueurs
        print(f'Connection from {client["ip"]}')
        Thread(target=self.receve, args=(client, )).start()
        self.broadcast(f'{client["ip"]} connected')


game = Game()
game.set_coord()
server = Server('127.0.0.1', 5555)
Thread(target=server.listen).start()
