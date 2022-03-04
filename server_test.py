from socket import socket, AF_INET, SOCK_STREAM

addr = ("localhost", 5555)
sock = socket(AF_INET, SOCK_STREAM)

with sock:
    sock.bind(addr)
    sock.listen()
    conn, addr = sock.accept()
    with conn:
        print (f"Connected at {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            sock.close()