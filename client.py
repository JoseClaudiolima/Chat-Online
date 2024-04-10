import tkinter as tk
from Lib import CriptografiaRSA as rsa
import ttkbootstrap as ttk
import socket
import threading
import math

def Entrada_de_nomeapp(window):

    def iniciar_chat(window,name_entry):
        nome_usuario = name_entry.get()
        if nome_usuario:
            window.withdraw()  # Esconde a janela de entrada de nome
            chat_window = tk.Toplevel()  # Usar Toplevel em vez de Window
            #chat_window.geometry(f'440x250+{x}+{y}')    
            chat_window.geometry(f'800x500+{x}+{y}')
            ChatApp(chat_window, nome_usuario)  

    window.title("Nome do Usuário")

    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 10, 'bold'))
    style.configure('TButton', font=('Arial', 10))

    box = tk.Frame(window)

    label = ttk.Label(box, text="Digite seu nome:")
    name_entry = ttk.Entry(box)
    enter_button = ttk.Button(window, text="Confirmar", command=lambda: iniciar_chat(window,name_entry))

    box.pack(pady = 15)
    label.pack(side = 'left', padx = 5)
    name_entry.pack(side = 'right')
    enter_button.pack()
          

def ChatApp(window, nome_usuario):
    def Enviar_mensagem():
        ''' Abaixo tem 3 parametros: 
            I. a mensagem em si; 
            II. o delimitador de paraemtro (para separar no recebimento de mensagem, qual é cada parametro);
            III. o nome do cliente.'''
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

    name = nome_usuario
    window.title(f"Chat Online - {name}")

    chat_box = tk.Frame(window)
    input = tk.Frame(window)

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

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #socket.connect(('192.168.15.41', 3000))
    cliente_socket.connect(('192.168.15.162', 3000))
    
    threading.Thread(target=Receber_mensagens).start()       


if __name__ == '__main__':
    Start_window = ttk.Window()

    # Calculando a posição central da tela
    screen_width = Start_window.winfo_screenwidth()
    screen_height = Start_window.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 200) // 2
    Start_window.geometry(f'300x127+{x}+{y}')

    entry_app = Entrada_de_nomeapp(Start_window)
    Start_window.mainloop()
