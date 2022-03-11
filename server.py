from selectors import DefaultSelector, EVENT_READ
from socket import socket




def accept(sock):
    global player1_id, player2_id
    conn, address = sock.accept()  
    
    '''
    Accepts any incoming requests.

    We tag the clients that connect in the order in which they join. First to join becomes player 1.
    '''
    if not player1_id:
        print("Player 1 joined the game")
        print(conn)
        print(address)
        player1_id = conn
    elif not player2_id:
        print("Player 2 joined the game")
        player2_id = conn
    
    
    conn.setblocking(False)
    sel.register(conn, EVENT_READ)


    


def read(conn):
    global player1_id, player2_id
     
    '''
    We also tag any requests, so that we can know which player is making the requests'''
    if conn == player1_id:
        appendix = "1"
    elif conn == player2_id:
        appendix = "2"
    request_message = conn.recv(1024) + appendix.encode()
    
    if not request_message:
        conn.close() 
    
    '''
    Send a response back to the client, according to the evaluation of the corresponding "response" to their request
    
    See the available commands below:
    '''
    conn.sendall(response(request_message.decode()).encode())



def request_from_database(sock : socket, request : str) -> str:
    sock.sendall(request.encode())
    return sock.recv(4096).decode()



def response(request: str) -> str:
    global player1_id, player2_id, selection_count
    
    '''
    Each request to the server is a string with an '=' at the end, which seperated it from the arguments.
    
    This allows us to treat it like a psuedofunction that consists of a func and an argument.
    
    Because we tag each request, we are also able to have a third argument to our psuedofunction, a player id.
    
    We sometimes return the string 'void'. This is because we return a string, the read function will attempts
    to encode it in order to send it back to the client. The encoded "void" does not actually do anything
    '''
    
    func, arg = request.split("=", 1)    
    if func == "inc_scount":
        selection_count += 1
        return "void"
    elif func == "get_scount":
        return f"{selection_count}"
    elif func == "check_id":
        return arg
    elif func == "from_db":
        if "restart" in arg:
            selection_count = 0
        return request_from_database(db_sock, arg)
        


'''
Game server socket, and ID tags used by both clients.
'''
player1_id, player2_id = '',''
selection_count = 0
sel = DefaultSelector()
sock = socket()
sock.bind(("localhost", 12000))
sock.listen()
sock.setblocking(False)
sel.register(sock, EVENT_READ, True)
print("Server is running...")



'''
The server connects to the database...
'''
db_sock = socket()
db_sock.connect(("localhost", 12001))



'''
These are incoming requests, handled by the selector.
'''
while True:
    events = sel.select()
    for key, _ in events:
        if key.data:
            accept(key.fileobj)
        else:
            read(key.fileobj)
