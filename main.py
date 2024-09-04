import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Configurações do cliente
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 5000         # Porta do servidor

# Função para receber mensagens do servidor
def receive_messages():
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, msg + '\n')
            chat_box.config(state=tk.DISABLED)
        except:
            print("Erro ao receber mensagem")
            break

# Função para enviar a mensagem
def send_message():
    msg = message_entry.get()
    # Exibe a mensagem enviada no chat localmente
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, "Você: " + msg + '\n')
    chat_box.config(state=tk.DISABLED)
    
    # Envia a mensagem para o servidor
    client_socket.send(msg.encode('utf-8'))
    message_entry.delete(0, tk.END)

# Configurações da interface Tkinter
root = tk.Tk()
root.title("Chat Cliente")

# Caixa de texto para exibir as mensagens
chat_box = scrolledtext.ScrolledText(root, state=tk.DISABLED)
chat_box.pack(padx=20, pady=5)

# Campo de entrada de texto
message_entry = tk.Entry(root, width=50)
message_entry.pack(padx=20, pady=5)

# Botão para enviar mensagem
send_button = tk.Button(root, text="Enviar", command=send_message)
send_button.pack(pady=5)

# Conectando ao servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Iniciando a thread para receber mensagens
thread = threading.Thread(target=receive_messages)
thread.start()

# Iniciando a interface Tkinter
root.mainloop()
