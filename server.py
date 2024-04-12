import socket
import threading

clients = []
portas = []

#porta entre 1024 a 49151
#futuramente usar essa senha para permitir acesso
def Create_chat(nmr_porta,senha,qtd_pessoas):
    def comunicacao(socket_do_client_chat):
        client_socket_chat.append(socket_do_client_chat)

        while True:
            try:
                mensagem_do_chat = client_socket_create_chat.recv(1024).decode()
                if not mensagem_do_chat:
                    break
                for c in client_socket_chat:
                    try:
                        c.send(mensagem_do_chat.encode())
                        #print(mensagem_do_chat) #Para provar que a criptografia é de ponta a ponta
                        
                    except ConnectionError:
                        continue
            except ConnectionError:
                return
        return

    server_pareamento_direto = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #If para imepdir que portas de mesmo numero sejam criadas
    if nmr_porta not in portas:
        server_pareamento_direto.bind((str(ipv4_address), int(nmr_porta)))
        server_pareamento_direto.listen(5)    
        portas.append(nmr_porta)
        print(f'Servidor aguardando conexões, em: {nmr_porta}')

        client_chat = []
        client_socket_chat = []
        while len(client_chat) <int(qtd_pessoas):

            client_socket_create_chat, addr = server_pareamento_direto.accept()
            print(f'Conexão recebida de {addr[0]}:{addr[1]} no chat {nmr_porta}')
            client_chat.append(addr[1])


            client_handler_chat = threading.Thread(target=comunicacao, args=(client_socket_create_chat,))
            client_handler_chat.start()


def escuta_solicitacao_primaria(client_socket):
    clients.append(client_socket)  
    while True:
        try:
            mensagem = client_socket.recv(1024).decode()
            if not mensagem:
                break
            msg = mensagem.split('+') 
            Create_chat(msg[0],msg[1],msg[2])
        except ConnectionError:
            break
    clients.remove(client_socket)
    client_socket.close()

#Aqui é só para conectar o client no server
def Pareamento_inicial():
    server_pareamento_inicial = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    global ipv4_address    
    ipv4_address = socket.gethostbyname(hostname)

    server_pareamento_inicial.bind((str(ipv4_address), 3000))
    server_pareamento_inicial.listen(5)    
    print(f'Servidor aguardando conexões... ipv4 do server: {ipv4_address}')

    global usuarios
    usuarios = []

    while True:
        
        client_socket, addr = server_pareamento_inicial.accept()
        print(f'Conexão recebida de {addr[0]}:{addr[1]} em pareamento normal com o server')

        usuarios.append(addr[1])

        client_handler = threading.Thread(target=escuta_solicitacao_primaria, args=(client_socket,))
        client_handler.start()
    

if __name__ == '__main__':
    Pareamento_inicial()
