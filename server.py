import socket
import threading
import pyperclip
import os
import time

nome_usuarios = []
usuarios_conexão_basica = [] #Lista dos usuários que fizeram a primeira conexão com o server
conexão_primaria_interligada_com_conexão_chat = {}
portas = {} #Dicionario das portas abertas com sucesos, contendo : portas['nmr_porta'] : {senha, qtd_max_pessoas, nome_gp, lista_dos_cliente_conectados_ao_chat[] }
#Abaixo, é para criar uma pasta em que conterá os arquivos usados no chat
SAVE_FOLDER = os.path.dirname(os.path.abspath(__file__)) #Pega o path do diretorio atual
pasta_arquivos = os.path.join(SAVE_FOLDER, 'arquivos_crip_servidor') 
if not os.path.exists(pasta_arquivos):
    os.makedirs(pasta_arquivos)
SAVE_FOLDER = pasta_arquivos

def Create_chat(nmr_porta,senha,qtd_max_pessoas,pedido,nome_gp,nome_cliente,socket_primario_client):
    def comunicacao(socket_do_client_chat,path_pasta_de_arquivos_da_porta):
        while True: #Esse looping é para: Receber as mensagens pelos clientes e enviar a todos do grupo
            try:
                mensagem_do_chat = socket_do_client_chat.recv(1024).decode()
                if "Protocolo_close" in mensagem_do_chat: #Ao cliente avisar que desconectará, o server remove do chat e fecha conexão
                    nome_usuarios.remove(nome_cliente)
                    portas[nmr_porta][3].remove(socket_do_client_chat)
                    socket_do_client_chat.close()
                    conexão_primaria_interligada_com_conexão_chat[socket_do_client_chat].close()

                    if len(portas[nmr_porta][3]) == 0: #Se o client for o ultimo do chat, o server fecha o chat, e libera a porta para ser criado por outros
                        for nome_arquivo in os.listdir(portas[nmr_porta][4]): # loop percorre todos os arquivos da pasta, para deleta-la
                            caminho_arquivo = os.path.join(portas[nmr_porta][4], nome_arquivo)
                            # Exclua o arquivo
                            os.remove(caminho_arquivo)
                        # Deleta a pasta vazia
                        os.rmdir(portas[nmr_porta][4])
                        del portas[nmr_porta]
                    else: #Se tiver ainda clientes na porta, o servidor avisará que tal cliente saiu
                        mensagem_do_chat = mensagem_do_chat.split(',')
                        for c in portas[nmr_porta][3]:
                            try:
                                c.send(f'Cliente saiu do chat,{mensagem_do_chat[1]}'.encode())
                            except ConnectionError:
                                continue
                    break

                elif 'Tamanho do arquivo:' in mensagem_do_chat:
                    mensagem_do_chat = mensagem_do_chat.split(':')
                    tamanho_arquivo = int(mensagem_do_chat[1])
                    
                    qtd_arquivos_na_pasta = len(os.listdir(path_pasta_de_arquivos_da_porta))
                    nome_arquivo = qtd_arquivos_na_pasta + 1
                    file_path = os.path.join(path_pasta_de_arquivos_da_porta, str(nome_arquivo))
                    
                    # Receber os dados do arquivo
                    with open(file_path, 'wb') as arquivo:
                        while tamanho_arquivo > 0:
                            dados = socket_do_client_chat.recv(1024)
                            if not dados:
                                break
                            arquivo.write(dados)
                            tamanho_arquivo -= len(dados)
                            print('antes',dados)
                            print('dps',str(dados))
                    portas[nmr_porta][5].append(qtd_arquivos_na_pasta + 1)
                    continue
                
                elif 'nmr_arquivo' in mensagem_do_chat:
                    mensagem_do_chat = mensagem_do_chat.replace('nmr_arquivo',str(len(portas[nmr_porta][5])))
                
                elif 'Baixar:' in mensagem_do_chat:
                    mensagem_do_chat = mensagem_do_chat.split(':')
                    time.sleep(1)
                    file_path = os.path.join(path_pasta_de_arquivos_da_porta,str(mensagem_do_chat[1])).replace('\\\\','\\')
                    tamanho_arquivo = os.path.getsize(file_path)
                    socket_do_client_chat.send(f'Baixar:{tamanho_arquivo}:{mensagem_do_chat[1]}'.encode())
                    time.sleep(1)
                    with open(file_path,'rb') as file:
                        while True:
                            data = file.read(1024)
                            if not data:
                                break
                            socket_do_client_chat.sendall(data)
                    print('server enviou arquivo com sucesso!')
                    continue
                        
                for c in portas[nmr_porta][3]: #Nesse looping: Para cada usuario do grupo, será enviado a mensagem em questão
                    try:
                        c.send(mensagem_do_chat.encode())
                        #print(mensagem_do_chat) #Este print prova que a criptografia é de ponta a ponta, o server não tem a mensagem descriptografada
                    except ConnectionError:
                        continue
            except ConnectionError:
                continue
        return
    

    if (nmr_porta not in portas) and pedido == 'entrar grupo': #Tratamento de erro
        socket_primario_client.send('Recusado, Grupo nao existe'.encode())
        return
    elif (nmr_porta in portas) and pedido == 'criar grupo':
        socket_primario_client.send('Recusado, Grupo já criado'.encode())
        return
    
    if nmr_porta not in portas:  #Para impedir que crie/abra portas de numeros iguais

        #Abaixo será criado um socket de teste para ver se é possivel abrir um server nessa porta
        #Isso foi necessário pois, se não tivesse um socket de teste, encontraria MUITOS problemas de socket ao fechar um socket de server em que teve a porta errada, ou ip errado, etc...
        server_teste_pareamento_direto = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        teste = False
        try:
            server_teste_pareamento_direto.bind((str(ipv4_address), int(nmr_porta))) #Será tentado abrir o serve no ip e porta dito pelo cliente, em caso de erro, abaixo será enviado a mensagem dizendo que foi recusado
            server_teste_pareamento_direto.listen(int(qtd_max_pessoas))
            teste = True
            server_teste_pareamento_direto.close()
        except (ConnectionRefusedError, TimeoutError, OSError):
            with server_teste_pareamento_direto: #fecha completamente o socket de teste
                #Caso tenha dado erro, "o with:" é como se fosse um apoio ao .close() .Pois apenas o .close() não foi o suficiente para finalizar o socket
                socket_primario_client.send('Recusado, Porta nao disponivel'.encode())
                server_teste_pareamento_direto.close()
            return
        
        if teste == True: #Caso o teste tenha tido sucesso, será criado o socket de fato que irá fazer a abertura do server
            global server_pareamento_direto
            server_pareamento_direto = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_pareamento_direto.bind((str(ipv4_address), int(nmr_porta))) #Ao ver que foi possivel abrir neste ip / porta, agora será aberto de fato em um socket definitivo
            server_pareamento_direto.listen(int(qtd_max_pessoas))

            #portas[nmr_porta] = [senha, qtd_max_pessoas,nome_gp, [] ] #ex: portas[8888] >> {123,'20',grupo da familia, [] }  #Esse [] é para listar os sockets dos clientes conectados nessa porta
            pasta_arquivos_da_porta = os.path.join(SAVE_FOLDER, str(nmr_porta)) 
            if not os.path.exists(pasta_arquivos_da_porta):
                os.makedirs(pasta_arquivos_da_porta)   
            portas[nmr_porta] = [senha, qtd_max_pessoas,nome_gp, [], pasta_arquivos_da_porta, []]
            #ex: portas[8888] >> {123,'20',grupo da familia, [] } o primeiro [] é para listar os sockets dos clientes conectados nessa porta
            # o segundo [] é para listar os arquivos na porta

            print(f'Servidor aguardando conexões, em: {nmr_porta}')

    if (nmr_porta in portas) and len(portas[nmr_porta][3]) <int(portas[nmr_porta][1]) : #Para: 'Trancar' o grupo chat, entre a quantidade de pessoas especificada
        if portas[nmr_porta][0] == senha: #exemplo:  {'8888' : '123'}, if '123' == senha 
            autorizado = f'Autorizado+{portas[nmr_porta][2]}' #É enviado que foi autorizado, e o nome do grupo do chat em questão
            socket_primario_client.send(autorizado.encode())
            client_socket_no_chat, addr = server_pareamento_direto.accept()
            print(f'Conexão recebida de ip:{addr[0]} porta do cliente:{addr[1]} no chat de porta: {nmr_porta}')
            portas[nmr_porta][3].append(client_socket_no_chat)      
            conexão_primaria_interligada_com_conexão_chat[client_socket_no_chat] = socket_primario_client
            #Abaixo será criada uma thread para cada cliente que estará no chat, fazendo que esse cliente receba as mensagens por checagem própria
            #Checar depois se é isso mesmo
            client_thread_chat = threading.Thread(target=comunicacao, args=(client_socket_no_chat,portas[nmr_porta][4],))
            client_thread_chat.start()
        else:
            socket_primario_client.send('Recusado, senha está errada!'.encode())
    else:
        socket_primario_client.send('Recusado, Grupo esta cheio'.encode())


