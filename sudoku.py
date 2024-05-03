def intialize_board(fileName)
        with open(fileName, 'r') as file:
                lines = file.readlines()
                board = []
                for line in lines:
                        board_row = []
                        for num in line.split():
                                board_row.append(int(num))
                        board.append(board_row)
                return board