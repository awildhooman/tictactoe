class Board:
    squares = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def printBoard(self):
        print("\033[2J\033[H")
        print("-------------")
        for i in range(3):
            print(f"| {self.squares[i][0]} | {self.squares[i][1]} | {self.squares[i][2]} |")
            print("-------------")

    def gameLoop(self):
        global gameState
        self.printBoard()

        #checks if player1/player2 is a player or computer object, then does the action accordingly
        if isinstance(self.player1, Player):
            if self.playerMove(self.player1):
                self.printBoard()
                gameState = 1
                return 0
        else:
            if self.player1.calculateMove():
                self.printBoard()
                gameState = 1
                return 0

        self.printBoard()

        if isinstance(self.player2, Player):
            if self.playerMove(self.player2):
                self.printBoard()
                gameState = 2
                return 0
        else:
            if self.player2.calculateMove():
                self.printBoard()
                gameState = 2
                return 0
        #tie
        if not self.movesLeft():
            gameState = 3

    def playerMove(self, player):
        playerCoordinates = player.playerMove()
        #-1 to make it not 0-indexed for player
        col = int(playerCoordinates[0]) - 1
        row = int(playerCoordinates[1]) - 1
        if self.squares[row][col] == " ":
            self.squares[row][col] = player.symbol
        #check if win
        if self.checkRow(row, player.symbol) or self.checkColumn(col, player.symbol) or self.checkDiagonals(player.symbol):
            return True
        

    #when a player makes a move, check the column/row/diagonal associated with that square
    def checkRow(self, row, symbol):
        if symbol == self.squares[row][0] == self.squares[row][1] == self.squares[row][2]:
            return True
        return False

    def checkColumn(self, col, symbol):
        if symbol == self.squares[0][col] == self.squares[1][col] == self.squares[2][col]:
            return True
        return False

    def checkDiagonals(self, symbol):
        if symbol == self.squares[1][1] and ((self.squares[0][0] == self.squares[1][1] == self.squares[2][2]) or (self.squares[0][2] == self.squares[1][1] == self.squares[2][0])):
            return True
        return False

    def movesLeft(self):
        for row in self.squares:
            for square in row:
                if square == " ":
                    return True
        return False


class Player:
    
    def __init__(self, symbol):
        self.symbol = symbol

    def playerMove(self):
        coordinates = input().split(" ")
        return coordinates

class Computer:
    
    opponent = None

    def __init__(self, symbol):
        self.symbol = symbol
        if symbol == "X":
            self.opponent = "O"
        else:
            self.opponent = "X"
    
    #evaluates the position, with +10 = computer win, 0 = tie, -10 = computer loss
    def evaluatePosition(self, board): 
        for i in range(3):
            if board.checkRow(i, "X"):
                return 10 * computerFirst
            if board.checkRow(i, "O"):
                return -10 * computerFirst

            if board.checkColumn(i, "X"):
                return 10 * computerFirst
            if board.checkColumn(i, "O"):
                return -10 * computerFirst
        
        if board.checkDiagonals("X"):
            return 10 * computerFirst
        if board.checkDiagonals("O"):
            return -10 * computerFirst
        
        return 0

    #this function assigns each possible move a value
    def minimax(self, board, depth, isMaximizing):
        score = self.evaluatePosition(board)
        if score == 10:
            return 10

        if score == -10:
            return -10

        if not board.movesLeft():
            return 0

        if isMaximizing:
            best = -20
            for i in range(3):
                for j in range(3):
                    if board.squares[i][j] == " ":
                        board.squares[i][j] = self.symbol
                        best = max(best, self.minimax(board, depth+1, not isMaximizing))
                        board.squares[i][j] = " "
            return best
        else:
            best = 20
            for i in range(3):
                for j in range(3):
                    if board.squares[i][j] == " ":
                        board.squares[i][j] = self.opponent
                        best = min(best, self.minimax(board, depth+1, not isMaximizing))
                        board.squares[i][j] = " "
            return best
    
    #calls minimax on empty squares, returns square with the best value
    def calculateMove(self):
        global board
        bestRow = -1
        bestCol = -1
        bestValue = -20

        for i in range(3):
            for j in range(3):
                if board.squares[i][j] == " ":
                    board.squares[i][j] = self.symbol
                    moveValue = self.minimax(board, 0, False)
                    board.squares[i][j] = " "
                    if moveValue > bestValue:
                        bestValue = moveValue
                        bestRow = i
                        bestCol = j
        if bestRow != -1:
            board.squares[bestRow][bestCol] = self.symbol

        if board.checkRow(bestRow, self.symbol) or board.checkColumn(bestCol, self.symbol) or board.checkDiagonals(self.symbol):
            return True

gameState = 0
print("\033[2J\033[H")
print("Welcome to Tic-Tac-Toe! To make a move, type the x-coordinate and the y-coordinate separated by a space.")
secondPlayer = input("Play vs Player or Computer? (p for player, c for computer): ")
computerFirst = -1

if secondPlayer == "p":
    board = Board(Player("X"), Player("O"))
else:
    order = input("Computer goes first or second? (type 1 or 2) ")
    if order == "1":
        computerFirst = 1
        board = Board(Computer("X"), Player("O"))
    else:
        board = Board(Player("X"), Computer("O"))

while True:
    board.gameLoop()
    if gameState == 1:
        print("X wins!")
        break
    if gameState == 2:
        print("O wins!")
        break
    if gameState == 3:
        print("Tie!")
        break