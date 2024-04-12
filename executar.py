#   PROVAVELMENTE ESSE C´DIGO NÃO VAI PARA A APS
#   É APENAS PARA RODAR UMA VEZ O SERVER.PY E DUAS VEZES O CLIENT.PY E AUTOMATICAMENTE!!!
#   Para não precisar ficar abrindo terminal toda hora


import threading
import concurrent.futures

def execute_script(script):
    import os
    print(f"Executando {script}")
    os.system(f"python {script}")

def run_server():
    print("Executando server.py em uma thread separada...")
    execute_script("server.py")

# Inicia o servidor em uma thread separada
server_thread = threading.Thread(target=run_server)
server_thread.start()

# Executa os dois client.py simultaneamente
print("Executando os clientes...")
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(execute_script, ["client.py", "client.py"])
