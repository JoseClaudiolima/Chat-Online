from Lib import CriptografiaRSA as rsa
from Lib import Emoticons

import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
import socket
import threading
import math
import time
import emoji
import os

#Passo 1: Coloque o nome
#Passo 2: Coloque o ipv4 do server, ja copia automaticamente no server.py
#Passo 3: Selecione a opção de criar chat que deseja
#Passo 4: Coloque uma porta desejada, acho que entre #1025 a 49152 não da erro, ainda falta previnir erro disto
#Passo 5: Escolha uma senha

run = []

def Tratar_janela_erro(window_antiga,dimensoes,qtd_label,text_l,font_l,pady_l):#Nesta função é automatizado o processo de criar uma janela de erro, até mesmo sobre colocar o texto no label
    window_antiga.withdraw()
    window_erro = Gerenciar_Janela('Crie',{'dimensoes' : dimensoes, 'alinhamento_tela': 'centralizado'},"Aviso")
    for i in range(qtd_label):
        ttk.Label(window_erro,text=f'{text_l[i]}',font=font_l[i],background='white').pack(pady=pady_l[i])
    window_erro.protocol("WM_DELETE_WINDOW", lambda:(
    window_antiga.deiconify(),
    window_erro.destroy() ))


def Gerenciar_Janela(comando,config_janela,titulo,window_reserva=None):
    def Destroir_widgets():
        for widget in window.winfo_children():
            widget.destroy()
        return

    def Janela_title_geometry(janela_personalizada,config_janela): #Aqui será configurado o titulo e tamanho da janela
        x,y = 0,0
        if config_janela['alinhamento_tela'] == 'centralizado':
            # Calculando a posição central da tela
            screen_width = janela_personalizada.winfo_screenwidth()
            screen_height = janela_personalizada.winfo_screenheight()
            x = (screen_width - 400) // 2
            y = (screen_height - 200) // 2

        janela_personalizada.geometry(f"{config_janela['dimensoes']}+{x}+{y}")
        janela_personalizada.title(titulo)

        return janela_personalizada
    

    if comando == 'Crie' and len(run) == 0: #Se for a primeira vez que pede para criar uma janela
        global window
        window = ttk.Window()
        run.append(window)
    elif comando == 'Delete e crie':
        Destroir_widgets()
    elif comando == 'Crie' and len(run) >= 1:
        window_reserva = ttk.Window()  
        window_reserva = Janela_title_geometry(window_reserva,config_janela)
        run.append(window_reserva)
        return window_reserva

    if comando == 'Crie' or comando == 'Delete e crie':
        window = Janela_title_geometry(window,config_janela) 
        return window        

    if comando == 'Crie-Toplevel':
        window_Toplevel = ttk.Toplevel()    # Usa Toplevel em vez de Window, pois cria uma janela mais independente, e mais previnida de erros 
        window.withdraw()                   # Usa witdraw em vez de destroy, pois previne erros (isso faz a tela não aparecer para o usuario em vez de destroila)
       
        window_Toplevel = Janela_title_geometry(window_Toplevel,config_janela)  
        return window_Toplevel
 
 #A função tem como objetivo que seja passado uma string e ela retorne se os parametros de analise da string estão aceitos, por exemplo, o usuário não pode colocar um caractere alfabetico no input de ipv4 do server ou de porta do servidor


