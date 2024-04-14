import socket
import threading
import pyperclip

usuarios_conexão_basica, portas = [], {}
client_socket_chat, client_chat = [], []

#porta entre 1024 a 49151
#futuramente usar essa senha para permitir acesso
def Create_chat(nmr_porta,senha,qtd_pessoas,socket_primario_client):
    def comunicacao(socket_do_client_chat):
        while True: #Esse looping é para: Receber as mensagens pelos clientes e enviar a todos do grupo
            try:
                mensagem_do_chat = socket_do_client_chat.recv(1024).decode()
                if mensagem_do_chat == "Protocolo_close":
                    client_socket_chat.remove(socket_do_client_chat)
                    socket_do_client_chat.close()
                    print('Usuario foi desconectado')
                    if len(client_socket_chat) == 0:
                        del portas[nmr_porta]
                    break
                for c in client_socket_chat:
                    try:
                        c.send(mensagem_do_chat.encode())
                        #print(mensagem_do_chat) #Para provar que a criptografia é de ponta a ponta
                    except ConnectionError:
                        continue
            except ConnectionError:
                continue
        return
    
    if nmr_porta not in portas:  #Para impedir que crie/abra portas de numeros iguais
        global server_pareamento_direto
        server_pareamento_direto = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_pareamento_direto.bind((str(ipv4_address), int(nmr_porta)))
        server_pareamento_direto.listen(int(qtd_pessoas))    
        portas[nmr_porta] = senha
        print(f'Servidor aguardando conexões, em: {nmr_porta}')

    if len(client_socket_chat) <int(qtd_pessoas): #Para: 'Trancar' o grupo chat, entre a quantidade de pessoas especificada
        if senha == portas.get(nmr_porta): #portas[nmr_porta] = senha
            socket_primario_client.send('Autorizado'.encode())
            client_socket_create_chat, addr = server_pareamento_direto.accept()
            print(f'Conexão recebida de ip:{addr[0]} porta do cliente:{addr[1]} no chat de porta: {nmr_porta}')
            client_socket_chat.append(client_socket_create_chat)       
            #Abaixo será criada uma thread para cada cliente que estará no chat, fazendo que esse cliente receba as mensagens por checagem própria
            #Checar depois se é isso mesmo
            client_thread_chat = threading.Thread(target=comunicacao, args=(client_socket_create_chat,))
            client_thread_chat.start()
        else:
            print('Senha do usuario está errada!')
    else:
        print('Servidor cheio')

def escuta_solicitacao_primaria(client_socket,id_cliente):
    usuarios_conexão_basica.append(client_socket)
    usuarios_conexão_basica.append(id_cliente)
    while True: #Esse looping é para: atender os 'comandos' do cliente, por enquanto só tem um comando, que é para criar um chat entre 2 pessoas
                #Esse looping é para: ou seja, entrará em looping recebendo as info, e criando novo chat com base nas info dos cliente
        try:
            mensagem = client_socket.recv(1024).decode()
            if not mensagem:
                break
            msg = mensagem.split('+') 
            Create_chat(msg[0],msg[1],msg[2],client_socket) # nmr_porta,senha,qtd_pessoas
        except ConnectionError:
            break

    

#Aqui é só para conectar o client no server
def Pareamento_inicial():
    server_pareamento_inicial = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria um obj socket, de conexão tcp ip
    hostname = socket.gethostname()
    global ipv4_address    
    ipv4_address = socket.gethostbyname(hostname)

    server_pareamento_inicial.bind((str(ipv4_address), 3000)) #associa o socket a um endereço ip e porta
    server_pareamento_inicial.listen(5) #servidor aceita até no maximo 5 conexões de clientes simultaneas
    print(f'Servidor aguardando conexões... ipv4 do server: {ipv4_address}')
    pyperclip.copy(ipv4_address) #copia (como se fosse ctrl+c) no ipv4 do server, não precisa mais copiar do terminal do servidor

    while True: #Esse looping é para: aceitar novos clientes ao server
        client_socket, addr = server_pareamento_inicial.accept() 
        print(f'Conexão recebida de {addr[0]}:{addr[1]} em pareamento normal com o server')
        #Abaixo, irá criar uma thread para cada cliente que se conectar ao servidor, para escutar suas solicitações primarias
        client_thread = threading.Thread(target=escuta_solicitacao_primaria, args=(client_socket,addr[1]))
        client_thread.start()
    

Pareamento_inicial()
