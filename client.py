import tkinter as tk
from Lib import CriptografiaRSA as rsa
import ttkbootstrap as ttk
import socket
import threading
import math

class NameEntryApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Nome do Usuário")

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10, 'bold'))
        self.style.configure('TButton', font=('Arial', 10))

        self.box = tk.Frame(window)

        self.label = ttk.Label(self.box, text="Digite seu nome:")
        self.name_entry = ttk.Entry(self.box)
        self.enter_button = ttk.Button(window, text="Confirmar", command=self.iniciar_chat)

        self.box.pack(pady = 15)
        self.label.pack(side = 'left', padx = 5)
        self.name_entry.pack(side = 'right')
        self.enter_button.pack()


    def iniciar_chat(self):
        nome_usuario = self.name_entry.get()
        if nome_usuario:
            self.window.withdraw()  # Esconde a janela de entrada de nome
            chat_window = tk.Toplevel()  # Usar Toplevel em vez de Window
            #chat_window.geometry(f'440x250+{x}+{y}')    
            chat_window.geometry(f'800x500+{x}+{y}')
            app = ChatApp(chat_window, nome_usuario)            

class ChatApp:
    def __init__(self, window, nome_usuario):
        
        self.name = nome_usuario
        self.window = window
        #self.window.resizable(False, False)
        self.window.title(f"Chat Online - {self.name}")

        #self.style = ttk.Style()
        #self.style.configure('TText', font=('Arial', 10))
        #self.style.configure('TButton', font=('Arial', 10))
        #self.style.configure('TEntry', font=('Arial', 10))  

        self.chat_box = tk.Frame(self.window)
        self.input = tk.Frame(self.window)

        self.chat_display = ttk.Text(self.chat_box,wrap='word',state='disabled',height=10,width=120)
        self.chat_display.pack(side = 'left',padx=10)
        # Configuração de tags para alinhamento
        self.chat_display.tag_configure('right', justify='right')
        self.chat_display.tag_configure('left', justify='left')

        self.scrollbar = ttk.Scrollbar(self.chat_box, command=self.chat_display.yview)
        self.scrollbar.pack(side='right', padx=10, fill='y')  # fill='y' para preencher a altura disponível

        self.message_input = ttk.Entry(self.input, width=30)
        self.message_input.pack(side='left',padx=10)

        self.send_button = ttk.Button(self.input, text="Enviar", command=self.enviar_mensagem)
        self.send_button.pack(side='left',padx=8)

        self.clear_button = ttk.Button(self.input, text="Limpar", command=self.limpar_chat)
        self.clear_button.pack(side='left',padx=7)

        self.chat_box.pack(fill='x', padx=10, pady=10)
        self.input.pack(fill='x', padx=10, pady=10)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 3000))

        threading.Thread(target=self.receber_mensagens).start()


    def enviar_mensagem(self):
        ''' Abaixo tem 3 parametros: 
            I. a mensagem em si; 
            II. o delimitador de paraemtro (para separar no recebimento de mensagem, qual é cada parametro);
            III. o nome do cliente.'''
        mensagem = f"{self.message_input.get()} {format(math.pi, '.10f')} {self.name}"
        if mensagem:
            cifra = rsa.cifrar(mensagem,28837,40301)
            self.socket.send(cifra.encode())
            self.message_input.delete(0, tk.END)
            

    def receber_mensagens(self):
        while True:
            try:
                mensagem = self.socket.recv(1024).decode()
                msg_decifrada = rsa.decifrar(mensagem,40301,12973)
                msg_decifrada = msg_decifrada.split(f" {format(math.pi, '.10f')} ")
                if msg_decifrada[0]:
                    nome = msg_decifrada[1]
                    self.chat_display.configure(state='normal')

                    if nome == self.name:
                        self.chat_display.insert(tk.END, f'{msg_decifrada[0]}\n', 'right')
                    else:
                        self.chat_display.insert(tk.END, f'{nome}: {msg_decifrada[0]}\n', 'left')
                    self.scroll_to_bottom()
                    self.chat_display.configure(state='disabled')
            except ConnectionError:
                break

    def limpar_chat(self):
        self.chat_display.configure(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state='disabled')
        
    def scroll_to_bottom(self):
        """Rola o chat para baixo."""
        self.chat_display.yview_moveto(1.0)


if __name__ == '__main__':
    Start_window = ttk.Window()

    # Calculando a posição central da tela
    screen_width = Start_window.winfo_screenwidth()
    screen_height = Start_window.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 200) // 2
    Start_window.geometry(f'300x127+{x}+{y}')

    entry_app = NameEntryApp(Start_window)
    Start_window.mainloop()
