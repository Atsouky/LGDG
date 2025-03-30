import socket
from threading import Thread
import pickle
import pygame
import csv

    

class Carte:
    def __init__(self,x,y,nom,imagepath,stats,camps=None,hiden=False,is_selected = False, scale=0.10):
        self.x = x
        self.y = y
        self.nom = nom
        self.pv, self.pm, self.pa, self.pw = stats
        self.scale = scale
        self.is_selected = is_selected
        self.img = pygame.image.load(imagepath)
        self.img = pygame.transform.scale(self.img, (self.img.get_width() * scale, self.img.get_height() * scale))
        w,h = self.img.get_width(),self.img.get_height()
        self.dosimg = pygame.image.load('data/dos/DosPioche.png')
        self.dosimg = pygame.transform.scale(self.dosimg, (self.dosimg.get_width() * scale, self.dosimg.get_height() * scale))
        
        self.imagepath = imagepath
        self.camps = camps
        self.hiden = hiden
        
        

        
        self.collision = None
    
    
    def draw(self,surface,who):
        
        if who == self.camps:
            
            if not self.hiden:
                surface.blit(self.img,(self.x,self.y))
                if not self.is_selected:
                    imgscale = pygame.image.load(self.imagepath)
                    imgscale = pygame.transform.scale(imgscale, (imgscale.get_width() * self.scale*6, imgscale.get_height() * self.scale*6))
                    surface.blit(imgscale,(0,0))
                
                    
            else:
                surface.blit(self.dosimg,(self.x,self.y))
        else:
            if not self.hiden:
                surface.blit(self.img,(self.x,self.y))
                
            else:
                surface.blit(self.dosimg,(self.x,self.y))

            
    def handle_events(self, event):
        if self.collision.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
            return True


class Pioche:
    def __init__(self,x,y, scale):
        self.img = pygame.image.load('data/dos/DosPioche.png')
        self.img = pygame.transform.scale(self.img, (self.img.get_width() * scale, self.img.get_height() * scale))
        self.collision = pygame.Rect(x,y,self.img.get_width(),self.img.get_height())
    def draw(self,surface):
        surface.blit(self.img,(self.collision.x,self.collision.y))
        
    def handle_events(self, event):
        if self.collision.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                print("pioche")
                return True
            



class Plateau:
    def __init__(self):
        
        
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
        
        self.emplacement1e ,self.emplacement3e  = self.emplacement3e, self.emplacement1e
        self.emplacement4e, self.emplacement5e = self.emplacement5e,self.emplacement4e 
          

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
        
        
        
        
        
    def draw(self,surface):    
        for emplacement in self.emplacements:
                pygame.draw.rect(surface,(0,0,255),pygame.Rect(emplacement[0],emplacement[1],emplacement[2],emplacement[3]),2)
        for emplacement in self.emplacementsE:
                pygame.draw.rect(surface,(255,0,0),pygame.Rect(emplacement[0],emplacement[1],emplacement[2],emplacement[3]),2)
        for deck in self.decks:
                pygame.draw.rect(surface,(0,255,0),pygame.Rect(deck[0],deck[1],deck[2],deck[3]),2)
        for deck in self.decksE:
                pygame.draw.rect(surface,(255,0,255),pygame.Rect(deck[0],deck[1],deck[2],deck[3]),2)

class Client:
    def __init__(self, ip, port, scale=0.10):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
        self.scale = scale
        self.client_data = {
            'ip': '127.0.0.1',
            'port': 5555,
            "name": None,
            'player': None
        }
    def send(self, message):
        self.client.send(pickle.dumps(message))
    def receve(self):
        global win_w, win_h, in_game_cartes
        sending = False
        while True:
            message = pickle.loads(self.client.recv(2048))
            if isinstance(message, dict):
                if not sending:
                    if message['type'] == 'Start':
                        sending = True
                        self.client_data['player'] = message['player']
                        self.send({'type':'Start', 'resolution':(win_w,win_h), 'name': 'Atsouky', 'player':message['player']})
                        sending = False
                                        
                    elif message['type'] == 'Pioche':
                        sending = True
                        carte = load_cartes(message['data'],self.scale)
                        print(message['data'])
                        message['data']['emplacement'] = 'deck'
                        in_game_cartes.append(carte)
                        sending = False
                    
            elif message == 'q':
                self.client.close()
                break
        
            else:
                print(message)

def load_cartes(carte,scale = 0.10):
    return Carte(
        carte['emplacement'],
        carte['name'],
        carte['image'],
        carte['stats'],
        camps=carte['camps'],
        hiden=carte['hiden'],
        scale=scale
    )

            
connected = False

in_game_cartes = []

pygame.init()
window = pygame.display.set_mode((0,0),pygame.RESIZABLE)
win_w,win_h = pygame.display.get_window_size()



while not connected:
    try:
        client = Client('127.0.0.1', 5555)
        connected = True
    except:
        pass

i = pygame.image.load('data/image/Ariane.png')
i = pygame.transform.scale(i, (i.get_width() * client.scale, i.get_height() * client.scale))
w,h = i.get_width(),i.get_height()
pioche= Pioche(win_w//2,win_h//2,client.scale)
i=None

plateau = Plateau()

Thread(target=client.receve).start()


while True:
    window.fill((0,0,0))  
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
        
    
        if pioche.handle_events(event):
            
            client.send({"type": "Pioche", "data": None, "player": client.client_data['player']})
        
        for carte in in_game_cartes:
            if carte.handle_events(event):
                selected = carte
                selected.is_selected = not selected.is_selected
    
    for i in in_game_cartes:
        i.draw(window)
    
    pioche.draw(window)     
    plateau.draw(window)         
    
    pygame.display.update()

