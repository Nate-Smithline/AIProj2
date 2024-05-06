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



        """
        PLAY_SODOKU

        This is the master function that runs the backtracking and goes through everything 
        """
        def play_sudoku(self):
                empty = self.find_empty()
                if not empty:
                        return True
                row, col = empty

                for num in range(1,10):
                        if self.valid_value(row, col, num):
                                self.game_board[row][col] = num
                                if self.play_sudoku():
                                        return True
                                else:
                                        self.game_board[row][col] = 0
                return False

        """
        FIND EMPTY

        this function is going to look through the board and find an empty square
        """
        def find_empty(self):
                min_values = float('inf')
                max_constraints = -1
                selected_cell = None
                
                for i, row in enumerate(self.game_board):
                        for j, num in enumerate(row):
                                if num == 0:
                                        num_values = self.mrv(i, j)

                                        constraints = self.dh_calculate(i, j)
                                        
                                        if num_values < min_values or (num_values == min_values and constraints > max_constraints):
                                                min_values = num_values
                                                max_constraints = constraints
                                                selected_cell = (i, j)
                return selected_cell                


        """
        MINIMUM REMAINING VALUES

        This function calculates the number of values remaining in the entire setup
        """
        def mrv(self, row, col):
                # set is more optimized for time complexity
                used_nums = set()
                
                #calculate all related
                for i in range(9):
                        # add everything in the column
                        used_nums.add(self.game_board[row][i])
                        #add everything in the row
                        used_nums.add(self.game_board[i][col])
                        #add diagonals
                        used_nums.add(self.game_board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3])

                        if row == col:
                                used_nums.add(self.game_board[i][i])
                        if row + col == 8:
                                used_nums.add(self.game_board[i][8 - i])

                possible_values = [num for num in range(1, 10) if num not in used_nums]
                return len(possible_values)
        

        """
        DH CALCULATE

        This function is going to calculate the degree heuristic (or number of items that are based on this)
        
        """
        def dh_calculate(self, row, col):
                num_constraints = 0
                for indx in range(9):
                        if self.game_board[row][indx] != 0:
                                num_constraints += 1
                        if self.game_board[indx][col] != 0:
                                num_constraints += 1
                        if self.game_board[3 * (row // 3) + indx // 3][3 * (col // 3) + indx % 3] != 0:
                                num_constraints += 1
                        if row == col and self.game_board[indx][indx] != 0:
                                num_constraints += 1
                        if row + col == 8 and self.game_board[indx][8 - indx] != 0:
                                num_constraints += 1
                
                return num_constraints


        """
        VALID_VALUE

        This function checks if the value found is valid in line. It is going search the row it is in, and try to find an error in it
        """
        def valid_value(self, row, col, num):
                for i in range(9):
                        if (self.game_board[row][i] == num or  self.game_board[i][col] == num):
                                return False
                        elif(self.game_board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num): #3x3 block
                                return False
                        elif(row == col and self.game_board[i][i] == num): #45 diagonal
                                return False
                        elif((row + col == 8 and self.game_board[i][8 - i] == num)):  # Check 135 diagonal
                                return False
                return True



sdk = Sodoku('Sample_Input.txt', 'SampleIO.txt')
