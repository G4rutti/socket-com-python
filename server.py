import socket
import threading
from datetime import datetime

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP local
PORT = 5000         # Porta para escutar

# Lista de clientes conectados
clients = []
client_names = {}

# Função para lidar com as mensagens recebidas de cada cliente
def handle_client(client_socket):
    try:
        # Recebe o nome do cliente quando ele se conecta
        name = client_socket.recv(1024).decode('utf-8')
        client_names[client_socket] = name
        broadcast(f"{name} entrou na conversa", client_socket)

        while True:
            # Recebe a mensagem do cliente
            msg = client_socket.recv(1024).decode('utf-8')
            time_sent = datetime.now().strftime('%H:%M')
            broadcast(f"{name}: {msg} | {time_sent}", client_socket)
    except:
        # Remove o cliente da lista se ele se desconectar
        clients.remove(client_socket)
        broadcast(f"{client_names[client_socket]} saiu da conversa", client_socket)
        del client_names[client_socket]

# Função para enviar a mensagem a todos os clientes conectados
def broadcast(msg, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(msg.encode('utf-8'))
            except:
                clients.remove(client)

# Função para iniciar o servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f'Servidor iniciado em {HOST}:{PORT}')
    while True:
        client_socket, addr = server.accept()
        print(f'Conexão de {addr}')
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

# Inicia o servidor
start_server()
