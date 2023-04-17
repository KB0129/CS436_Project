import threading
import socket
from datetime import datetime


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

# show the message to the all clients
def handle(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'q':
                clients.remove(client)
                break
            else: 
                broadcast(message.encode())

        except: # error while broadcasting or receiving message , remove client and its name   
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'Server: {nickname} left the chatroom.'.encode('ascii'))
            nicknames.remove(nickname)
            break

# receive client from client.py 
def receive():
    counter = 0
    while True:
        client, address = server.accept()
        nickname = client.recv(1024).decode('ascii') 
        # server always accept client
        if counter >= 3: 
            print("testing if this works")
            client.send('reject'.encode('ascii'))
            client.close()
        elif nickname in nicknames:
            print("testing if this works2")
            client.send('nicknameError'.encode('ascii'))
            client.close()
        else:
            print(f"Connection with {str(address)}")
            counter+=1
        # recieve nickname and client from client.py python3 client.py
            client.send('CONNECTED'.encode('ascii'))
            #nickname = client.recv(1024).decode('ascii') 
            nicknames.append(nickname)
            clients.append(client) 

            print(f'Server:{nickname} joined the chatroom.')
            broadcast(f'Server: {nickname} joined the chatroom.'.encode('ascii')) # show who join the chatroom

            thread = threading.Thread(target=handle, args=(client, ))
            thread.start()


#enter -> 소켓연결 -> 서버단에서 인원이 꽉차면은 -> 리젝트를 보내고 -> CLOSE() -> 클라에서는 리젝을 받지 -> 
                 #   -> 인원이 남는가 -> CONNECTED를 CLIENT로 보낸다 -> "NICK"을 클라에게 보내서 닉네임이 뭔지 물어본다.
# start server program
print("Sever is now on. Listening...")
receive()
