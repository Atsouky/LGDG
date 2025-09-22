import socket
import threading
import pickle
import random
import json


HOST = "127.0.0.1"
PORT = 5000

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)



def send(sock, obj):
    """Send a pickled Python object through a socket"""
    data = pickle.dumps(obj)
    sock.sendall(data)

def recv(sock):
    """Receive a pickled Python object from a socket"""
    data = sock.recv(4096)
    if not data:
        return None
    return pickle.loads(data)

def handle_client(conn, addr, nb):
    print(f"[NEW CONNECTION] {addr} connected.")
    with conn:
        while True:
            obj = recv(conn)
            if obj is None:
                continue

            print(f"[{addr}] {obj}")
            
            types = obj["type"]
            content = obj["content"]
            
            # Terminate connection if "kill" received
            if obj["content"] == "kill":
                send(conn, {"type": "message", "content": "Goodbye."})
                print(f"[DISCONNECT] {addr} sent kill command.")
                break
            
            elif types == "ping":
                
                response = {"type": "ping", "content": nb}
                send(conn, response)
            
            elif types == "poser":
                fr = content["from"]
                targ = content['target']
                
                for i,j in enumerate(Game[nb]['hand']):
                    if j.id == fr["card"][0]:
                        dfrcard = i
                        break
                    
                        
                Game[nb]["terrain"][targ['emplacement'][1]] = Game[nb]["hand"].pop(dfrcard)
                
                
                send(conn,{'type':"poser","content":[content['from']["emplacement"][1],content['target']["emplacement"][1],Game[nb]["terrain"][targ['emplacement'][1]].id,Game[nb]["terrain"][targ['emplacement'][1]].pv]})
                
            
            elif types == "pioche":
                carte = pioche.piocher()
                if carte:
                    Game[nb]['hand'].append(carte)
                    response = {"type": "pioche", "content": carte.format()}
                else:
                    response = {"type": "pioche", "content": None}
                send(conn, response)
            
            elif types == "command":
                if content == "reload":
                    pioche.reset()
            
            else:
                # Normal echo response
                response = {"type": "message", "content": "Echo: " + obj["content"]}
                send(conn, response)

    print(f"[DISCONNECT] {addr} disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server running on {HOST}:{PORT}")
    
    
    
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, threading.active_count()), daemon=True)
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


class Pioche:
    def __init__(self,cartes):
        self.pioche_origine = cartes
        self.pioche = []
        self.reset()
        self.shuffle()
    def add(self, carte):
        self.pioche.append(carte)
        
    def est_vide(self):
        return len(self.pioche) == 0
        
    def piocher(self):
        if not self.est_vide():
            return self.pioche.pop(0)
        else : return None
    def reset(self):
        self.pioche = self.pioche_origine
        
    def get_pioche(self):
        return self.pioche
    
    def get_pioche_origine(self):
        return self.pioche_origine
    
    def shuffle(self):
        random.shuffle(self.pioche)

class Card:
    def __init__(self,id,name,stats,classe,lien,pouvoir,stratege=False,hidden=True):
        self.id = id
        self.name = name
        self.pv,self.pa,self.pm,self.pw = stats["pv"],stats["pa"],stats["pm"],stats["pw"]
        self.classe = classe
        self.lien = lien
        self.pouvoir = pouvoir
        self.stratege = stratege
        self.hidden = hidden

    def is_hidden(self):
        return self.hidden
    
    def __repr__(self):
        return f"{self.id}, {self.pv},{self.pa},{self.pm},{self.pw},{self.classe},{self.lien},{self.pouvoir}"
    
    def format(self):
        return (self.id, self.pv)


Game = {1:{"hand":[],"terrain":{1:None,2:None,3:None,4:None,5:None,6:None}},
        2:{"hand":[],"terrain":{1:None,2:None,3:None,4:None,5:None,6:None}}}


def load_card(table):
    liste = []
    for i,j in table.items():
        liste.append(Card(i,j["name"],j["stats"],j["class"],j["lien"],j["pouvoir"]))
    return liste




if __name__ == "__main__":
    datatable = load_json("characterdatatable.json")
    cartes = load_card(datatable)
    pioche = Pioche(cartes)
    start_server()
    
