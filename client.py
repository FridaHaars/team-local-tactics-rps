from socket import socket


class Request:
    def __init__(self, sock : socket):
        self.sock = sock
        """
        Request is a class that lets us reuse the same socket for multiple purposes over several files without causing
        circular import errors.
        """
    

    def to_server(self, request : str):
        """
        Make a request to the server, see the "request" function in server.py for possible requests.
        """
        
        self.sock.sendall(request.encode())
        return self.sock.recv(4096).decode()

  
sock = socket()
sock.connect(("localhost", 12000))
request = Request(sock)
print(request.to_server("from_db=champs"))
    