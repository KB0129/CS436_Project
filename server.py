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
user_data=[]

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
            elif message == 'a':
                client.send('file'.encode())
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
            client.send('reject'.encode('ascii'))
            client.close()
        elif nickname in nicknames:
            client.send('nicknameError'.encode('ascii'))
            client.close()
        else:
            if nickname == 'LIST':
                user_info = str(counter)+'. '+ str(nickname) +' is using address: '+ str(address[1]) + ' with port:'+str(port)
                client.send(user_info.encode('ascii'))
                client.close()
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


#enter -> Connect Socket ->  If user is full -> Send Reject -> Server: close() -> Client: get reject -
#      ->                -> If user is not full -> Send Connect -> Server: thread() -> Client: input nickname
# start server program
print("Sever is now on. Listening...")
receive()
