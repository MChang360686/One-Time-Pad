#!/usr/bin/env python3

import socket
import threading
import select
import sys

HOST = input("Please enter host address")
if(HOST == ''):
  HOST = '127.0.0.1'
  print("Host is localhost")

Socket = input("Please enter port number")
if(Socket == ''):
  Socket = int('12345')
  print("Port Number is 12345")
else:
    Socket = int(Socket)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, Socket))
server.listen()
print("Server Initialized")

clients = []
aliases = []
FORMAT = "utf-8"

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{aliases[clients.index(client)]}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close
            name = aliases[index]
            aliases.remove(name)
            break



def receive():
    while True:
        client, address = server.accept()
        print(f"Connection from {str(address)}")
        client.send("ALIAS".encode('utf-8'))
        client.send(bytes("Server is ready to receive", FORMAT))
        name = client.recv(1024)
        aliases.append(name)
        clients.append(client)
        print(f"alias {name} connects from {address}")
        broadcast((f"New connection {name}\n").encode(FORMAT))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is running")
receive()