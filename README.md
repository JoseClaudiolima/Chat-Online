# Chat Online com Sockets e GUI Ttkbootstrap
Este é um projeto de chat online desenvolvido em Python, utilizando sockets para comunicação entre o servidor e os clientes. A interface gráfica é construída com ttkbootstrap.

### O projeto consiste em dois principais scripts:
1. **server.py**: Este script implementa o servidor do chat. Ele gerencia a comunicação entre os diferentes clientes e distribui as mensagens recebidas para todos os participantes ativos do chat.
2. **client.py**: Este script é executado pelos usuários que desejam participar do chat. Ele se conecta ao servidor e fornece uma interface gráfica para enviar e receber mensagens.

### Pré-requisitos
1. Certifique-se de ter Python instalado no seu sistema.
2. Biblioteca externa do python, **ttkbootstrap**: Instale usando o comando pip install ttkbootstrap.
3. Biblioteca externa do python, **pyperclip**: Instale usando o comando pip install pyperclip.
4. Biblioteca externa do python, **emoji**: Instale usando o comando pip install emoji.

### Como usar
Inicie o servidor executando python server.py.
Os clientes podem se conectar ao servidor executando python client.py.
Os clientes serão solicitados a inserir o endereço IP do servidor e a porta.
Uma vez conectados, os clientes podem começar a enviar e receber mensagens através da interface gráfica.

Licença
Este projeto é licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.
