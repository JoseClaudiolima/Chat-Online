from Lib import CriptografiaRSA as rsa

import tkinter as tk
import ttkbootstrap as ttk
import socket
import threading
import math

#Passo 1: Coloque o nome
#Passo 2: Coloque o ipv4 do server, aparece no terminal do server.py
#Passo 3: Selecione a opção de cima, a de baixo ainda não foi programada
#Passo 4: Coloque uma porta desejada, acho que entre #1025 a 49152 não da erro, mas talvez devemos pesquisar isso
#Passo 5: Colocaria a senha, porém ainda não tem funcionalidade para ela

#comando = 'Crie', Delete e crie, Crie-Toplevel
run = []
def Gerenciar_Janela(comando,config_janela,titulo,window_reserva=None):
    def Destroir_widgets():
        for widget in window.winfo_children():
            widget.destroy()
        return

    def Janela_title_geometry(janela_personalizada,config_janela):
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
    

    if comando == 'Crie' and len(run) == 0:
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
        #global window_Toplevel  #Acho que da para tirar isso
        window_Toplevel = ttk.Toplevel()    # Usar Toplevel em vez de Window, evita msg de erro (Cria uma janela mais independente, pelo que entendi) 
        window.withdraw()                   # usa witdraw em vez de destroy, evita msg de erro (isso faz a tela não aparecer para o usuario em vez de destroila)
       
        window_Toplevel = Janela_title_geometry(window_Toplevel,config_janela)  
        return window_Toplevel


