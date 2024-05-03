def intialize_board(fileName):
        file = open(fileName, 'r')
        lines = file.readlines()
        board = []
        for line in lines:
                board_row = []
                for num in line.split():
                        board_row.append(int(num))
                board.append(board_row)
        file.close()
        return board

def board_to_file(board, fileName):
        file = open(fileName, 'w')
        for row in board:
                file.write(' '.join(map(str,row)) + '\n')
        file.close()

def empty_square(board):
        for i in range(len(board)-1):
                for j in range(len(board[0]) -1 ):
                        if board[i][j] == 0:
                                return i, j
        return None