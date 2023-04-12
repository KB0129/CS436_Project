# import socket
# import sys
# import time

# if __name__ == '__main__':
#     socket_server = socket.socket()
#     server_host = socket.gethostname()
#     ip = socket.gethostbyname(server_host)
#     sport = 18000

#     print('This is your IP address: ', ip)
#     server_host = input('Enter friend\'s IP address:')
#     name = input('Enter Friend\'s name: ')

#     socket_server.connect((server_host, sport))

#     socket_server.send(name.encode())
#     server_name = socket_server.recv(1024)
#     server_name = server_name.decode()

#     print(server_name, ' has joined...')
#     while True:
#         message = (socket_server.recv(1024)).decode()
#         print(server_name, ":", message)
#         message = input("Me : ")
#         socket_server.send(message.encode())

import socket
import threading

nickname = input("Choose your nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connet(('127.0.0.1', 18000))

# get message from server
def recieve():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                pass
            else:
                print(message)

        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


    
