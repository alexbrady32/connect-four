# Alex Brady
# Principles of Networking Project
# Connect Four Server

#import socket module
from socket import *
from gameLogic import *

gameBoard = GameBoard()

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 31415
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(2)

player1Socket, addr = serverSocket.accept()
player2Socket  = ''

while True:
  request = player1Socket.recv(1024)
  splitLines = request.splitlines()
  protocol = splitLines[0].rstrip('\r\n')
  command = splitLines[1].rstrip('\r\n')
  args = splitLines[2].rstrip('\r\n')
  # Protocol Format: protocol name, command, arguments
  if command == 'newGame':    
    response = 'C4\r\nnewGame\r\nTrue'
    player1Socket.send(response)
    player2Socket, addr = serverSocket.accept()
  else:  
    player2Socket.send(request)
  request = player2Socket.recv(1024)
  splitLines = request.splitlines()
  protocol = splitLines[0].rstrip('\r\n')
  command = splitLines[1].rstrip('\r\n')
  args = splitLines[2].rstrip('\r\n')
  if command == 'newGame':
    response = 'C4\r\nnewGame\r\nFalse'
    player2Socket.send(response)
    response = 'C4\r\nstartGame\r\n '
    player1Socket.send(response)    
  else:
    player1Socket.send(request)
  
serverSocket.close()
    
