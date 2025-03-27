import socket
from threading import Thread
import pickle,csv

def load_cartes():
    cartes = []
    with open('DataPerso.csv', 'r') as file:
        reader = csv.reader(file, skipinitialspace=True,delimiter=',', quoting=csv.QUOTE_NONE)
        for id,row in enumerate(reader):
            if id == 0 or id == 1 or row == [] :
                continue
            else:
                cartes.append(Carte(0,row[0],row[1],(row[2],row[3],row[4],row[5]),row[6]))
    return cartes

class Carte:
    def __init__(self, Emplacement, name, image, stats, classes,camps=None, hiden=False):
        self.Emplacement = Emplacement
        self.name = name
        self.image = image
        self.classes = classes
        self.pv, self.pm, self.pa, self.pw = stats
        self.camps = camps
        self.hiden = hiden
    def get_all_info(self):
        return {
            'Emplacement': self.Emplacement,
            'name': self.name,
            'image': self.image,
            'classes': self.classes,
            'stats': (self.pv, self.pm, self.pa, self.pw),
            'camps': self.camps,
            'hiden': self.hiden
        }

class Plateau:
    def __init__(self, joueur1, joueur2, cartes):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        win_w, win_h = joueur1.resolution
        w,h = cartes[0].width,cartes[0].height
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

class Pioche_server:
    def __init__(self):
        self.cartes = load_cartes()
        self.mélanger()
    
    def mélanger(self):
        import random
        random.shuffle(self.cartes)
        
    def piocher(self):
        return self.cartes.pop()


nb_joueurs = 0
class Server:
    clients = []
    def __init__(self, ip, port, pioche):
        self.serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pioche = pioche
        self.serveur.bind((ip, port))
        self.serveur.listen(2)
        print('Server online')
    
    def listen(self):
        
        while True:
            client, address = self.serveur.accept()
            Client = {'ip':address, 'client':client , 'name':None, 'scale': None, 'player': None , 'resolution': None}
            self.clients.append(Client)
            Thread(target=self.handle_new_client, args=(Client, )).start()
    
    def broadcast(self, message, client_in=None):
        if message['type'] == 'Pioche':
            for client in self.clients:
                if client_in == client['player']:
                    message['hiden'] = False
                    client['client'].send(pickle.dumps(message))
                else:
                    message['hiden'] = True
                    client['client'].send(pickle.dumps(message))
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
                
                elif message["type"] == 'Pioche':
                    self.broadcast({'type':'Pioche', 'data':self.pioche.piocher().get_all_info()}, message['player'])
            
            else:
                self.broadcast(message)

    def handle_new_client(self, client):
        global nb_joueurs
        print(f'Connection from {client["ip"]}')
        self.Send({'type':'Start', 'player':nb_joueurs}, client)
        Thread(target=self.receve, args=(client, )).start()
        self.broadcast({'type':'info', 'data':client["ip"]})


pioche = Pioche_server()     
server = Server('127.0.0.1', 5555, pioche)
Thread(target=server.listen).start()

