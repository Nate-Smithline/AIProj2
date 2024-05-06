"""
Artificial Intelligence Project 2, Sodoku

Completed by Aayush Draftary and Nathan Smith
"""


class Sodoku:
        """
        INIT FUNCTION

        - will establish the initial variables and run the entire program front-to-back
        """
        def __init__(self, import_file, export_file):
                self.game_board = []

                #initialize the board
                self.board_read_in(import_file)

                self.play_sudoku()

                self.board_read_out(export_file)
        
        """
        BOARD READ IN

        will read the file sent through the program into a gameBoard that will be used to do all the work
        """
        def board_read_in(self, import_file):
                file = open(import_file, 'r')
                lines = file.readlines()
                #go through each line
                for line in lines:
                        board_row = []
                        for num in line.split():
                                #split and add to master gameboard array
                                board_row.append(int(num))
                        self.game_board.append(board_row)
                file.close()

        """
        BOARD READ OUT
        """
        def board_read_out(self, export_file):
                file = open(export_file, 'w')
                #go through each row and write it back in
                for row in self.game_board:
                        file.write(' '.join(map(str,row)) + '\n')
                file.close()



        def play_sudoku(self):
                empty = self.find_empty()
                if not empty:
                        return True
                row, col = empty

                for num in self.order_domain_values():
                        if self.valid_value(row, col, num):
                                self.game_board[row][col] = num
                                if self.play_sudoku():
                                        return True
                                else:
                                        self.game_board[row][col] = 0
                return False


        def order_domain_values(self):
                return range(1, 10)

        """
        FIND EMPTY

        this function is going to look through the board and find an empty square
        """
        def find_empty(self):
                for i, row in enumerate(self.game_board):
                        if 0 in row:
                                return i, row.index(0)
                return False

        def valid_value(self, row, col, num):
                for i in range(9):
                        if (self.game_board[row][i] == num or
                                self.game_board[i][col] == num or
                                self.game_board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num):
                                return False
                return True



sdk = Sodoku('nytimes_input.txt', 'NYtimes_output.txt')
