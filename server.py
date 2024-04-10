import socket
import threading

clients = []

def handle_client(client_socket):
    clients.append(client_socket)
    
    while True:
        try:
            mensagem = client_socket.recv(1024).decode()
            if not mensagem:
                break
            broadcast(mensagem)
        except ConnectionError:
            break

    clients.remove(client_socket)
    client_socket.close()

def broadcast(mensagem):
    for client in clients:
        try:
            client.send(mensagem.encode())
        except ConnectionError:
            continue

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()    
    ipv4_address = socket.gethostbyname(hostname)

    server.bind((str(ipv4_address), 3000))
    server.listen(5)    
    print('Servidor aguardando conexões...')

    while True:
        client_socket, addr = server.accept()
        print(f'Conexão recebida de {addr[0]}:{addr[1]}')

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    start_server()
