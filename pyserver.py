from selectors import DefaultSelector, EVENT_READ
from socket import socket
import dbreader


def accept(sock):
    global player1_id, player2_id
    conn, address = sock.accept()  # Should be ready
    
    if not player1_id:
        player1_id = conn
    elif not player2_id:
        player2_id = conn
    
    conn.setblocking(False)
    sel.register(conn, EVENT_READ)


def string_to_socket(socket : str):
    None
    


def read(conn):
    global player1_id, player2_id
     
    #add ID tag to end of request messages so the server knows who wants it:
    if conn == player1_id:
        appendix = "1"
    elif conn == player2_id:
        appendix = "2"
    
    request_message = conn.recv(1024) + appendix.encode()
    
    if not request_message:
        conn.close() 
    
    conn.sendall(response(request_message.decode()).encode())



def response(request: str) -> str:
    global player1_id, player2_id
    
    method, value = request.split(" ")
    if method == "pick_champ":
        return dbreader.request(value)
    elif method == "chat":
        return value
    elif method == "all_champs":
        return dbreader.get_all()
    elif method == "check_id":
        if value == "1":
            return "I am player one"
        elif value == "2":
            return "I am player two"



    
player1_id = ''
player2_id = '' 




connections = []
sel = DefaultSelector()
sock = socket()
sock.bind(("localhost", 12000))
sock.listen()
sock.setblocking(False)
sel.register(sock, EVENT_READ, True)


while True:
    events = sel.select()
    for key, _ in events:
        if key.data:
            accept(key.fileobj)
        else:
            read(key.fileobj)