def escuta_solicitacao_primaria(client_socket,id_cliente):
    usuarios_conexão_basica.append(client_socket)
    usuarios_conexão_basica.append(id_cliente)
    while True: #Esse looping é para: atender os 'comandos' do cliente, por enquanto só tem um comando, que é para criar um chat entre 2 pessoas
                #Esse looping é para: ou seja, entrará em looping recebendo as info, e criando novo chat com base nas info dos cliente
        try:
            mensagem = client_socket.recv(1024).decode()
            if not mensagem:
                break
            elif 'Nome:' in mensagem:
                mensagem = mensagem.split(':') #mensagem[1] é o nome do cliente
                if (len(nome_usuarios) == 0) or (mensagem[1] not in nome_usuarios) :
                    nome_usuarios.append(mensagem[1])
                    client_socket.send('Nome Autorizado!'.encode()) 
                else: #Nome usuario já está foi escolhido no server
                    client_socket.send('Nome já escolhido por outro usuario!'.encode())
            else:
                msg = mensagem.split('+') 
                Create_chat(msg[0],msg[1],msg[2],msg[3],msg[4],msg[5],client_socket) # nmr_porta,senha,qtd_max_pessoas,nome_gp,nome do cliente, e o client_socket
        except ConnectionError:
            break
    

