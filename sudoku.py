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
        # this function is called to see if there are any more moves, and to potentially end the game
    
        empty = self.find_next()
        if empty:
            row, col = empty
        else:
            return True
    
        #go in order, except those that are used already
        for num in self.domain_order():
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
    Remaining Values (RV)

    This function is the backbone of the mrv formula. It's job is to find the remaining values for a specific coordinate point
    """
    def rv(self, x, y):
        all_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for i in range(9):
            #values in other cols
            if self.game_board[x][i] in all_vals:
                all_vals.remove(self.game_board[x][i])

            #values in other rows
            if self.game_board[i][y] in all_vals:
                all_vals.remove(self.game_board[i][y])
        

        # Values in diagonal ends
        if x == y:  # Top-left to bottom-right diagonal
            for i in range(9):
                if self.game_board[i][i] in all_vals:
                    all_vals.remove(self.game_board[i][i])

        if x + y == 8:  # Top-right to bottom-left diagonal
            for i in range(9):
                if self.game_board[i][8 - i] in all_vals:
                    all_vals.remove(self.game_board[i][8 - i])

        return len(all_vals)


    """
    MINIMUM REMAINING VARIABLE

    This function is going to calculate the number of close restraints to factor this into the equation
    """
    def mrv(self, options):

        finalists = []
        final_rv = float("inf")

        for (x, y) in options:
            val = self.rv(x, y)
            if(val == final_rv):
                finalists.append((x, y))
            elif(val < final_rv):
                finalists = []
                finalists.append((x, y))
                final_rv = val

        return finalists
        


    def degrees(self, x, y):
        num_cnstrnts = 0
        
        for i in range(9):
            #values in other cols
            if self.game_board[x][i] != 0:
                num_cnstrnts += 1

            #values in other rows
            if self.game_board[i][y] != 0:
                num_cnstrnts += 1
        

        # Values in diagonal ends
        if x == y:  # Top-left to bottom-right diagonal
            for i in range(9):
                if self.game_board[i][i] != 0:
                    num_cnstrnts += 1

        if x + y == 8:  # Top-right to bottom-left diagonal
            for i in range(9):
                if self.game_board[i][8 - i] != 0:
                    num_cnstrnts += 1

        return num_cnstrnts

    """
    Degree Heuristic

    This calculates the number of constraints on itself
    """
    def dh(self, options):
        finalists = []
        final_deg = float("inf")

        for (x, y) in options:
            val = self.degrees(x, y)
            if(val == final_deg):
                finalists.append((x, y))
            elif(val < final_deg):
                finalists = []
                finalists.append((x, y))
                final_deg = val

        return finalists


    """
    Find Empty

    This is going to go throughout the gameboard and find the first item that it can that is 0, then return that value
    """
    def find_next(self):
        #go through each row
        options = []

        for x in range(len(self.game_board)):
            for y in range(len(self.game_board[x])):
                if(self.game_board[x][y] == 0):
                   options.append((x, y)) 
        if(len(options) == 0):
            return False

        mrvs = self.mrv(options)
        if(len(mrvs) >= 2):
            dhs = self.dh(mrvs)
            return dhs[0]
        return mrvs[0]

    

    """
    Valid Value

    This valid value system is going to check if the theorized solution has a match already in the order system that could cause a problem. It is essentially a gut checking system throughout the program
    """    
    def valid_val(self, row, col, num):
        #basic check if it's in the same row or column
        for i in range(9):
            if self.game_board[row][i] == num or self.game_board[i][col] == num:
                return False
            
            if(self.game_board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num):
                return False

        #check for a diagonal match
        for i in range(3):
            for j in range(3):
                #had to Google how to do a diagonal match, luckily lots of blocks
                if self.game_board[3 * (row // 3) + i][3 * (col // 3) + j] == num:
                    return False

                
        if row == col:  # Top-left to bottom-right diagonal
            for indx in range(9):
                if self.game_board[indx][indx] == num:
                    return False

        if row + col == 8:  # Top-right to bottom-left diagonal
            for indx in range(9):
                if self.game_board[indx][8 - indx] == num:
                    return False

        return True


    """
    domain_order

    This function could eventually be changed for more complex operations, but right now just goes in order from 1-9
    """
    def domain_order(self):
        return range(1, 10)



    
        



sdk = Sodoku('nyti.txt', 'nyto.txt')