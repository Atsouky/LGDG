import socket
from threading import Thread
import pickle
import pygame

class Carte:
    def __init__(self,x,y, name, image, stats, classes,camps=None, hiden=False, is_strategy=False, scale=0.10):
        self.scale = scale    
        self.x = x
        self.y = y
        self.name = name
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.classes = classes
        self.pv, self.pm, self.pa, self.pw = stats
        self.camps = camps
        self.hiden = hiden
        self.is_strategy = is_strategy
        self.collision = None

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    
class Game:
    def __init__(self,scale):
        self.scale = scale
        self.plateau = None
    def load(self, plateau):
        self.plateau = plateau
        for i,j in self.plateau.items():
            for k,l in j.items():
                for m,n in l.items():
                    if n['carte'] != None:
                        n['carte'] = Carte(n['x'],n['y'],n['carte'].name,n['carte'].image,n['carte'].stats,n['carte'].classes,n['carte'].camps,n['carte'].hiden,n['carte'].is_strategy,self.scale)
                        print(n)
    
    def draw(self, surface):
        for i,j in self.plateau.items():
            for k,l in j.items():
                for m,n in l.items():
                    if n['carte'] != None:
                        n['carte'].draw(surface)



class Client:
    def __init__(self, ip, port, scale=0.10):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
        self.scale = scale
        self.client_data = {
            'ip': '127.0.0.1',
            'port': 5555,
            "name": None,
            'Nb_joueurs': None
        }

    def send(self, message):
        self.client.send(pickle.dumps(message))
    
    def receve(self):
        global game
        while True:
            message = pickle.loads(self.client.recv(2048))
            if isinstance(message, str):
                if message == 'q':
                    break
                elif message == "Start":
                    self.client_data['Nb_joueurs'] = message
                
                else:
                    print(message)
            elif isinstance(message, dict):
                if message['type'] == 'Game':
                    game.load(message['data'])

class Pioche:
    def __init__(self, x,y,scale):
        self.img = pygame.image.load('data/dos/DosPioche.png')
        self.img = pygame.transform.scale(self.img, (self.img.get_width() * scale, self.img.get_height() * scale))
        self.collision = pygame.Rect(x,y,self.img.get_width(),self.img.get_height())

    def draw(self,surface):
        surface.blit(self.img,(self.collision.x,self.collision.y))
    
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.collision.collidepoint(event.pos):
                return True

pygame.init()
window = pygame.display.set_mode((0,0),pygame.NOFRAME)
win_w, win_h = pygame.display.get_window_size()







client = Client('127.0.0.1', 5555)
Thread(target=client.receve).start()
client.send('Start')
print(client.client_data)
pioche = Pioche(0,0,0.10)
game = Game(0.15)

while True:
    window.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client.send('q')
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_w:
                client.send('q')
                pygame.quit()
                exit()
        
        if pioche.handle_events(event):
            client.send({'type':'Pioche', 'player': client.client_data['Nb_joueurs']})
    pioche.draw(window)
    pygame.display.update()
        