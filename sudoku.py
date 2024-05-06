

def board_to_file(board, fileName):
        file = open(fileName, 'w')
        for row in board:
                file.write(' '.join(map(str,row)) + '\n')
        file.close()

def empty_square(board):
        for i in range(len(board)-1):
                for j in range(len(board[0]) ):
                        if board[i][j] == 0:
                                return i, j
        return None

def valid_value(board, row, col, num):
        for i in range(9):
                if board[row][i] == num or board[i][col] == num or board[3*(row//3)+i//3][3 * (col //3) + i % 3] == num:
                        return False
                elif row == col:
                        if board[i][i] == num:
                                return False
                elif row + col == 8:
                        if board[i][8-i] == num:
                                return False
        return True

def play_sudoku(board):
        empty = empty_square(board)
        if empty == None:
                return True
        row, col = empty
        for i in range(1,10):
                if valid_value(board, row, col, i):
                        board[row][col] = i
                        if play_sudoku(board):
                                return True
                        else:
                                board[row][col] = 0
        return False


class Sodoku:
        def __init__(self, fileName):
                self.fileName = fileName
                self.gameBoard = []

                #initialize the board
                self.initialize_board()

                #testing
                self.print_board()
        
        def initialize_board(self):
                file = open(self.fileName, 'r')
                lines = file.readlines()
                for line in lines:
                        board_row = []
                        for num in line.split():
                                board_row.append(int(num))
                        self.gameBoard.append(board_row)
                file.close()

        #temporary function
        def print_board(self):
                for line in self.gameBoard:
                        print(" ".join(map(str, line)))

                



sdk = Sodoku('Sample_Input.txt')
