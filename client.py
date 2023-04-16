import socket
import threading
import time
import pickle
from datetime import datetime

def enter():
    global nickname 
    nickname = input("Please enter a username: ")
    global client 
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
        # message = f'{nickname}: {input("")}'
        message = input()
        if message.lower() == 'q':
            client.send(message.encode())
            #write 쓰레드가 종료되어야함 + recieve 쓰레드도 종료해야함
        else:
            new_message = f'{nickname}: {message}'
            date_now = datetime.now().strftime("[%H:%M] ")
            new_message = date_now + new_message
            client.send(new_message.encode('ascii'))

# give options to user
def giveOption():    
    while True:
        print("Please select one of the following options:\n    1.Get a report of the chatroom from the server.\n    2.Request to join the chatroom.\n    3.Quit the program")
        user_Option = input("Your choice: ")
        try:
            # if message is not empty, send it to server
            if not user_Option.isspace():
            # Option 1: get the list of clients in the server
                if user_Option == "1":
                    print("Here is the list: ")
                    time.sleep(0.8)
                    serverSend = client.recv(1024)
                    serverList = pickle.loads(serverSend)
            
                # Option 2: join the chatroom
                elif user_Option == "2":
                    enter()
                    recieve_thread = threading.Thread(target=recieve)
                    recieve_thread.start()
                    while True:
                        
                        # message = f'{nickname}: {input("")}'
                        message = input()
                        if message.lower() == 'q':
                            client.send(message.encode())
                            recieve_thread.join()
                            return 
                        else:
                            new_message = f'{nickname}: {message}'
                            date_now = datetime.now().strftime("[%H:%M] ")
                            new_message = date_now + new_message
                            client.send(new_message.encode('ascii'))

                # Option 3: quit the chatroom 
                elif user_Option == "3":
                    print("Program finish, Bye")
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                    return
                # wrong option case
                else:
                    print("Wrong option, choose again.")
                    #client_menu()
        except:
            print("System Error.")
            client.shutdown(socket.SHUT_RDWR)
            client.close()      
            return

    
def chatting():
    client_Thread()
    



"""
def client_Thread():
    recieve_thread = threading.Thread(target=recieve)
    recieve_thread.start()
    write_thread = threading.Thread(target=write)
    write_thread.start()
"""
def main_function():
    giveOption()
    

        
     
# start client program
main_function()


# recieve_thread = threading.Thread(target=recieve)
# recieve_thread.start()
# write_thread = threading.Thread(target=write)
# write_thread.start()

    
