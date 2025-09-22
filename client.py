import socket
import pickle
import threading
import pygame as pg
import time,json

pg.init()
pg.font.init()

pg.display.set_caption("Client")
screen = pg.display.set_mode()
clock = pg.time.Clock()
font = pg.font.Font(None, 32)
global_scale = 0.136
screen_width, screen_height = pg.display.get_surface().get_size()

with open("characterdatatable.json", "r") as f:
    datatable = json.load(f)

img = pg.image.load("data/Fonds des cartes/FondBleu.png")
card_width, card_height = pg.transform.scale(img, (img.get_width() * global_scale, img.get_height() * global_scale)).get_size()




class Client:
    
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 5000
        self.s = None
        
        self.player = None

    def send(self, obj):
        """Send a pickled Python object through a socket"""
        data = pickle.dumps(obj)
        self.s.sendall(data)

    def recv(self):
        """Receive a pickled Python object from a socket"""
        data = self.s.recv(4096)
        if not data:
            return None
        return pickle.loads(data)

    def client_session(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST,self.PORT))
        print("Connected to server. Type messages, or 'kill' to exit.")

        while True:

            # Receive response
            response = self.recv()
            try:types = response['type'];content = response["content"]
            except:pass
            
            
            if response is None:
                print("Server closed connection.")
                break
            
            elif response['content'] == "kill":
                print("Connection terminated.")
                break
            elif types == "ping":
                self.player = response['content']
                print("[SERVER RESPONSE]", self.player)
            

            
            elif types == "pioche":
                for key in Game["hand"]:
                    if Game["hand"][key].get() == None and content:
                        print(content[1])
                        Game["hand"][key].set(Card(content[0],content[1]))
                        break
            elif types == 'poser':
                Game["hand"][content[0]].remove()
                Game["terrain_p"][content[1]].set(Card(content[2],content[3]))
            
            else:print("[SERVER RESPONSE]", response)



class Card:
    def __init__(self,name,pv):
        self.name = name
        self.pv = pv
        if name!='hidden':
            sprite = pg.image.load(f"data/{name}.png")
        else:
            sprite = pg.image.load(f"data/Dos des cartes/DosAdversaires.png")
        self.sprite = pg.transform.scale(sprite, (sprite.get_width() * global_scale, sprite.get_height() * global_scale))
    
    
    def draw(self,coord):
        screen.blit(self.sprite, (coord[0],coord[1]))
        
    def get(self):
        return (self.name,self.pv)
    def __repr__(self):
        return str(self.name)
    
