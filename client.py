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

#comando = criar janela ou delete e crie
def Gerenciar_Janela(comando,config_janela,titulo):
    def Destroir_widgets():
        for widget in window.winfo_children():
            widget.destroy()
        return

    def Janela_title_geometry(janela_personalizada,config_janela):
        x,y = 0,0
        if config_janela is None:
            config_janela = {'dimensoes' : '300x127', 'alinhamento_tela': 'centralizado'}

        if config_janela['alinhamento_tela'] == 'centralizado':
            # Calculando a posição central da tela
            screen_width = janela_personalizada.winfo_screenwidth()
            screen_height = janela_personalizada.winfo_screenheight()
            x = (screen_width - 400) // 2
            y = (screen_height - 200) // 2

        janela_personalizada.geometry(f"{config_janela['dimensoes']}+{x}+{y}")
        janela_personalizada.title(titulo)

        return janela_personalizada
    

    if comando == 'Crie':
        global window
        window = ttk.Window()

    elif comando == 'Delete e crie':
        Destroir_widgets()

    if comando == 'Crie' or comando == 'Delete e crie':
        window = Janela_title_geometry(window,config_janela) 
        return window

    if comando == 'Crie-Toplevel':
        #global window_Toplevel  #Acho que da para tirar isso
        window_Toplevel = ttk.Toplevel()    # Usar Toplevel em vez de Window, evita msg de erro (Cria uma janela mais independente, pelo que entendi) 
        window.withdraw()                   # usa witdraw em vez de destroy, evita msg de erro (isso faz a tela não aparecer para o usuario em vez de destroila)
       
        window_Toplevel = Janela_title_geometry(window_Toplevel,config_janela)  
        return window_Toplevel

 

#fazendo assim para ir logo, dps junta o grupo com chat direto
def Chat_App(nmr_porta,senha,qtd_pessoas):
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

    #Abaixo a gente manda para o server, a mensagem contendo os 3 parametros abaixo, para o chat criar um novo chat lá com base nessas info
    message = f'{nmr_porta}+{senha}+{qtd_pessoas}'
    connection.send(message.encode())

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((ip_server, int(nmr_porta)))
    

    chat_window = Gerenciar_Janela('Crie-Toplevel',
                                   {'dimensoes': '800x500','alinhamento_tela': 'nenhum' },
                                   'Chat Online')  

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
                     {'dimensoes' : '300x200', 'alinhamento_tela': 'centralizado'},
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

    confirm_button = ttk.Button(box,text='Confirmar', command=lambda: Chat_App(input_porta.get(),input_senha.get(),2))
    confirm_button.pack(pady=(15))

  
def Inicio():
    window = Gerenciar_Janela('Delete e crie',None,'Escolha de chat')
    box = tk.Frame(window)
    box.pack()

    direct_chat_button = ttk.Button(box, text='Conexão direta',command= lambda:direct_chat(box))
    multiple_chat_button = ttk.Button(box, text='Criar Grupo')

    direct_chat_button.pack(pady=(20,10))
    multiple_chat_button.pack()


def Conectar_ao_servidor(name_entry):
    def Teste_conexão():
        global ip_server
        ip_server = input_ip_servidor.get()
        if ip_server == '':
            return
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
    

    global name
    name = name_entry.get()
    if name == '':
        return    

    window = Gerenciar_Janela('Delete e crie',None,'Conecte ao Servidor')

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
    style.configure('TLabel', font=('Arial', 10, 'bold'))
    style.configure('TButton', font=('Arial', 10))

    box = tk.Frame(window)
    box2 = tk.Frame(window)

    label = ttk.Label(box, text="Digite seu nome:")
    name_entry = ttk.Entry(box)
    enter_button = ttk.Button(box2, text="Confirmar", command=lambda: Conectar_ao_servidor(name_entry))

    box.pack(pady=15)
    box2.pack()
    label.pack(side='left', padx=5)
    name_entry.pack(side='left')
    enter_button.pack()

    window.mainloop()
    window.protocol("WM_DELETE_WINDOW", lambda: window.quit())  # Fechar janela principal sem erro
          

if __name__ == '__main__':
    Entrada()
