#!/usr/bin/env python3
import threading
import socket

host = '127.0.0.1'
port = 8001
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(port)

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handleClient(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(nickname + 'has left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break


def recieve():
    while True:
        client, address = server.accept()
        print('Connection established with' + str(address))
        nickname = client.recv(1024).decode('ascii')

        client.send('NICK'.encode('ascii'))
        nicknames.append(nickname)
        clients.append(client)

        print('Nickname of the client us' + nickname)
        broadcast(nickname + 'has joined the chat!'.encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()


print('Server is running')
recieve()
