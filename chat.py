import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

# Configurações do cliente
HOST = '127.0.0.1'
PORT = 5000

# Função para receber mensagens do servidor
def receive_messages(chat_box):
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
def send_message(message_entry, chat_box, nome, event=None):
    msg = message_entry.get()
    time_sent = datetime.now().strftime('%H:%M')

    # Exibe a mensagem enviada no chat localmente
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"Você: {msg} | {time_sent}\n", 'user_message')
    chat_box.config(state=tk.DISABLED)

    # Envia a mensagem para o servidor
    client_socket.send(f"{msg}".encode('utf-8'))
    message_entry.delete(0, tk.END)

# Função para fechar a conexão e encerrar o programa
def close_connection(chat_box, root):
    # Enviar uma mensagem avisando que a conexão foi encerrada
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, "Conexão encerrada.\n", 'system_message')
    chat_box.config(state=tk.DISABLED)

    # Avisar ao servidor que a conexão foi encerrada
    try:
        client_socket.send("Conexão encerrada pelo cliente.".encode('utf-8'))
        client_socket.close()  # Fechar a conexão com o servidor
    except:
        pass

    root.quit()  # Fecha a janela do Tkinter
    root.destroy()  # Destroi a janela para encerrar o programa

# Função para iniciar o chat com o nome do usuário
def iniciar_chat(nome):
    # Conectando ao servidor
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    # Enviando o nome do usuário para o servidor
    client_socket.send(nome.encode('utf-8'))

    # Configurações da interface Tkinter para o chat
    root = tk.Tk()
    root.title("Chat Cliente")

    # Tema escuro
    root.configure(bg='#2c2f33')
    
    # Caixa de texto para exibir as mensagens
    chat_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD, bg='#23272a', fg='#ffffff', font=('Arial', 12), insertbackground='white')
    chat_box.pack(padx=20, pady=5)
    
    # Definir cor especial para as mensagens do usuário
    chat_box.tag_config('user_message', foreground='#7289da')
    chat_box.tag_config('system_message', foreground='#ff5555')  # Cor especial para mensagens do sistema
    
    # Campo de entrada de texto
    message_entry = tk.Entry(root, width=50, bg='#2c2f33', fg='#ffffff', insertbackground='white')
    message_entry.pack(padx=20, pady=5)

    # Bind para a tecla Enter chamar a função send_message
    message_entry.bind('<Return>', lambda event: send_message(message_entry, chat_box, nome, event))
    
    # Botão para enviar mensagem
    send_button = tk.Button(root, text="Enviar", command=lambda: send_message(message_entry, chat_box, nome), bg='#7289da', fg='#ffffff', activebackground='#5865f2')
    send_button.pack(pady=5)

    # Botão para encerrar a conexão
    exit_button = tk.Button(root, text="Sair", command=lambda: close_connection(chat_box, root), bg='#ff5555', fg='#ffffff', activebackground='#ff4444')
    exit_button.pack(pady   =5)
    
    # Iniciando a thread para receber mensagens
    thread = threading.Thread(target=receive_messages, args=(chat_box,))
    thread.start()

    # Iniciando a interface Tkinter
    root.mainloop()
