import socket
import threading
import pickle
import random


HOST = "127.0.0.1"
PORT = 5000

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
            
            elif types == "pioche":
                carte = pioche.piocher()
                if carte:
                    response = {"type": "pioche", "content": {"name":carte,"pv":10}}
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
    def __init__(self):
        self.pioche_origine = ["Ariane","Aude" ,"Dimitri" ,"Edwin" ,"Eleo" ,"Lie" ,"Liz" ,"LomaMalo" ,"MaiRose" ,"Mike" ,"Papuchon" ,"Sofia" ,"Sosara" ,"Stones" ,"Vivalie" ,"Zerephyr"]
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











if __name__ == "__main__":
    pioche = Pioche()
    start_server()
    
