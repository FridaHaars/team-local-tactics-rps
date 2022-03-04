from socket import socket, AF_INET, SOCK_STREAM

server_addr = ("localhost", 5555)
sock = socket(AF_INET, SOCK_STREAM)

with sock:
    sock.connect(server_addr)
    sock.sendall(b"HellooOO test")
    data = sock.recv(1024)
    print(f"Received {data}!")
    sock.close()