#Aqui é só para conectar o client no server
def Pareamento_inicial():
    server_pareamento_inicial = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria um obj socket, de conexão tcp ip
    hostname = socket.gethostname()
    global ipv4_address    
    ipv4_address = socket.gethostbyname(hostname)

    server_pareamento_inicial.bind((str(ipv4_address), 3000)) #associa o socket a um endereço ip e porta
    server_pareamento_inicial.listen(8) #servidor aceita até no maximo 8 conexões de clientes simultaneas
    print(f'Servidor aguardando conexões...')
    print(f'IPv4 do servidor já está copiado na area de transferencia! ({ipv4_address})')
    pyperclip.copy(ipv4_address) #copia (como se fosse ctrl+c) no ipv4 do server, não precisa mais copiar do terminal do servidor

    while True: #Esse looping é para: aceitar novos clientes ao server
        client_socket, addr = server_pareamento_inicial.accept() 
        print(f'Conexão recebida de {addr[0]}:{addr[1]} em pareamento normal com o server')
        #Abaixo, irá criar uma thread para cada cliente que se conectar ao servidor, para escutar suas solicitações primarias
        client_thread = threading.Thread(target=escuta_solicitacao_primaria, args=(client_socket,addr[1]))
        client_thread.start()
    

Pareamento_inicial()
