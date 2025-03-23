from random import shuffle
import pygame
import csv

class Carte:
    def __init__(self, x, y, name, image, pv, mp, pa, pw, classe, lien=[], camps=None, pw_value=None,is_Stratège=False, is_hiden=True, scale=0.25):
        self.x = x
        self.y = y
        self.name = name
        self.imagePath = image
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale))
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
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        if self.is_selected:
            img = pygame.image.load(self.imagePath)
            surface.blit(img, (0, 0))
           
    
    def handle_events(self, surface, mp):
        if self.is_selected:
            Move=pygame.Rect(self.x+self.width, self.y,100,50)
            pygame.draw.rect(surface, (255,0,0), Move, 2)
            if Move.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(surface, (0,255,0), Move, 2)
                if pygame.mouse.get_pressed()[0] :#and mp > 0:
                    global select,moving
                    select = self
                    moving = True
                    self.is_selected = False
                    
                    
        
    
    
    

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
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 0.075, self.image.get_height() * 0.075))
        self.collision = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
    def piocher(self):
        if self.cartes:
            carte = self.cartes.pop()
            carte.move(win_w//2+carte.width,0)
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
        self.emplacement1 = pygame.Rect(win_w-w-115, win_h-h, w, h)
        self.emplacement2 = pygame.Rect(win_w-w*2-130, win_h-h, w, h)
        self.emplacement3 = pygame.Rect(win_w-w*3-145, win_h-h, w, h)
        self.emplacement4 = pygame.Rect(win_w-w-175, win_h-h*2-15, w, h)
        self.emplacement5 = pygame.Rect(win_w-w*2-190, win_h-h*2-15, w, h)
        self.emplacement6 = pygame.Rect(win_w-w*2-130, win_h-h*3-30, w, h)
        
        self.emplacements = [self.emplacement1, self.emplacement2, self.emplacement3, self.emplacement4, self.emplacement5, self.emplacement6]
        
        
    def draw(self, surface):
        for i in self.emplacements:
            pygame.draw.rect(surface, (255,0,0), i, 2)
        



              #x, y, nom,    image,                 pv, mp, pa, pw, classe
Ariane = Carte(0,0,'Ariane','data/image/ariane.png', 10, 3, 35, 2,'Attaque')



pygame.init()

fenetre = pygame.display.set_mode((0,0),pygame.NOFRAME)
win_w, win_h = pygame.display.get_window_size()

cartes = []

with open('DataPerso.csv', 'r') as file:
    reader = csv.reader(file, skipinitialspace=True,delimiter=',', quoting=csv.QUOTE_NONE)
    for id,row in enumerate(reader):
        if id == 0 or id == 1 or row == [] :
            continue
        else:
            cartes.append(Carte(0,0,row[0],row[1],row[2],row[3],row[4],row[5],row[6],scale = 0.15))
                    



Atsouky = Joueur("Atsouky",[],Mp=10)
adv = Joueur("adv",[])

plateau = Plateau(Atsouky,adv,cartes)



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
                            moving = False
                        
            

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if select is not None:
                    for i in plateau.emplacements:
                        if select.collision.colliderect(i) and moving:
                            select.move(i.x,i.y)
                    #moving = False    
                
        
            
            
        if plateau.pioche.handle_events(fenetre,event):
            plateau.joueur1.piocher(plateau.pioche)
    
    if moving:
        select.move(event.pos[0]-select.width/2,event.pos[1]-select.height/2)
    
    
    
    
    for carte in plateau.joueur1.get_deck():
            carte.draw(fenetre)
            carte.handle_events(fenetre, plateau.joueur1.Mp)
    
    plateau.draw(fenetre)
    plateau.pioche.draw(fenetre)
    
    
    pygame.display.update()