import math
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
        #the game board itself, array of arrays
        self.game_board = []

        #read the board in
        self.board_read_in(import_file)

        #play the game
        self.play_sudoku()

        #read it out
        self.board_read_out(export_file)
        
    """
    BOARD READ IN

    will read the file sent through the program into a gameBoard that will be used to do all the work
    """
    def board_read_in(self, import_file):
        file = open(import_file, 'r')
        lines = file.readlines()
        
        #go through all the lines
        for line in lines:

            board_row = []
            
            for num in line.split():
                #split and add to master gameboard array
                board_row.append(int(num))

            self.game_board.append(board_row)

        file.close()

    """
    BOARD READ OUT

    This takes the gameboard and reads it back into the destination file. Granted this could be the same file, but must be specified. 
    """
    def board_read_out(self, export_file):
        file = open(export_file, 'w')

        #go through line by line and read back into the file.
        for row in self.game_board:
            file.write(' '.join(map(str,row)) + '\n')

        file.close()



    """
    PLAY_SODOKU

    This is the master function that runs the backtracking and goes through everything 
    """
    def play_sudoku(self):
        #the empty calls the heuristic methods, but not in the recursive backtracking function
        empty = self.find_empty()
        if empty:
            row, col = empty
        else:
            return True
        
        #go in order, except those that are used already
        for num in self.domain_order(row, col):
            #look for valid values
            if self.valid_val(row, col, num):
                #set and recursively call
                self.game_board[row][col] = num
                if self.play_sudoku():
                    return True
                else:
                    #backtracking
                    self.game_board[row][col] = 0
        return False

    """
    Find Empty

    This is going to go throughout the gameboard and find the first item that it can that is 0, then return that value
    """
    def find_empty(self):
        #go through each row
        for i, row in enumerate(self.game_board):
            #go through each item in each row
            for j, num in enumerate(row):
                #return inf match
                if num == 0:
                    return i, j
        return False # was either False or None, doesn't make a huge difference
    

    """
    Valid Value

    This valid value system is going to check if the theorized solution has a match already in the order system that could cause a problem. It is essentially a gut checking system throughout the program
    """    
    def valid_val(self, row, col, num):
        #basic check if it's in the same row or column
        for i in range(9):
            if self.game_board[row][i] == num or self.game_board[i][col] == num:
                return False

        #check for a diagonal match
        for i in range(3):
            for j in range(3):
                #had to Google how to do a diagonal match, luckily lots of blocks
                if self.game_board[3 * (row // 3) + i][3 * (col // 3) + j] == num:
                    return False

        return True

    """
    domain_order

    This function goes through the domain order originally in chronological order, but after trial also adds into a set all the numbers it could not be to eliminate that before returning the right answer

    This is also the most important because it is where we decided to use the degree heuristic and minimum remaining variable
    """
    def domain_order(self, row, col):

        used_nums = []

        for all_indxs in range(9):
            used_nums.append(self.game_board[row][all_indxs])
            used_nums.append(self.game_board[all_indxs][col])
            used_nums.append(self.game_board[3 * (row // 3) + all_indxs // 3][3 * (col // 3) + all_indxs % 3])
        
        possible_values = []
        for indx in range(1, 10):
            if indx not in used_nums:
                possible_values.append(indx)

        # found online this was a good way to do the balancing, works beautifully and logically makes sense
        possible_values.sort(key=lambda x: (self.mrv(row, col, x), self.dh(row, col)))

        return possible_values


    """
    MINIMUM REMAINING VARIABLE

    This function is going to calculate the number of close restraints to factor this into the equation
    """
    def mrv(self, row, col, num):
        num_cnstrnts = 0
        for i in range(9):
            
            #add constraint based on horizontal or vertical
            if self.game_board[row][i] == num or self.game_board[i][col] == num:
                num_cnstrnts += 1

            #add constraint based on 45 or 135 degrees
            if self.game_board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
                num_cnstrnts += 1
        return num_cnstrnts


    """
    Degree Heuristic

    Calculates the number of things that would be affected by a choice on the one
    """
    def dh(self, row, col):
        affected_degrees = 0
        for indx in range(9):
            if self.game_board[row][indx] == 0:
                affected_degrees += 1
            if self.game_board[indx][col] == 0:
                affected_degrees += 1
            if self.game_board[3 * (row // 3) + indx // 3][3 * (col // 3) + indx % 3] == 0:
                affected_degrees += 1
        return affected_degrees
        



sdk = Sodoku('Input3.txt', 'Input3_Out.txt')