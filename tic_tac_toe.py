class Board:
    squares = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def printBoard(self):
        #print("\033[2J\033[H")
        print("-------------")
        for i in range(3):
            print(f"| {self.squares[i][0]} | {self.squares[i][1]} | {self.squares[i][2]} |")
            print("-------------")

    def move(self):
        global gameState
        self.printBoard()
        if self.playerMove(self.player1):
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
            self.player2.calculateMove()

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
    
    def evaluatePosition(self, board):
        for i in range(3):
            if board.checkRow(i, "X"):
                return -10
            if board.checkRow(i, "O"):
                return 10

            if board.checkColumn(i, "X"):
                return -10
            if board.checkColumn(i, "O"):
                return 10
        
        if board.checkDiagonals("X"):
            return -10
        if board.checkDiagonals("O"):
            return 10
        
        return 0

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
        board.squares[bestRow][bestCol] = "O"

gameState = 0
print("Welcome to Tic-Tac-Toe! To make a move, type the x-coordinate and the y-coordinate separated by a space.")
secondPlayer = input("Play vs Player or Computer? (p for player, c for computer): ")
if secondPlayer == "p":
    board = Board(Player("X"), Player("O"))
else:
    board = Board(Player("X"), Computer("O"))

while True:
    board.move()
    if gameState == 1:
        print("X wins!")
        break
    if gameState == 2:
        print("O wins!")
        break