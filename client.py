# Alex Brady
# Principles of Networking Project
# Connect Four Client

from Tkinter import *
from socket import *
from gameLogic import *
from threading import Thread

class Manager:
   def waitForResponse(self):
      WaitThread(self.on_thread_finished).start()
   
   def on_thread_finished(self):
      
      response = clientSocket.recv(1024)
      splitLines = response.splitlines()
      protocol = splitLines[0].rstrip('\r\n')
      command = splitLines[1].rstrip('\r\n')
      args = splitLines[2].rstrip('\r\n')
      gameBoard.hadTurn = False
      if command == 'startGame':
         statusLabel.configure(text='Another player has joined. It\'s your turn')
      else:
         executeCommand(command, args, gameBoard)
         locationList = ast.literal_eval(args)
         location = [locationList[0], locationList[1]]      
         if gameBoard.currentPlayer == Player.RED_PLAYER:
            window.itemconfig(boardLocations[location[0]][location[1]], fill="red")
         else:
            window.itemconfig(boardLocations[location[0]][location[1]], fill="yellow")
         
         currentMove = Point(locationList[0], locationList[1])  
         gameWon, method = gameBoard.checkStatus(currentMove)
         if gameWon:
            gameBoard.hadTurn = True
            statusLabel.configure(text='You Lost!')
         else:
            gameBoard.togglePlayer()
            statusLabel.configure(text='It\'s your turn')
      
class WaitThread(Thread):
   def __init__(self, callback):
      Thread.__init__(self)
      self.callback = callback
   
   def run(self):
      self.callback()
      
clientSocket = socket(AF_INET, SOCK_STREAM)
host = 'localhost'
port = 31415
clientSocket.connect((host, port))

gameBoard = GameBoard()
thread = Manager()

def clickLocationCallback(event, arg):
   if gameBoard.placeChip(arg):
      if gameBoard.currentPlayer == Player.RED_PLAYER:
         window.itemconfig(boardLocations[arg[0]][arg[1]], fill="red")
      else:
         window.itemconfig(boardLocations[arg[0]][arg[1]], fill="yellow")
      currentMove = Point(arg[0], arg[1])
      gameWon, method = gameBoard.checkStatus(currentMove)
      if gameWon:
         window.update()
         gameBoard.hadTurn = True
         response = 'C4\r\nplaceChip\r\n{location}'.format(location=arg) 
         clientSocket.send(response)
         statusLabel.configure(text='You Won!')
      else:         
         window.update()
         gameBoard.togglePlayer()
         gameBoard.hadTurn = True
         response = 'C4\r\nplaceChip\r\n{location}'.format(location=arg) 
         clientSocket.send(response)
         statusLabel.configure(text='Waiting on other player')
         thread.waitForResponse()   


        
master = Tk()

window = Canvas(master, width=700, height=600)
window.configure(background='Blue')
window.pack()

statusLabel = Label(master)
statusLabel.pack()

startX = 10
startY = 510
boardLocations = []
for row in range(0,6):
   boardLocations.append([])
   for col in range(0,7):
      boardLocations[row].append(window.create_oval(startX, startY, startX + 90, startY + 90, fill='White'))
      data = [row, col]
      window.tag_bind(boardLocations[row][col], "<Button-1>", lambda event, arg=data: clickLocationCallback(event, arg))
      startX = startX + 100
   startX = 10
   startY = startY - 100

clientSocket.send('C4\r\nnewGame\r\n ')
response = clientSocket.recv(1024)
splitLines = response.splitlines()
protocol = splitLines[0].rstrip('\r\n')
command = splitLines[1].rstrip('\r\n')
args = splitLines[2].rstrip('\r\n')
if args == 'False':
   statusLabel.configure(text="Waiting on other player")
   thread.waitForResponse()

else:
   statusLabel.configure(text="Waiting on another player to join")
   gameBoard.hadTurn = True
   thread.waitForResponse()
   
mainloop()
clientSocket.close()