def Tratar_input(string,id,window_antiga,pode_numero,pode_char_esp,pode_char_alfa,limite_max_char,limite_min_char,numero_minimo):
    validação = True
    validação_numero = validação_char_esp = validação_char_alfa = validação_max_limite = validação_min_limite = validação_vazia = validacao_numero_minimo  = ''

    string = string.strip()
    if string == '':
        validação = False
        validação_vazia = 'Erro'
    if (pode_numero == False) and (any(char.isdigit() for char in string)): #Na sequencia de ifs abaixo, é comparado se a string está conforme necessário
        validação = False
        validação_numero = 'Erro'
    if (pode_char_esp == False) and (any(not char.isalnum() and not char.isspace() and not char == '.' for char in string)):
        validação = False
        validação_char_esp = 'Erro'
    if (pode_char_alfa == False) and (any(char.isalpha() for char in string)):    
        validação = False
        validação_char_alfa = 'Erro'
    if (limite_max_char != False) and (limite_max_char < len(string)):
        validação = False
        validação_max_limite = 'Erro'
    if (limite_min_char != False) and (limite_min_char > len(string)):
        validação = False
        validação_min_limite = 'Erro'
    if (numero_minimo != False) and ((string =='')  or (int(string) <= numero_minimo) ):
        validação = False
        validacao_numero_minimo = 'Erro'
    if validação == False: #Abaixo será criado uma janela personalizada baseada no erro especifico do usuário ao colocar o input não compativel
        window_antiga.withdraw() 
        window_erro = Gerenciar_Janela('Crie',{'dimensoes' : '325x150', 'alinhamento_tela': 'centralizado'},"Aviso")
        ttk.Label(window_erro,text='Aviso!!',font=('Arial',13, 'bold'),background='white').pack(pady=(5))
        if validação_numero == 'Erro':
            ttk.Label(window_erro,text='- Números não são permitidos!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        if validação_char_esp == 'Erro':
            ttk.Label(window_erro,text='- Caracteres especiais não são permitidos!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        if validação_char_alfa == 'Erro':
            ttk.Label(window_erro,text='- Caracteres do alfabeto não são permitidos!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        if validacao_numero_minimo == 'Erro':
            ttk.Label(window_erro,text=f'- Número do(a) {id} precisa ser acima de {numero_minimo}',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        if validação_max_limite == 'Erro':     
            ttk.Label(window_erro,text=f'- É necessário que o(a) {id} contenha até {limite_max_char} caracteres!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        if validação_min_limite == 'Erro':
            ttk.Label(window_erro, text=f'- É necessário que o(a) {id} tenha no minimo {limite_min_char} de caracteres!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        if validação_vazia == 'Erro':
            ttk.Label(window_erro,text=f'- É necessário que o(a) {id} contenha até {limite_max_char} caracteres!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        window_erro.protocol("WM_DELETE_WINDOW", lambda:(
            window_antiga.deiconify(),
            window_erro.destroy() )) # Adiciona um evento ao fechar a janela
        return string, False
    return string, True


def Chat_App(nmr_porta,senha,qtd_pessoas,nome_gp,window_antiga,pedido):
    def Fechar_janela_chat():
        chat_window.destroy() #Isso aqui destroy a chat_window apenas na primeira thread
        msg_close = "Protocolo_close"
        Enviar_mensagem(msg_close) #Avisa ao server, que o client desconectou
        Thread_receber.join()
        time.sleep(1) #Coloquei isso para resolver um bug em que era enviado a msg ao server que fechou a conexão, porém a msg nem chegava ao server, e a linha cliente_socket.close(), já fechava o socket antes da msg chegar no server 
        cliente_socket.close() #Cliente se desconecta de fato

    def Enviar_mensagem(msg=None,admin = None):
        if msg == "Protocolo_close": #Isso é para avisar o servidor que o cliente fechou a janela e se desconectará
            cliente_socket.send(msg.encode())
            return
        mensagem = f"{msg} {format(math.pi, '.10f')} {name}" #Isso é para separar as diferentes informações passadas em uma só mensagem, os 10 numeros do pi foi escolhido como meio de separação de mensagens, uma vez que dificilmente alguem escreveria isso no chat
        if mensagem: #Abaixo fará a cifragem da mensagem, e depois o envio ao servidor
            mensagem = emoji.demojize(mensagem) 
            if admin != None:
                cifra = f'{admin}{rsa.cifrar(mensagem,28837,40301)}'
            else:
                cifra = rsa.cifrar(mensagem,28837,40301) #Está com chave já selecionada, podemos aleatorizar depois
            cliente_socket.send(cifra.encode()) #a mensagem é enviada nessa linha ao servidor, usando sockets
            message_input.delete(0, tk.END)
        widget_emoji(chat_display,'Desapareça')

    def Enviar_Arquivo():
        filepath = filedialog.askopenfilename()
        filename = os.path.basename(filepath)
        tamanho_arquivo = os.path.getsize(filepath)

        cliente_socket.send( (f'Tamanho do arquivo:{tamanho_arquivo}').encode() )
        time.sleep(1) #Só para garantir que o server está aguardando o envio

        with open(filepath,'rb') as file: #irá abrir o arquivo, em leitura de bytes
            while True:
                data = file.read(1024)
                if not data:
                    break
                cliente_socket.sendall(data)    
        Enviar_mensagem(f'{filename}',f'arquivo {tamanho_arquivo} ')

    def Bind_tag_arquivo(tag,tamanho_arquivo):
        def mostrar_info_arquivo(event,info):
            global popup_window
            popup_window = tk.Toplevel(chat_box)
            popup_window.wm_overrideredirect(True)  # Remove a decoração da janela
            popup_window.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")  # Posiciona a janela próxima ao cursor
            if info <1000:
                label_info = tk.Label(popup_window, text=f'{info:.0f}KB', font=("Arial", 10))
            else:
                info = info/1000
                label_info = tk.Label(popup_window, text=f'{info:.3f}MB', font=("Arial", 10))
            label_info.pack()
        
        def esconder_info_arquivo(event):
            popup_window.destroy()
        
        def baixar_arquivo(event,v):
            print('baixaagora',v)

        chat_display.tag_bind(tag,'<Button-1>', lambda event: baixar_arquivo(event,tag))
        chat_display.tag_bind(tag, '<Enter>', lambda event: mostrar_info_arquivo(event, (tamanho_arquivo)))
        chat_display.tag_bind(tag, '<Leave>', esconder_info_arquivo)

    def Receber_mensagens():
        rodar = True
        qtd_arquivos = 0
        while rodar:
            try:
                mensagem = cliente_socket.recv(1024).decode() #Decodificará a mensagem por padrão do servidor
                is_arquivo = False
                if 'arquivo' in mensagem:
                    mensagem = mensagem.split(' ')
                    tamanho_arquivo = int(mensagem[1])/1024
                    mensagem = mensagem[2]
                    is_arquivo = True
                msg_decifrada = rsa.decifrar(mensagem,40301,12973) #Está com chave já selecionada, podemos aleatorizar depois
                msg_decifrada = msg_decifrada.split(f" {format(math.pi, '.10f')} ")
                if msg_decifrada[0]: 
                    if chat_window.winfo_exists(): #Checa se ainda existe o chat_window, pode ter sido fechado pela primeira tread 
                        nome = msg_decifrada[1]
                        chat_display.configure(state='normal')
                        msg_texto = emoji.emojize(msg_decifrada[0])

                        if nome == name: #Se o nome da pessoa for o do próprio cliente, faz configuração diferencial na amostra da mensagem no chat
                            for i in msg_texto:#O looping é feito para analisar se há emoji na mensagem colocada, pois caso afirmativo é colocado um estilo de font diferenciado ao emoji
                                if emoji.is_emoji(i):
                                    chat_display.insert(tk.END, i, 'right emoticon_tag')
                                else:
                                    if is_arquivo == True: #Se for o texto do arquivo, terá um estilo diferente (para permitir mudança de cor e de funcionalidades como:)
                                        chat_display.insert(tk.END, i, f'right arquivo {qtd_arquivos}')
                                        qtd_arquivos += 1
                                        Bind_tag_arquivo(qtd_arquivos,tamanho_arquivo)
                                    else:
                                        chat_display.insert(tk.END, i, 'right')
                            chat_display.insert(tk.END, '\n', 'right')
                        else:
                            primeira_iteracao = True
                            for i in msg_texto: #O looping é feito para analisar se há emoji na mensagem colocada, pois caso afirmativo é colocado um estilo de font diferenciado ao emoji
                                if primeira_iteracao == True:
                                    chat_display.insert(tk.END, f'{nome}: ', 'left')
                                    primeira_iteracao = False
                                if emoji.is_emoji(i):
                                    chat_display.insert(tk.END, i, 'left emoticon_tag')
                                else:
                                    if is_arquivo == True:
                                        chat_display.insert(tk.END, i, 'left arquivo')
                                    else:
                                        chat_display.insert(tk.END, i, 'left')
                            chat_display.insert(tk.END, '\n', 'left')
                        Scroll_to_bottom()
                        chat_display.configure(state='disabled')
                    else:
                        rodar = False
            except ConnectionError:
                break

    def Limpar_chat():
        chat_display.configure(state='normal')
        chat_display.delete(1.0, tk.END)
        chat_display.configure(state='disabled')
        
    def Scroll_to_bottom():
        """Rola o chat para baixo."""
        chat_display.yview_moveto(1.0)

    def widget_emoji(window,solicitacao, event=None):
        def emoji_click(emoji): #Coloca o emoji clicado no input do usuario
            message_input.insert(tk.END, emoji)

        def classe_click(classe,event=None): #Mostra os emojis da classe, ao clicar no emoji de exemplo
            for i in range(len(classe_emoji_menores_list)):
                if classe == i: #Coloca a borda no emoji de exemplo, e tira do que não foram clicados
                    emoji_de_exemplo_list[i].configure(border = 1, relief = 'solid')
                else:
                    emoji_de_exemplo_list[i].configure(border = 0,relief = 'flat')

                for j in range(len(classe_emoji_menores_list[i])): # Looping em cada emoji menor para que mostre cada um na tela
                    if classe == i:
                        classe_emoji_menores_list[i][j].pack(side='left')
                    else:
                        classe_emoji_menores_list[i][j].pack_forget()

        def carregar_emoji():
            def cada_emoji_unico(classe,frame,nmr_classe):
                Emoji_list = emoji.emojize(Emoticons.Meus_emoji(classe)) #Pega todos os emojis menores do nosso modulo de emoticon
                c = 0
                copia_frame = frame
                for emoji_icon in Emoji_list: #Neste looping é carregado todos os emojis do nosso modulo de emoticon, e mostra a da primeira classe, e oculta as demais
                    if emoji.is_emoji(emoji_icon):
                        emoji_label_icon = tk.Label(copia_frame, text=emoji_icon, font=('Arial',16))
                        emoji_label_icon.bind("<Button-1>",lambda event, e =emoji_icon: emoji_click(e))
                        emoji_label_icon.pack()
                        c +=1
                        if c == 6:
                            c = 0
                            emoji_minor_frame = tk.Frame(emoji_frame)
                            emoji_minor_frame.pack(side='left')

                            copia_frame = emoji_minor_frame
                            classe_emoji_menores_list[nmr_classe].append(emoji_minor_frame)
                            if not nmr_classe == 0:
                                emoji_minor_frame.pack_forget()

            global emoji_minor_frame_smile, emoji_minor_frame_mao #Abaixo é programado os Labels do emoji classe (o de exemplo)
            emoji_minor_frame_smile = tk.Frame(emoji_frame)
            emoji_minor_frame_smile.pack(side='left')
            emoji_minor_frame_mao = tk.Frame(emoji_frame)
            emoji_minor_frame_pessoas = tk.Frame(emoji_frame)
            emoji_minor_frame_animais = tk.Frame(emoji_frame)
            emoji_minor_frame_alimentos = tk.Frame(emoji_frame)

            #Abaixo faz chamada para carregar os emojis menores, e também é colocado na lista que contém todos os emojis menores utilizados no código em uma unica array
            classe_emoji_menores_list.append([emoji_minor_frame_smile])
            cada_emoji_unico('Smile' , emoji_minor_frame_smile , 0)
            classe_emoji_menores_list.append([emoji_minor_frame_mao])
            cada_emoji_unico('Mão e corpo' , emoji_minor_frame_mao, 1)
            classe_emoji_menores_list.append([emoji_minor_frame_pessoas])
            cada_emoji_unico('Pessoas no geral' , emoji_minor_frame_pessoas, 2)
            classe_emoji_menores_list.append([emoji_minor_frame_animais])
            cada_emoji_unico('Animais e natureza' , emoji_minor_frame_animais, 3)
            classe_emoji_menores_list.append([emoji_minor_frame_alimentos])
            cada_emoji_unico('Alimentos' , emoji_minor_frame_alimentos, 4)
            
        #Será executado o if abaixo, apenas uma vez, quando o chat_app for executado.
        #Basicamente no if abaixo, ele criará tanto os emojis de exemplo, quanto os menores, e pedirá para carregar ambos na função acima.
        #Os outros elif, são para mostrar e ocultar os emojis da tela conforme as ações do usuario (que dispararam a chamada dessa função)
        if Abrir_emojis[0] == 'Não aberto' and solicitacao == 'Abrir':
            Abrir_emojis[0] = 'Invisivel' 
            global emoji_frame           
            emoji_frame = tk.Frame(window)
            emoji_frame.pack(side='left')

            emoji_classe_frame = tk.Frame(emoji_frame)
            emoji_classe_frame.pack(side='left',padx=(5,0))
            
            classe_emoji_menores_list = []
            emoji_de_exemplo_list = []
            emoji_classe_label_rosto = tk.Label(emoji_classe_frame,text=emoji.emojize(':thinking_face:'),font=('Arial',20),border=1,relief="solid")
            emoji_classe_label_rosto.pack()
            emoji_classe_label_rosto.bind("<Button-1>",lambda event, e = 0: classe_click(e))
            emoji_de_exemplo_list.append(emoji_classe_label_rosto)

            emoji_classe_label_mao = tk.Label(emoji_classe_frame,text=emoji.emojize(':thumbs_up:'),font=('Arial',20))
            emoji_classe_label_mao.pack()
            emoji_classe_label_mao.bind("<Button-1>",lambda event, e = 1: classe_click(e)) 
            emoji_de_exemplo_list.append(emoji_classe_label_mao)

            emoji_classe_label_corpo = tk.Label(emoji_classe_frame,text=emoji.emojize(':person_gesturing_NO:'),font=('Arial',20))
            emoji_classe_label_corpo.pack()
            emoji_classe_label_corpo.bind("<Button-1>",lambda event, e = 2: classe_click(e))
            emoji_de_exemplo_list.append(emoji_classe_label_corpo)

            emoji_classe_label_animal = tk.Label(emoji_classe_frame,text=emoji.emojize(':dog_face:'),font=('Arial',20))
            emoji_classe_label_animal.pack()
            emoji_classe_label_animal.bind("<Button-1>",lambda event, e = 3: classe_click(e))
            emoji_de_exemplo_list.append(emoji_classe_label_animal)

            emoji_classe_label_comida = tk.Label(emoji_classe_frame,text=emoji.emojize(':beer_mug:'),font=('Arial',20))
            emoji_classe_label_comida.pack()
            emoji_classe_label_comida.bind("<Button-1>",lambda event, e = 4: classe_click(e))
            emoji_de_exemplo_list.append(emoji_classe_label_comida)

            carregar_emoji()
            emoji_frame.pack_forget()
        elif (Abrir_emojis[0] == 'Aberto' and solicitacao == 'Desapareça') or (Abrir_emojis[0] == 'Aberto' and solicitacao == 'Abrir'):
            Abrir_emojis[0] = 'Invisivel'
            emoji_frame.pack_forget()
        elif Abrir_emojis[0] == 'Invisivel' and solicitacao == 'Abrir':
            Abrir_emojis[0] = 'Aberto'
            emoji_frame.pack(side='left')

    def apagar_emoji(entry): #Essa função é necessário pois o GUI em questão não lida corretamente com o apagar de emojis no input, ao ser apagado de forma crua ele deixa um caractere invalido no lugar do emoji
        if len(entry.get()) > 0 and emoji.is_emoji(entry.get()[-1]): #Aqui verificamos se há emoji presente no input, caso sim, é salvo o texto sem o ultimo caractere, e é colocado um caractere não emoji no final
            entry_text = entry.get()                                 #Portanto, quando acabar a função, será a pagado o caractere não emoji pelo bind padrão em que o backspace apaga o ultimo char, porém o ultimo char agora é um char que não causa problemas
            new_text = entry_text[:-1]  # Obtém todo o texto, exceto o último caractere
            new_text +='a'
            entry.delete(0, tk.END)  # Limpa o texto atual
            entry.insert(0, new_text)  # Define o novo texto no Entry  
        

    nmr_porta, validação_porta = Tratar_input(nmr_porta,'porta',window_antiga,True,False,False,5,4,4000)
    if validação_porta == True:
        senha, validação_senha = Tratar_input(senha,'senha',window_antiga,True,True,True,8,3,False)
    if validação_porta == True and validação_senha == True:
        if qtd_pessoas != False:
            qtd_pessoas, validação_qtd_p = Tratar_input(qtd_pessoas,'quantidade de pessoas',window_antiga,True,False,False,2,False,1)
            nome_gp, validação_nome_gp = Tratar_input(nome_gp,'nome do grupo',window_antiga,True,True,True,30,1,False)
        else:
            validação_qtd_p = True
            validação_nome_gp = True
    if validação_porta == True and validação_senha == True and validação_qtd_p == True and validação_nome_gp == True:
        qtd_pessoas = int(qtd_pessoas)

        if nome_gp != False:
            #Abaixo mandamos para o server, a mensagem contendo os 5 parametros abaixo, para o chat criar um novo chat lá com base nessas informações
            message = f'{nmr_porta}+{senha}+{qtd_pessoas}+{pedido}+{nome_gp}'
            connection.send(message.encode())
        else:
             #Abaixo mandamos para o server, a mensagem contendo os 5 parametros abaixo, para o chat criar um novo chat lá com base nessas informações
            message = f'{nmr_porta}+{senha}+{qtd_pessoas}+{pedido}+{nome_gp}'
            connection.send(message.encode())

        escutando = True
        connection.settimeout(4) #Escuta por no maximo 4s se conseguiu fazer conexão com o server
        while escutando: #Isso aqui é para ver se o servidor aceita mais uma conexão no chat, ou se já esta cheio ou se a senha está errada
            try:
                confirmacao = connection.recv(1024).decode()
                if confirmacao == 'Recusado, Grupo nao existe':
                    escutando = False
                    conexao_validacao = False
                    Tratar_janela_erro(window_antiga, '400x127', 2, ['Aviso!!','- O grupo em questão não existe!']
                                        , [('Arial',13, 'bold'),('Arial',11)] , [(5),(0)])
                    Inicio()
                    return
                elif confirmacao == 'Recusado, Grupo esta cheio':
                    escutando = False
                    conexao_validacao = False
                    Tratar_janela_erro(window_antiga, '400x127', 2, ['Aviso!!','- O grupo em questão está cheio!']
                                        , [('Arial',13, 'bold'),('Arial',11)] , [(5),(0)])
                    Inicio()
                    return
                elif confirmacao == 'Recusado, Grupo já criado':
                    escutando = False
                    conexao_validacao = False
                    Tratar_janela_erro(window_antiga, '400x127', 2, ['Aviso!!','- O grupo em questão já foi criado!']
                                        , [('Arial',13, 'bold'),('Arial',11)] , [(5),(0)])
                    Inicio()
                    return
                elif confirmacao == 'Recusado, senha está errada!':
                    escutando = False
                    conexao_validacao = False
                    Tratar_janela_erro(window_antiga, '400x127', 2, ['Aviso!!','- A senha está incorreta!']
                                        , [('Arial',13, 'bold'),('Arial',11)] , [(5),(0)])
                    return
                elif confirmacao == 'Recusado, Porta nao disponivel':
                    escutando = False
                    conexao_validacao = False
                    Tratar_janela_erro(window_antiga, '400x127', 2, ['Aviso!!','- A porta escolhida está indisponivel!']
                                        , [('Arial',13, 'bold'),('Arial',11)] , [(5),(0)])
                    return
                confirmacao = confirmacao.split('+')
                if confirmacao[0] == 'Autorizado':
                    nome_grupo = confirmacao[1]
                    escutando = False
                    conexao_validacao = True
                    break
            except (ConnectionError,ConnectionRefusedError, TimeoutError, OSError, BlockingIOError, socket.error, socket.timeout) as a:
                    print(f'Erro: {a}') #Pode apagar isso antes de entregar a aps
                    escutando = False
                    conexao_validacao = False
                    return
        connection.settimeout(None) #Desfaz o escuta até no max 4s    
            
        
        if conexao_validacao == True: #Caso a conexão de entrar/criar chat for aceita, será configurado todo os detalhes do chat
            cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente_socket.connect((ip_server, int(nmr_porta)))
            chat_window = Gerenciar_Janela('Crie-Toplevel',
                                        {'dimensoes': '800x525','alinhamento_tela': 'nenhum' },
                                        f'Chat Online - {nome_grupo}')#colocar nome de quem conectou junto

            chat_box = tk.Frame(chat_window)
            input = tk.Frame(chat_window)

            chat_display = ttk.Text(chat_box,font=("Arial", 12),wrap='word',state='disabled',height=10,width=120)
            chat_display.pack(side = 'left',padx=10)
            # Configuração de tags para alinhamento
            chat_display.tag_configure('right', justify='right')
            chat_display.tag_configure('left', justify='left')
            chat_display.tag_configure('emoticon_tag', font=('Arial',20))
            chat_display.tag_configure('arquivo', foreground='red', font=('bold'))  # Definindo a cor do texto (do arquivo) de vermelho


            scrollbar = ttk.Scrollbar(chat_box, command=chat_display.yview)
            scrollbar.pack(side='right', padx=10, fill='y')  # fill='y' para preencher a altura disponível

            message_input = ttk.Entry(input, width=30)
            message_input.pack(side='left',padx=10)
            message_input.bind('<BackSpace>', lambda event, entry=message_input: apagar_emoji(entry))


            emoji_text = emoji.emojize(':slightly_smiling_face:') #O texto de emoji ao lado do input do usuario se torna um botão que mostra os emojis disponiveis para serem rapidamente usados
            emoji_label = ttk.Label(input, text=emoji_text,font=('Arial',32))
            emoji_label.pack(side='left')
            Abrir_emojis = ['Não aberto']
            emoji_label.bind("<Button-1>", lambda event: widget_emoji(chat_window,'Abrir', event))

            transf_arq = ttk.Button(input, text="Transf. Arquivo", command=Enviar_Arquivo)
            transf_arq.pack(side='left',padx=7)

            send_button = ttk.Button(input, text="Enviar", command=lambda: Enviar_mensagem(message_input.get()))
            send_button.pack(side='left',padx=8)
            message_input.bind("<Return>", lambda event: send_button.invoke())

            clear_button = ttk.Button(input, text="Limpar", command=Limpar_chat)
            clear_button.pack(side='left',padx=7)

            chat_box.pack(fill='x', padx=10, pady=10)
            input.pack(fill='x', padx=10, pady=10) 

            widget_emoji(chat_window,'Abrir')

            Thread_receber = threading.Thread(target=Receber_mensagens) #É iniciado uma thread para rodar separadamente no aguardo de mensagens enviadas pelo servidor
            Thread_receber.start()
            chat_window.protocol("WM_DELETE_WINDOW", lambda: Fechar_janela_chat())
        else:
            cliente_socket.close()


def config_chat(box,conexao,dimensoes,diplomacia): #Nesta janela o usuario definirá a configuração do chat escolhido
    window = Gerenciar_Janela('Delete e crie',
                     {'dimensoes' : dimensoes, 'alinhamento_tela': 'centralizado'}, #Alterar largura
                     'Configuração - Chat')
    
    box_voltar = tk.Frame(window)
    box_voltar.pack(side='left',fill='y')
    box = tk.Frame(window)
    box.pack()    
    box2 = tk.Frame(box)
    box2.pack()
    box3 = tk.Frame(box)
    box3.pack()

    style = ttk.Style()
    style.configure('Vertical.TButton',font=('Consolas',12))


    btn_voltar = ttk.Button(box_voltar,text='V\nO\nL\nT\nA\nR',width=1, style='Vertical.TButton',command=Inicio)
    btn_voltar.pack(fill='y',expand=True)


    label_porta = ttk.Label(box2,text=f'{diplomacia} uma porta de rede: ')
    label_porta.pack(pady=(10,5))

    input_porta = ttk.Entry(box2)
    input_porta.pack()
    
    label_senha = ttk.Label(box3,text=f'{diplomacia} a senha da rede:')
    label_senha.pack(pady=(10,5))

    input_senha = ttk.Entry(box3)
    input_senha.pack()

    if conexao == 'criar grupo':
        label_qtd = ttk.Label(box3,text='Quantidade maxima de pessoas: ')
        label_qtd.pack(pady=(10,5))
        input_qtd_pessoa = ttk.Entry(box3)
        input_qtd_pessoa.pack()

        label_nome_gp = ttk.Label(box3,text='Escolha o nome do grupo: ')
        label_nome_gp.pack(pady=(10,5))
        input_nome_gp = ttk.Entry(box3)
        input_nome_gp.pack()

        confirm_button = ttk.Button(box,text='Confirmar', command=lambda: Chat_App(input_porta.get(),input_senha.get(),input_qtd_pessoa.get(),input_nome_gp.get(),window,'criar grupo'))
        input_nome_gp.bind("<Return>", lambda event: confirm_button.invoke())
    elif conexao == 'entrar em grupo':
        confirm_button = ttk.Button(box,text='Confirmar', command=lambda: Chat_App(input_porta.get(),input_senha.get(),False,False,window,'entrar grupo'))

    input_porta.focus_set()  # Define o foco para o Entry do nome do usuário
    input_senha.bind("<Return>", lambda event: confirm_button.invoke())#Ao pressionar enter, ele chamada a função do botão
    confirm_button.pack(pady=(15))

  
def Inicio(): #Nesta janela o usuário escolherá se prefere criar um grupo, entrar em um ou então algo direto com outra pessoa
    window = Gerenciar_Janela('Delete e crie',{'dimensoes':'300x150', 'alinhamento_tela' : 'centralizado'},'Escolha de chat')
    box = tk.Frame(window)
    box.pack()

    create_chat_button = ttk.Button(box, text='Criar um Grupo', width = 15, command= lambda:config_chat(box,'criar grupo','325x325','Escolha'))
    conect_chat_button = ttk.Button(box, text='Unir-se a Grupo', width = 15, command= lambda: config_chat(box,'entrar em grupo','300x200','Insira'))

    create_chat_button.pack(pady=(20,10))
    conect_chat_button.pack(padx=20)


def Conectar_ao_servidor(name_entry,window_antiga):
    def Teste_conexão(): #Abaixo, será feito uma tentativa de comunicação com o servidor
        global ip_server
        ip_server, validação = Tratar_input(input_ip_servidor.get(),'ipv4',window,True,False,False,15,7,False)
        if validação == True:
            try:
                global connection
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.connect((ip_server, 3000))

                Inicio()
            except (ConnectionRefusedError, TimeoutError, OSError) as e: #Tela de erro ao conectar ao ip do server
                Tratar_janela_erro(window,'400x127',3,['Aviso!!','- Não foi possivel estabelecer a conexão com o servidor!','- Verifique se o ipv4 do servidor foi digitado corretamente!'],
                                   [('Arial',13, 'bold'),('Arial',11),('Arial',11)],
                                   [(5),(0),(0)])
            return
    
    global name 
    name, validação = Tratar_input(name_entry,'nome',window_antiga,False,False,True,16,False,False)
    if validação == True: #Após validar o nome, pedirá o ipv4 do server
        window = Gerenciar_Janela('Delete e crie',{'dimensoes':'300x127', 'alinhamento_tela' : 'centralizado'},'Conecte ao Servidor')

        box = tk.Frame(window)
        box.pack()

        label_servidor = ttk.Label(box, text='Insira o ipv4 do servidor abaixo:')
        label_servidor.pack(pady=5)

        input_ip_servidor = ttk.Entry(box)
        input_ip_servidor.pack()

        button_servidor = ttk.Button(box, text='Confirmar',command= lambda:Teste_conexão())
        button_servidor.pack(pady=10)

        input_ip_servidor.focus_set()  # Define o foco para o Entry do nome do usuário
        input_ip_servidor.bind("<Return>", lambda event: button_servidor.invoke())


def Entrada(): #Criará a janela inicial, pedindo o nome do usuario como entrada, além de carregar os widgets necessários
    window = Gerenciar_Janela('Crie',
                              {'dimensoes':'300x127', 'alinhamento_tela' : 'centralizado'},
                              "Nome do Usuário")

    style = ttk.Style() 
    style.configure('TButton', font=('Arial', 10)) #ttk.button não aceita alterar font facilmente igual o label

    box = tk.Frame(window)
    box2 = tk.Frame(window)

    label = ttk.Label(box, text="Digite seu nome:",font=('Arial', 10, 'bold'))
    name_entry = ttk.Entry(box)
    enter_button = ttk.Button(box2, text="Confirmar", command=lambda: Conectar_ao_servidor(name_entry.get(),window)) #Programar que o comando 'enter' faça o mesmo que clicar no botao

    box.pack(pady=15)
    box2.pack()
    label.pack(side='left', padx=5)
    name_entry.pack(side='left')
    enter_button.pack()

    name_entry.focus_set()  # Define o foco para o Entry do nome do usuário
    name_entry.bind("<Return>", lambda event: enter_button.invoke()) #Ao pressionar enter, ele chamada a função do botão

    window.protocol("WM_DELETE_WINDOW", lambda: window.quit())  # Fechar janela principal sem erro
    window.mainloop()          

Entrada()
