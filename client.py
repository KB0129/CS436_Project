import socket
import threading
import time
import pickle 

nickname = input("Choose your nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 18000))

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

# write function to send message to chatroom
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

# give options to user
def giveOption(option):
    try:
        # if message is not empty, send it to server
        if not option.isspace():
            client.send(option.encode())
        
        # Option 1: get the list of clients in the server
        if option == "1":
            print("Here is the list: ")
            time.sleep(0.8)
            serverSend = client.recv(1024)
            serverList = pickle.loads(serverSend)
        
        # Option 2: join the chatroom
        elif option == "2":
            recieve_thread = threading.Thread(target=recieve)
            recieve_thread.start()
            write_thread = threading.Thread(target=write)
            write_thread.start()

        # Option 3: quit the chatroom
        elif option =="3":
            print("Leave the chatroom")
            client.shutdown(socket.SHUT_RDWR)
            client.close()
    except:
        print("Type, error!")
        client.shutdown(socket.SHUT_RDWR)
        client.close()        

print("\nChoose Option:\n1.Get a report of the chatroom from the server.\n2.Request to join the chatroom.\n3.Quit the program\n")
user_Option = input("What is your option?: ")
giveOption(user_Option)
print("\n")


# recieve_thread = threading.Thread(target=recieve)
# recieve_thread.start()
# write_thread = threading.Thread(target=write)
# write_thread.start()

    
