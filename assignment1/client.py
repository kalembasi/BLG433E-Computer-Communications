# Omer Malik Kalembasi
# 150180112

import struct
import threading
import socket
import hashlib

def client_side(client_socket): 
    
    while (True):
        
        message_type = input()
        
        if message_type == "01":
            sender = struct.pack('b', 1) 
            client_socket.sendall(sender)
            
        if message_type == "02":
            sender = struct.pack('b', 2)
            client_socket.sendall(sender)
            
        if message_type == "03":
            sender = struct.pack('b', 3)
            client_socket.sendall(sender)
            
        if message_type == "04":
            guess = input('Guess: \n').encode()
            instruction_type = struct.pack('b', 4)
            sender = instruction_type + guess
            client_socket.sendall(sender)
            
        if message_type == "05":
            sender = struct.pack('b', 5)
            client_socket.sendall(sender)

def server_side(client_socket):
    
    while(True):
        
        response = client_socket.recv(1024)
        packet_type = struct.unpack('b',response[0:1])[0]
        
        if packet_type == "0":
            encoding_type = struct.unpack('b',response[1:2])[0]
            size = struct.unpack('<h',response[2:4])[0]
            if encoding_type == "0":
                information = response[4:4+size].decode('utf-8')
            if encoding_type == "1":
                information = response[4:4+(size*2)].decode('utf-16')
            print(information)
            
        if packet_type == "1":
            encoding_type = struct.unpack('b',response[1:2])[0]
            size = struct.unpack('<h',response[2:4])[0]
            lenght = struct.unpack('<h',response[4:6])[0]
            
            if encoding_type == 0:
                question = response[6:6+size].decode('utf-8')
                
            if encoding_type == 1:
                question = response[6:6+(size*2)].decode('utf-16')
                
            print("Word lenght: ", lenght)
            print("Question: ",question)
            
        if packet_type == "2":
            position = struct.unpack('b', response[2:3])[0]
            letter = response[3:4].decode('utf-8')
            print("Position: ", position)
            print("Letter: ", letter)
            
        if packet_type == "3":
            rem_time = struct.unpack('<h', response[4:6])[0]
            print("Remaining Time: ", rem_time)
            
        if packet_type == "4":
            overall_score = struct.unpack('<h', response[2:4])[0]
            rem_time = struct.unpack('<h', response[4:6])[0]
            print("Remaining time: ", rem_time)
            print("Overall Score: ", overall_score)
        
        
rem_time = 300 # remaining time

#print (hashlib.algorithms_guaranteed)

hex = "F8EDEB992DB9D25AD8683710DD1BCCDB" # hex got from mail
#hexEncrypted = hashlib.sha1(hex.encode("utf-8"))
#print(hexEncrypted.hexdigest())


host = "160.75.154.126" 
port = 2022  

client_socket = socket.socket()  
client_socket.connect((host, port))  # connect to the server

message = "Start_Connection" 
print("Client:", message) # display on terminal

client_socket.send(message.encode())  # send message
randomHex = client_socket.recv(1024).decode("utf-8")  # receive message

print("Server: " + randomHex)  # display on terminal

concatenatedHex = randomHex + hex
hexEncrypted = hashlib.sha1(concatenatedHex.encode()) # encrypt with using SHA1

message = hexEncrypted.hexdigest() + "#" + "150180112"
print("Client:", message.encode()) # display on terminal

client_socket.send(message.encode())  # send message
responseMessage = client_socket.recv(1024).decode("utf-8")  # receive message
print("Server: " + responseMessage)  # display on terminal


print("Client: 0") # display on terminal
sendMessage = struct.pack('B', 0)
client_socket.sendall(sendMessage) # send message 'Y'

responseMessage = client_socket.recv(1024).decode("utf-8")  # receive message
print("Server: " + responseMessage)  # display on terminal

thread1 = threading.Thread(target=client_side, args=(client_socket,))
thread2 = threading.Thread(target=server_side, args=(client_socket,))
thread1.start()
thread2.start()
thread1.join()
thread2.join()


client_socket.close()  # close the connection