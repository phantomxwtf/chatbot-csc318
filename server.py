import threading
import socket
import tkinter as tk

host = '127.0.0.1'
port = 59000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []

def broadcast(message, sender_alias=None):
    for client in clients:
        if sender_alias:
            client.send(f'{sender_alias}: {message}'.encode('utf-8'))
        else:
            client.send(message.encode('utf-8'))

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('utf-8').startswith('@'):  # Check if it's a private message
                recipient_alias, message_body = message.decode('utf-8').split(" ", 1)
                recipient_index = aliases.index(recipient_alias[1:])
                recipient_client = clients[recipient_index]
                recipient_client.send(f'(Private) {aliases[clients.index(client)]}: {message_body}'.encode('utf-8'))
            else:
                broadcast(message.decode('utf-8'), aliases[clients.index(client)])
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!', 'Server')
            aliases.remove(alias)
            update_client_list()  # Update client list when someone leaves
            break

def update_client_list():
    client_list = ", ".join(aliases)
    connected_clients_listbox.delete(0, tk.END)  # Clear existing entries
    for alias in aliases:
        connected_clients_listbox.insert(tk.END, alias)

def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}')
        broadcast(f'{alias} has connected to the chat room!', 'Server')
        update_client_list()  # Update client list when someone joins
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Tkinter GUI setup
root = tk.Tk()
root.title("Server")

connected_clients_label = tk.Label(root, text="Connected Clients:")
connected_clients_label.pack()

connected_clients_listbox = tk.Listbox(root, width=50, height=20)
connected_clients_listbox.pack()

server_thread = threading.Thread(target=receive)
server_thread.start()

root.mainloop()
