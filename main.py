from random import shuffle
import pygame
import csv

from Serveur import Server


import socket
from threading import Thread
import pickle


class Carte:
    def __init__(self, x, y, name, image, pv, mp, pa, pw, classe, lien=[], camps=None, pw_value=None,is_Stratège=False, is_hiden=True, scale=0.25):
        self.x = x
        self.y = y
        self.name = name
        self.imagePath = image
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale))
        self.dos = pygame.image.load('data/dos/DosCarte.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.collision = pygame.Rect(self.x, self.y, self.width, self.height)
        self.pv = pv
        self.mp = mp
        self.pa = pa
        self.pw = pw
        self.classe = classe
        self.camps = camps
        self.pw_value = pw_value
        self.is_Stratège = is_Stratège
        self.is_hiden = is_hiden
        self.lien = lien
        self.is_selected = False
        

    def __str__(self):
        return f'{self.name} (pv:{self.pv}, pm:{self.mp}, pa:{self.pa}, pw:{self.pw})'
    def __repr__(self):
        return f'{self.name} (pv:{self.pv}, pm:{self.mp}, pa:{self.pa}, pw:{self.pw})'
    def move(self,x,y):
        self.x = x
        self.y = y
        self.collision = pygame.Rect(self.x, self.y, self.width, self.height)
    #region get
    def get_pos(self):
        return self.x, self.y
    def get_name(self):
        return self.name    
    def get_pv(self):
        return self.pv
    def get_mp(self):
        return self.mp
    def get_pa(self):
        return self.pa
    def get_pw(self):
        return self.pw
    def get_camps(self):
        return self.camps
    def get_pw_value(self):
        return self.pw_value
    def get_classe(self):
        return self.classe
    #endregion
    def attaque(self, cible):
        self.is_hiden = False
        cible.is_hiden = False
        if self.pa > 0 and cible.get_name() not in self.lien and self.camps != cible.camps:
            cible.pv = max(0, cible.pv - self.pa)
            if cible.pv > 0:
                self.pv = max(0, self.pv - cible.pa)
        
    def heal(self, cible):
        cible.pv += self.pw_value
    
    def drawString(self, surface,x,y, text):
        font = pygame.font.Font(None, 30)
        text = font.render(text, True, (255,255,255))
        surface.blit(text, (x, y))
    
    def draw(self, surface,scale):
        if not self.is_hiden:
            surface.blit(self.image, (self.x, self.y))
            if self.is_selected:
                img = pygame.image.load(self.imagePath)
                img = pygame.transform.scale(img, (img.get_width() * scale*7, img.get_height() * scale*7))
                surface.blit(img, (0, 0))
        else:
            surface.blit(self.dos, (self.x, self.y))
    def rescale(self,scale):
        image = pygame.image.load(self.imagePath)
        self.image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.collision = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def handle_events(self, surface, mp):
        if self.is_selected:
            Move=pygame.Rect(self.x+self.width, self.y,100,50)
            Attaque = pygame.Rect(self.x+self.width, self.y+50,100,50)
            
            pygame.draw.rect(surface, (255,0,0), Move, 2)
            pygame.draw.rect(surface, (255,0,0), Attaque, 2)
            
            self.drawString(surface,self.x+self.width+10, self.y+10, "Bouger")
            self.drawString(surface,self.x+self.width+10, self.y+60, "Attaquer")
            
            if Move.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(surface, (0,255,0), Move, 2)
                
                if pygame.mouse.get_pressed()[0] :#and mp > 0:
                    global select,moving
                    select = self
                    moving = True
                    self.is_selected = False
            
            if Attaque.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(surface, (0,255,0), Attaque, 2)
                
                if pygame.mouse.get_pressed()[0] :#and mp > 0:
                    pass

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
        return 'Packet carte send or receive'
                
def packet_carte_to_carte(message):
    data = message.data
    return Carte(data['x'],data['y'],data['name'],data['image'],data['pv'],data['mp'],data['pa'],data['pw'],data['classe'],data['lien'],data['camps'],data['pw_value'],data['is_Stratège'],data['is_hiden'],data['scale'])
    
def carte_to_packet_carte(carte):
    return Packet_carte(carte.x,carte.y,carte.name,carte.image,carte.pv,carte.mp,carte.pa,carte.pw,carte.classe,carte.lien,carte.camps,carte.pw_value,carte.is_Stratège,carte.is_hiden,carte.scale)    






class Client:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
    def send(self, message):
        self.client.send(pickle.dumps(message))
    def receve(self):
        global Server_Mesage
        while True:
            
            message = pickle.loads(self.client.recv(2048))
            if isinstance(message, str):
                if message == '?scale':
                    self.send('? '+str(scale))
                elif message == 'q':
                    self.client.close()
                    break
                elif message[0:2] == '¤j':
                    isJoueur = message.split(' ')[1]
                    
                print(message)
                
            
            
                
            elif isinstance(message, Packet_carte):
                message = packet_carte_to_carte(message)
                message.rescale(scale)
                print(message)
                Server_Mesage = message
                
                

class Joueur:
    def __init__(self, name, deck, Mp = None):
        self.name = name
        self.deck = deck
        self.Mp = Mp
    
    
    def __str__(self):
        return self.name
    def __repr__(self): 
        return self.name
    def get_name(self):
        return self.name
    def get_deck(self):
        return self.deck
    
    def add_cartes(self, cartes):
        self.deck.extend(cartes)
    def piocher(self,Pioche):
        if  self.Mp != None and self.Mp > 0:
            p=Pioche.piocher()
            if p != None:
                self.deck.append(p)
                self.Mp -= 1
    
    def poser(self,carte):
        self.deck.remove(carte)

class Pioche:
    def __init__(self, cartes):
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
            carte.move(win_w//2+carte.width+carte.width//2,0)
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
                        
        


        
        

class Plateau:
    def __init__(self, joueur1, joueur2, cartes):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.pioche = Pioche(cartes)
        w,h = cartes[0].width,cartes[0].height
        cx,cy = win_w-w-115, win_h-h
        
        self.emplacement1 = pygame.Rect(cx, cy, w, h)
        self.emplacement2 = pygame.Rect(cx-w-20, win_h-h, w, h)
        self.emplacement3 = pygame.Rect(cx-w*2-40, win_h-h, w, h)
        self.emplacement4 = pygame.Rect(cx-w//2-10, win_h-h*2-15, w, h)
        self.emplacement5 = pygame.Rect(cx-w//2-w-30, win_h-h*2-15, w, h)
        self.emplacement6 = pygame.Rect(cx-w-20, win_h-h*3-30, w, h)
        
        self.emplacements = [self.emplacement1, self.emplacement2, self.emplacement3, self.emplacement4, self.emplacement5, self.emplacement6]
        
        cx,cy = win_w-w-115, 20
        self.emplacement1e = pygame.Rect(cx, cy, w, h)
        self.emplacement2e = pygame.Rect(cx-w-20, cy, w, h)
        self.emplacement3e = pygame.Rect(cx-w*2-40, cy, w, h)
        self.emplacement4e = pygame.Rect(cx-w//2-10, cy+h+15, w, h)
        self.emplacement5e = pygame.Rect(cx-w//2-w-30, cy+h+15, w, h)
        self.emplacement6e = pygame.Rect(cx-w-20, cy+h*2+30, w, h)
        
        self.emplacementsE = [self.emplacement1e, self.emplacement2e, self.emplacement3e, self.emplacement4e, self.emplacement5e, self.emplacement6e]
        
        
    def draw(self, surface):
        for i in self.emplacements:
            pygame.draw.rect(surface, (0,0,255), i, 2)
        for i in self.emplacementsE:
            pygame.draw.rect(surface, (255,0,0), i, 2)



              #x, y, nom,    image,                 pv, mp, pa, pw, classe
Ariane = Carte(0,0,'Ariane','data/image/ariane.png', 10, 3, 35, 2,'Attaque')



pygame.init()

fenetre = pygame.display.set_mode((0,0),pygame.NOFRAME)
win_w, win_h = pygame.display.get_window_size()
dictscale ={
    "1920x1080":0.15,
    "1366x768":0.10,
}
scale = dictscale[str(win_w)+"x"+str(win_h)]


cartes = []

with open('DataPerso.csv', 'r') as file:
    reader = csv.reader(file, skipinitialspace=True,delimiter=',', quoting=csv.QUOTE_NONE)
    for id,row in enumerate(reader):
        if id == 0 or id == 1 or row == [] :
            continue
        else:
            cartes.append(Carte(0,0,row[0],row[1],row[2],row[3],row[4],row[5],row[6],scale = scale))
                    
Server_Mesage = None


Atsouky = Joueur("Atsouky",[],Mp=10)
adv = Joueur("adv",[])

plateau = Plateau(Atsouky,adv,cartes)

from threading import Thread
client = Client('127.0.0.1', 5555)
client_tread = Thread(target=client.receve)
client_tread.start()
client.send('/name Atsouky')





click = False
select = None
move = False
moving = False
while True:
    fenetre.fill((0,0,0))   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_w:
                client.send('q')
                exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                
                for i in plateau.joueur1.get_deck():
                    if i.collision.collidepoint(event.pos):
                        i.is_selected = not i.is_selected
                        if moving: 
                            i.is_selected = False
                            if select is not None:
                                for i in plateau.emplacements:
                                    if select.collision.colliderect(i) and moving:
                                        select.move(i.x,i.y)
                                client.send(f'¤move {select.name} {select.x} {select.y}')
                            moving = False
                        
            

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if select is not None:
                    for i in plateau.emplacements:
                        if i.collidepoint(event.pos) and moving:
                            select.move(i.x,i.y)
                    #moving = False    
                
        
            
            
        if plateau.pioche.handle_events(fenetre,event):
            #plateau.joueur1.piocher(plateau.pioche)
            client.send('¤pioche')
    
    if moving:
        select.move(event.pos[0]-select.width/2,event.pos[1]-select.height/2)
    
    
    if Server_Mesage is not None:
        plateau.joueur1.add_cartes([Server_Mesage])
        Server_Mesage = None
    
    for carte in plateau.joueur1.get_deck():
            carte.draw(fenetre,scale)
            carte.handle_events(fenetre, plateau.joueur1.Mp)
    
    plateau.draw(fenetre)
    plateau.pioche.draw(fenetre)
    
    
    pygame.display.update()