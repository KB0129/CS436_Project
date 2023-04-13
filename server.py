import threading
import socket

host = '127.0.0.1' # local host, run the server on my computer
port = 18000

# start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server bind to loacl hose, port = 18000
# server should be 'listening mode" to connection
# listeners for 3 active connections. 
server.bind((host, port))
server.listen(3)

# put the clients, nicknames on list
clients = []
nicknames = []

# send message to all clients on the server
def broadcast(message):
    for client in clients:
        client.send(message)

#  try to show the message to the all clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except: # error while broadcasting or receiving message , remove client and its name   
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

# receive information from client.py
def receive():
    while True:
        # server always accept client
        client, address = server.accept()
        print(f"Connection with {str(address)}")

        # recieve nickname and client from client.py
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii') 
        nicknames.append(nickname)
        clients.append(client) 

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii')) # show who join the chatroom
        client.send('Connected to the server!'.encode('ascii')) # client know he/she is on the server

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

# main
print("Sever is now on. Listening...")
receive()