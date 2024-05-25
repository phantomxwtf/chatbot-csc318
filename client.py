import socket
import threading
import tkinter as tk

host = '127.0.0.1'
port = 59000

alias = None
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith('Connected Clients:'):
                connected_clients_label.config(text=message)
            else:
                message_listbox.insert(tk.END, message)
        except:
            print("An error occurred!")
            client.close()
            break

def send_message(event=None):
    message = message_entry.get()
    if message.startswith('@'):  # Check if it's a private message
        recipient_alias, message_body = message.split(" ", 1)
        client.send(f'{recipient_alias} {message_body}'.encode('utf-8'))
    else:
        client.send(message.encode('utf-8'))
    message_entry.delete(0, tk.END)

def set_alias():
    global alias
    alias = alias_entry.get()
    alias_entry.destroy()  # Destroy the entry widget after getting alias
    alias_button.destroy() # Destroy the alias button after setting alias
    alias_label.config(text=f"Alias: {alias}") # Display alias label
    # Connect to the server and start receiving messages
    client.connect((host, port))
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

root = tk.Tk()
root.title("Chat Application")

alias_entry = tk.Entry(root, width=50)
alias_entry.pack(pady=10)

alias_button = tk.Button(root, text="Set Alias", command=set_alias)
alias_button.pack()

message_frame = tk.Frame(root)
message_frame.pack(pady=10)

scrollbar = tk.Scrollbar(message_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

message_listbox = tk.Listbox(message_frame, width=50, height=20, yscrollcommand=scrollbar.set)
message_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.config(command=message_listbox.yview)

message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=10)
message_entry.bind("<Return>", send_message)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

connected_clients_label = tk.Label(root, text="Connected Clients:")
connected_clients_label.pack()

alias_label = tk.Label(root, text="")
alias_label.pack()

private_chat_info_label = tk.Label(root, text="To send a private message, use '@alias message'")
private_chat_info_label.pack()

root.mainloop()
