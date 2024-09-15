import tkinter as tk
from chat import iniciar_chat

def abrir_tela_chat(nome):
    root.destroy()  # Fecha a tela de entrada
    iniciar_chat(nome)  # Chama a função que inicia o chat

# Função para capturar o nome e passar para a tela de chat
def entrar_no_chat():
    nome = nome_entry.get()
    if nome:
        abrir_tela_chat(nome)

# Configurações da interface Tkinter para a tela de entrada
root = tk.Tk()
root.title("Tela de Entrada")

# Label para instrução
instrucoes_label = tk.Label(root, text="Digite seu nome para entrar no chat:")
instrucoes_label.pack(padx=20, pady=10)

# Campo de entrada para o nome
nome_entry = tk.Entry(root, width=40)
nome_entry.pack(padx=20, pady=10)

# Botão para avançar para o chat
entrar_button = tk.Button(root, text="Entrar", command=entrar_no_chat)
entrar_button.pack(pady=20)

# Iniciando a interface Tkinter
root.mainloop()
