# Alex Brady
# Principles of Networking Project
# Connect Four Game Logic

import ast

class Player:
  YELLOW_PLAYER, RED_PLAYER, NO_PLAYER = range(3)
  
class Point:
  def __init__ (self, x, y):
    self.row = x
    self.column = y
    
  
class GameBoard:
  def __init__ (self):
    self.board = [[Player.NO_PLAYER for x in range(7)] for x in range(6)] 
    self.currentPlayer = Player.YELLOW_PLAYER
    self.hadTurn = False
  
  def verticalCheck (self, lastMove):
    row = lastMove.column
    column = lastMove.row
    if row < 3:
      return False
    
    currentPlayer = self.currentPlayer
    for i in range(row - 3, row):
      if self.board[i][column] != currentPlayer:
        return False
    
    return True
  
  def horizontalCheck (self, lastMove):
    column = lastMove.column - 1
    row = lastMove.row
    counter = 1
    currentPlayer = self.currentPlayer
    
    while column >= 0:
      if self.board[row][column] != currentPlayer:
        break
      column = column - 1
      counter = counter + 1
    
    if counter >= 4:
      return True
    
    counter = 1
    column = lastMove.column + 1
    while column <= 6:
      if self.board[row][column] != currentPlayer:
        break
      column = column + 1
      counter = counter + 1      
    
    if counter >= 4:
      return True
    
    return False
  
  def leftUpDiagonalCheck(self, lastMove):
    column = lastMove.column - 1
    row = lastMove.row - 1
    counter = 1
    currentPlayer = self.currentPlayer
    
    while column >= 0 and row >= 0:
      if self.board[row][column] != currentPlayer:
        break
      column = column - 1
      row = row - 1
      counter = counter + 1
    
    if counter >= 4:
      return True
    
    counter = 1
    column = lastMove.column + 1
    row = lastMove.row + 1
    while column <= 6 and row <= 5:
      if self.board[row][column] != currentPlayer:
        break
      column = column + 1
      row = row + 1
      counter = counter + 1      
    
    if counter >= 4:
      return True
    
    return False
  
  def rightUpDiagonalCheck(self, lastMove):
    column = lastMove.column - 1
    row = lastMove.row + 1
    counter = 1
    currentPlayer = self.currentPlayer
    
    while row <= 5 and column >= 0:
      if self.board[row][column] != currentPlayer:
        break
      column = column - 1
      row = row + 1
      counter = counter + 1
    
    if counter >= 4:
      return True
    
    counter = 1
    column = lastMove.column + 1
    row = lastMove.row - 1
    while column <= 6 and row >= 0:
      if self.board[row][column] != currentPlayer:
        break
      column = column + 1
      row = row - 1
      counter = counter + 1      
    
    if counter >= 4:
      return True
    
    return False  
    
    
  def checkStatus (self, lastMove):
    '''Check status to see if the either player has won.
    Current method only checks for wins straight
    accross or straight up and down (no diagonals).'''

    if self.verticalCheck(lastMove):
      return (True, 'vertical')
    if self.horizontalCheck(lastMove):
      return (True, 'horizontal')
    if self.leftUpDiagonalCheck(lastMove):
      return (True, 'leftUpDiagonal')
    if self.rightUpDiagonalCheck(lastMove):
      return (True, 'rightUpDiagonal')    
    
    return (False, '')

  
  def togglePlayer (self):
    '''Changes the current player to the opposing player'''
    if self.currentPlayer == Player.RED_PLAYER:
      self.currentPlayer = Player.YELLOW_PLAYER
    else:
      self.currentPlayer = Player.RED_PLAYER
  
  def placeChip (self, location):
    '''Attempts to place the current player's color chip at the location.
    This function does nothing if the location is already occupied'''
    if self.hadTurn == True:
      return False
    row = location[0]
    col = location[1]
    if row == 0:
      if self.board[row][col] != Player.NO_PLAYER:
        return False 
      else:
        self.board[row][col] = self.currentPlayer
        return True        
    else:
      if self.board[row][col] != Player.NO_PLAYER:
        return False       
      elif self.board[row - 1][col] == Player.NO_PLAYER:
        return False
      else:
        self.board[row][col] = self.currentPlayer
        return True        
    
    
def executeCommand (command, args, board):
  if command == 'placeChip':
    locationList = ast.literal_eval(args)
    location = [locationList[0], locationList[1]]
    board.placeChip(location)