class Emplacement:
    def __init__(self,x,y,color=(0,255,0)):
        self.x,self.y= x,y
        self.w,self.h = card_width,card_height
        self.rect = pg.Rect(self.x,self.y,self.w,self.h)
        self.content = None
        self.color = color
    

    def collision(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
    
    def coord(self):
        return (self.x,self.y)
    def get(self):
        if self.content:
            return self.content
    def get_name(self):
        if self.content:
            return self.content.get()
    
    def set(self,content:Card):
        self.content = content
    def remove(self):
        self.content = None
    def __repr__(self):
        if self.content:
            return str(self.content)
        else:
            return f'No Card'
    def draw(self):
        if self.content:
            self.content.draw(self.coord())
        else:
            pg.draw.rect(screen, self.color, self.rect,1)

class Selecteur:
    def __init__(self,x,y,state,card):
        self.x,self.y = x,y-75
        self.card = card
        zoom= pg.image.load(f"data/{card.get()[0]}.png")
        self.zoom = pg.transform.scale(zoom, (zoom.get_width() * (global_scale+0.5), zoom.get_height() * (global_scale+0.5)))
        self.state = state    # hand terrain_p terrain_e ehand
        self.rect_att = pg.Rect(self.x,self.y,card_width,25)
        self.rect_move = pg.Rect(self.x,self.y+25,card_width,25)
        self.rect_pw = pg.Rect(self.x,self.y+50,card_width,25)
        self.rect_hand = pg.Rect(self.x,self.y+50,card_width,25)
    
    def draw(self):
        screen.blit(self.zoom, (0,0))
        match self.state:
            case "hand":
                pg.draw.rect(screen, (0,255,0), self.rect_hand,1)
                draw_string("Poser",self.rect_hand.topleft[0],self.rect_hand.topleft[1])
                
                
            case "terrain_p":
                pg.draw.rect(screen, (0,255,0), self.rect_att,1)
                pg.draw.rect(screen, (0,255,0), self.rect_move,1)
                pg.draw.rect(screen, (0,255,0), self.rect_pw,1)

    def collision(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect_hand.collidepoint(mouse_pos):
            return "hand"
        if self.rect_att.collidepoint(mouse_pos):
            return "att"
        if self.rect_move.collidepoint(mouse_pos):
            return "move"
        if self.rect_pw.collidepoint(mouse_pos):
            return "pw"
                
        

class Pioche:
    def __init__(self, x,y):
        self.x = x
        self.y = y
        sprite = pg.image.load("data/Dos des cartes/DosPioche.png")
        self.sprite = pg.transform.scale(sprite, (sprite.get_width() * global_scale, sprite.get_height() * global_scale))
        self.w , self.h = self.sprite.get_size()
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
    def draw_pioche(self,x,y):
        screen.blit(self.sprite, (x, y))

    def collision(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        
        

def void_terrain():
    Game = {"terrain_p":{},
        "terrain_e":{},
        "hand":{},
        "ehand":{}}
    terp = [(1,1),(2,1),(3,1),(1.5,2),(2.5,2),(2,3)]
    for k,l in enumerate(terp):
        i,j = l
        Game["terrain_p"][k+1] = Emplacement(screen_width - card_width*i,screen_height - card_height*j)
        Game["terrain_e"][k+1] = Emplacement(screen_width - card_width*i,card_height*(j-1),(255,0,0))
        Game["hand"][k+1] = Emplacement(card_width*(k+1),screen_height - card_height)
        Game["ehand"][k+1] = Emplacement(card_width*(k+5),0,(255,0,0))
    Game["hand"][7] = Emplacement(card_width*7,screen_height - card_height)
    Game["ehand"][7] = Emplacement(card_width*11,0,(255,0,0))
    return Game


def draw_all():
    for PKey in Game.keys():
        for key in Game[PKey].keys():
            Game[PKey][key].draw()



def draw_string(text, x, y ,scale = 1, rgb = (0,255,0)):
    text = font.render(text, True, rgb)
    text = pg.transform.scale(text, (text.get_width() * scale, text.get_height() * scale))
    screen.blit(text, (x, y))
    
    
def check_collision():
    for PKey in Game.keys():
        for key in Game[PKey].keys():
            if Game[PKey][key].collision():
                return {"emplacement":(PKey,key),"card":Game[PKey][key].get()}


        


Action = {"type":None,"content":{"from":None,"target":None}}

Poser = False
Bouger = False
Attaquer = False
Pouvoir = False

loop = True
pioche = Pioche((screen_width//2 + card_width*2), (screen_height - card_height*2))
selected = None


timer1 = time.monotonic()




if __name__ == "__main__":
    Game = void_terrain()

    client = Client()
    thead = threading.Thread(target=client.client_session)
    thead.start()
    time.sleep(0.1)
    client.send({"type": "ping", "content": ""})
    
    while loop:
        screen.fill((0,0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                client.send({"type": "message", "content": "kill"})
                loop = False
                break
            
            if event.type == pg.KEYDOWN:
                key = event.key
                if  key == pg.K_ESCAPE:
                    client.send({"type": "message", "content": "kill"})
                    loop = False
                    break
                
                if key == pg.K_RETURN:
                    client.send({"type": "command", "content": "reload"})
                    
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    
                    if any([Poser,Attaquer,Bouger,Pouvoir]) is False:
                        #quant selectioner
                        if selected:
                            selected_coli = selected.collision()
                            if selected_coli:
                                print(selected_coli)
                                match selected_coli:
                                    case "hand": 
                                        Action["type"] = "poser"
                                        Action['content']['from'] = col
                                        Action['content']['from']['card'] = col['card'].get()
                                        Poser =    True
                                        print(Action)
                                    case "att" : Attaquer = True
                                    case "move": Bouger =   True
                                    case "pw"  : Pouvoir =  True
                        
                        #emplacement
                        col= check_collision()
                        if col: 
                            print(col)
                            
                            pkey,key = col["emplacement"]
                            cx,cy = Game[pkey][key].coord()
                            if col["card"]:
                                selected = Selecteur(cx,cy,pkey,col['card'])
                            
                            
                            
                        #pioche
                        if pioche.collision():
                            if Game["hand"][7].get() == None:
                                client.send({"type": "pioche", "content": ""})  
                            else: print("Main pleine")
                    
                    elif Poser:
                       
                        col = check_collision()
                        
                        
                        
                        #TODO : Does not Work
                        while col is not None and col["emplacement"][0] != "terrain_p" and col['card'] != None:
                            col = check_collision()
                        
                        Action['content']["target"] = col
                        
                        print(Action)
                        Poser = False
                        client.send(Action)
                        Action = {"type":None,"content":{"from":None,"target":None}}
                        selected = None


        
        if time.monotonic() - timer1 > 1:
            timer1 = time.monotonic()
            
        
        draw_all()
        pioche.draw_pioche(pioche.x, pioche.y)
        
        
        if selected:
            selected.draw()
            
            
            
            
        pg.display.flip()
        clock.tick(60)
    
    pg.quit()  
    thead.join()  



