def Tratar_input(string,id,window_antiga,pode_numero,pode_char_esp,pode_char_alfa,limite_max_char,limite_min_char):
    validação = True
    validação_numero = validação_char_esp = validação_char_alfa = validação_max_limite = validação_min_limite = validação_vazia  = ''

    string = string.strip()
    if string == '':
        validação = False
        validação_vazia = 'Erro'
    if (pode_numero == False) and (any(char.isdigit() for char in string)):
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

    if validação == False:
        window_antiga.withdraw() 
        window_erro = Gerenciar_Janela('Crie',{'dimensoes' : '300x127', 'alinhamento_tela': 'centralizado'},"Aviso")
        ttk.Label(window_erro,text='Aviso!!',font=('Arial',13, 'bold'),background='white').pack(pady=(5))
        if validação_numero == 'Erro':
            ttk.Label(window_erro,text='- Números não são permitidos!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        if validação_char_esp == 'Erro':
            ttk.Label(window_erro,text='- Caracteres especiais não são permitidos!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        if validação_char_alfa == 'Erro':
            ttk.Label(window_erro,text='- Caracteres do alfabeto não são permitidos!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
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


def Chat_App(nmr_porta,senha,qtd_pessoas,window_antiga):
    def Enviar_mensagem():
        mensagem = f"{message_input.get()} {format(math.pi, '.10f')} {name}"
        if mensagem:
            cifra = rsa.cifrar(mensagem,28837,40301) #Está com chave já selecionada, podemos aleatorizar depois
            cliente_socket.send(cifra.encode())
            message_input.delete(0, tk.END)

    def Receber_mensagens():
        while True:
            try:
                mensagem = cliente_socket.recv(1024).decode()
                msg_decifrada = rsa.decifrar(mensagem,40301,12973) #Está com chave já selecionada, podemos aleatorizar depois
                msg_decifrada = msg_decifrada.split(f" {format(math.pi, '.10f')} ")
                if msg_decifrada[0]:
                    nome = msg_decifrada[1]
                    chat_display.configure(state='normal')

                    if nome == name:
                        chat_display.insert(tk.END, f'{msg_decifrada[0]}\n', 'right')
                    else:
                        chat_display.insert(tk.END, f'{nome}: {msg_decifrada[0]}\n', 'left')
                    Scroll_to_bottom()
                    chat_display.configure(state='disabled')
            except ConnectionError:
                break

    def Limpar_chat():
        chat_display.configure(state='normal')
        chat_display.delete(1.0, tk.END)
        chat_display.configure(state='disabled')
        
    def Scroll_to_bottom():
        """Rola o chat para baixo."""
        chat_display.yview_moveto(1.0)

    nmr_porta, validação_a = Tratar_input(nmr_porta,'porta',window_antiga,True,False,False,5,4)
    if validação_a == True:
        senha, validação_b = Tratar_input(senha,'senha',window_antiga,True,True,True,8,3)
    if validação_a == True and validação_b == True:
        #Abaixo a gente manda para o server, a mensagem contendo os 3 parametros abaixo, para o chat criar um novo chat lá com base nessas info
        message = f'{nmr_porta}+{senha}+{qtd_pessoas}'
        connection.send(message.encode())

        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((ip_server, int(nmr_porta)))
        

        chat_window = Gerenciar_Janela('Crie-Toplevel',
                                    {'dimensoes': '800x500','alinhamento_tela': 'nenhum' },
                                    f'Chat Online - {name} e #cliente que conecta junto')#colocar nome de quem conectou junto

        chat_box = tk.Frame(chat_window)
        input = tk.Frame(chat_window)

        chat_display = ttk.Text(chat_box,wrap='word',state='disabled',height=10,width=120)
        chat_display.pack(side = 'left',padx=10)
        # Configuração de tags para alinhamento
        chat_display.tag_configure('right', justify='right')
        chat_display.tag_configure('left', justify='left')

        scrollbar = ttk.Scrollbar(chat_box, command=chat_display.yview)
        scrollbar.pack(side='right', padx=10, fill='y')  # fill='y' para preencher a altura disponível

        message_input = ttk.Entry(input, width=30)
        message_input.pack(side='left',padx=10)

        send_button = ttk.Button(input, text="Enviar", command=Enviar_mensagem)
        send_button.pack(side='left',padx=8)

        clear_button = ttk.Button(input, text="Limpar", command=Limpar_chat)
        clear_button.pack(side='left',padx=7)

        chat_box.pack(fill='x', padx=10, pady=10)
        input.pack(fill='x', padx=10, pady=10) 
        threading.Thread(target=Receber_mensagens).start() 


def direct_chat(box):
    window = Gerenciar_Janela('Delete e crie',
                     {'dimensoes' : '300x200', 'alinhamento_tela': 'centralizado'}, #Alterar largura
                     'Configuração - Chat-direto')
    
    box = tk.Frame(window)
    box.pack()    
    box2 = tk.Frame(box)
    box2.pack()
    box3 = tk.Frame(box)
    box3.pack()


    label_porta = ttk.Label(box2,text='Escolha uma porta de rede: ')
    label_porta.pack(pady=(10,5))

    input_porta = ttk.Entry(box2)
    input_porta.pack()
    
    label_senha = ttk.Label(box3,text='Escolha a senha da rede:')
    label_senha.pack(pady=(10,5))

    input_senha = ttk.Entry(box3)
    input_senha.pack()

    confirm_button = ttk.Button(box,text='Confirmar', command=lambda: Chat_App(input_porta.get(),input_senha.get(),2,window))
    confirm_button.pack(pady=(15))

  
def Inicio(): #Programar se o usuario clicar em criar grupo
    window = Gerenciar_Janela('Delete e crie',{'dimensoes':'300x127', 'alinhamento_tela' : 'centralizado'},'Escolha de chat')
    box = tk.Frame(window)
    box.pack()

    direct_chat_button = ttk.Button(box, text='Conexão direta',command= lambda:direct_chat(box))
    multiple_chat_button = ttk.Button(box, text='Criar Grupo')

    direct_chat_button.pack(pady=(20,10))
    multiple_chat_button.pack()


def Conectar_ao_servidor(name_entry,window_antiga):
    def Teste_conexão(): #Adicionar tela de loading
        global ip_server
        ip_server, validação = Tratar_input(input_ip_servidor.get(),'ipv4',window,True,False,False,15,7)
        if validação == True:
            try:
                global connection
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #Adicionar tela de loading aqui antes de tentar conexão, atualmente o app trava se colocar invalido
                connection.connect((ip_server, 3000))

                Inicio()
            except (ConnectionRefusedError, TimeoutError, OSError):
                #Adicionar tela de erro
                print(f'Ip de servidor está errado!')
            return
    
    global name #Levar essa verificação para outro lugar
    name, validação = Tratar_input(name_entry,'nome',window_antiga,False,False,True,16,False)
    if validação == True:
        window = Gerenciar_Janela('Delete e crie',{'dimensoes':'300x127', 'alinhamento_tela' : 'centralizado'},'Conecte ao Servidor')

        box = tk.Frame(window)
        box.pack()

        label_servidor = ttk.Label(box, text='Insira o ipv4 do servidor abaixo:')
        label_servidor.pack(pady=5)

        input_ip_servidor = ttk.Entry(box)
        input_ip_servidor.pack()

        button_servidor = ttk.Button(box, text='Confirmar',command= lambda:Teste_conexão())
        button_servidor.pack(pady=10)


def Entrada():
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

    window.mainloop()
    window.protocol("WM_DELETE_WINDOW", lambda: window.quit())  # Fechar janela principal sem erro
          

if __name__ == '__main__': #Executa apenas quando é o arquivo é aberto 
    Entrada()
