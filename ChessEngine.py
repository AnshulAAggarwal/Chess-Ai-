class ChessState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'B': self.getBishopMoves,
                              'N': self.getKnightMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves
                              }
        self.whitemove = True
        self.movelog = []
        self.white_King_Location = (7, 4)
        self.black_King_Location = (0, 4)
        self.checkMate = False
        self.stalemate = False

    # this does not work for enpassant castle and pawn promotion
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.movelog.append(move)
        self.whitemove = not self.whitemove

        # update white king location
        if move.piece_moved == "wk":
            self.white_King_Location = (move.end_row, move.end_col)

        # update black king location
        elif move.piece_moved == "bk":
            self.black_King_Location = (move.end_row, move.end_col)

    # undo the last move

    def undo_move(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.whitemove = not self.whitemove

            # update white king location
            if move.piece_moved == "wk":
                self.white_King_Location = (move.start_row, move.start_col)

            # update black king location
            elif move.piece_moved == "bk":
                self.black_King_Location = (move.start_row, move.start_col)

    # moves considering check
    def get_Valid_Moves(self):
        # 1. generate all  moves
        moves = self.all_moves()

        # 2. for each move , make the move
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            # we are switching it back because make move switches the move
            self.whitemove = not self.whitemove
            # 3. for all of moves generate ur oppenent's moves
            # 4. see which of those moves attack ur king
            if self.in_check():
                moves.remove(moves[i])
            self.whitemove = not self.whitemove
            self.undo_move()
        if len(moves) == 0:
            if self.in_check():
                self.checkMate = True
            else:
                self.stalemate = True
        else:
            self.checkMate = False
            self.stalemate = False
        # 5. remove the moves which attack our king
        return moves

    # moves without considering checks
    # basically this method will provide all the possibles moves and get_Valid_Moves
    # will filter out the one which put the king is check

    def in_check(self):
        if self.whitemove:
            return self.square_under_attack(self.white_King_Location[0], self.white_King_Location[1])
        else:
            return self.square_under_attack(self.black_King_Location[0], self.black_King_Location[1])

    # check this piece at r,c is under attack
    def square_under_attack(self, r, c):
        self.whitemove = not self.whitemove  # switch to enemy
        oppmoves = self.all_moves()
        self.whitemove = not self.whitemove
        for move in oppmoves:
            if move.end_row == r and move.end_col == c:
                return True
        return False

    def all_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whitemove) or (turn == 'b' and not self.whitemove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # calls the apt move function
        return moves

    # get that pawn's moves

    def getPawnMoves(self, r, c, moves):
        if self.whitemove:
            if self.board[r - 1][c] == "--":  # 1 step move
                moves.append(move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 step move
                    moves.append(move((r, c), (r - 2, c), self.board))
            if c + 1 < 8 and self.board[r - 1][c + 1][0] == "b":
                moves.append(move((r, c), (r - 1, c + 1), self.board))
            if c - 1 >= 0 and self.board[r - 1][c - 1][0] == "b":
                moves.append(move((r, c), (r - 1, c - 1), self.board))
        else:
            if self.board[r + 1][c] == "--":  # 1 step move
                moves.append(move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 step move
                    moves.append(move((r, c), (r + 2, c), self.board))
            if c + 1 < 8 and self.board[r + 1][c + 1][0] == "w":
                moves.append(move((r, c), (r + 1, c + 1), self.board))
            if c - 1 >= 0 and self.board[r + 1][c - 1][0] == "w":
                moves.append(move((r, c), (r + 1, c - 1), self.board))
                # get that Rook's Moves
        # add pawn promotions

    def getKingMoves(self, r, c, moves):
        if self.whitemove:
            if (r - 1 >= 0 and c - 1 >= 0) and (self.board[r - 1][c - 1] == "--" or self.board[r - 1][c - 1][0] == "b"):
                moves.append(move((r, c), (r - 1, c - 1), self.board))

            if (r - 1 >= 0 and c) and (self.board[r - 1][c] == "--" or self.board[r - 1][c][0] == "b"):
                moves.append(move((r, c), (r - 1, c), self.board))

            if (r - 1 >= 0 and c + 1 < 8) and (self.board[r - 1][c + 1] == "--" or self.board[r - 1][c + 1][0] == "b"):
                moves.append(move((r, c), (r - 1, c + 1), self.board))

            if (r and c - 1 >= 0) and (self.board[r][c - 1] == "--" or self.board[r][c - 1][0] == "b"):
                moves.append(move((r, c), (r, c - 1), self.board))

            if (r and c + 1 < 8) and (self.board[r][c + 1] == "--" or self.board[r][c + 1][0] == "b"):
                moves.append(move((r, c), (r, c + 1), self.board))

            if (r + 1 < 8 and c - 1 >= 0) and (self.board[r + 1][c - 1] == "--" or self.board[r + 1][c - 1][0] == "b"):
                moves.append(move((r, c), (r + 1, c - 1), self.board))

            if (r + 1 < 8 and c) and (self.board[r + 1][c] == "--" or self.board[r + 1][c][0] == "b"):
                moves.append(move((r, c), (r + 1, c), self.board))

            if (r + 1 < 8 and c + 1 < 8) and (self.board[r + 1][c + 1] == "--" or self.board[r + 1][c + 1][0] == "b"):
                moves.append(move((r, c), (r + 1, c + 1), self.board))
        else:
            if (r - 1 >= 0 and c - 1 >= 0) and (self.board[r - 1][c - 1] == "--" or self.board[r - 1][c - 1][0] == "w"):
                moves.append(move((r, c), (r - 1, c - 1), self.board))

            if (r - 1 >= 0 and c) and (self.board[r - 1][c] == "--" or self.board[r - 1][c][0] == "w"):
                moves.append(move((r, c), (r - 1, c), self.board))

            if (r - 1 >= 0 and c + 1 < 8) and (self.board[r - 1][c + 1] == "--" or self.board[r - 1][c + 1][0] == "w"):
                moves.append(move((r, c), (r - 1, c + 1), self.board))

            if (r and c - 1 >= 0) and (self.board[r][c - 1] == "--" or self.board[r][c - 1][0] == "w"):
                moves.append(move((r, c), (r, c - 1), self.board))

            if (r and c + 1 < 8) and (self.board[r][c + 1] == "--" or self.board[r][c + 1][0] == "w"):
                moves.append(move((r, c), (r, c + 1), self.board))

            if (r + 1 < 8 and c - 1 >= 0) and (self.board[r + 1][c - 1] == "--" or self.board[r + 1][c - 1][0] == "w"):
                moves.append(move((r, c), (r + 1, c - 1), self.board))

            if (r + 1 < 8 and c) and (self.board[r + 1][c] == "--" or self.board[r + 1][c][0] == "w"):
                moves.append(move((r, c), (r + 1, c), self.board))

            if (r + 1 < 8 and c + 1 < 8) and (self.board[r + 1][c + 1] == "--" or self.board[r + 1][c + 1][0] == "w"):
                moves.append(move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        if self.whitemove:
            i = r
            j = c + 1
            while (j < 8):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    j = j + 1
                elif self.board[i][j][0] == "b":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
            j = c - 1
            while (j > -1):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    j = j - 1
                elif self.board[i][j][0] == "b":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
            i = r - 1
            j = c
            while (i > -1):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    i = i - 1
                elif self.board[i][j][0] == "b":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
            i = r + 1
            while (i < 8):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    i = i + 1
                elif self.board[i][j][0] == "b":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
        else:
            i = r
            j = c + 1
            while (j < 8):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    j = j + 1
                elif self.board[i][j][0] == "w":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
            j = c - 1
            while (j > -1):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    j = j - 1
                elif self.board[i][j][0] == "w":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
            i = r - 1
            j = c
            while (i > -1):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    i = i - 1
                elif self.board[i][j][0] == "w":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
            i = r + 1
            while (i < 8):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    i = i + 1
                elif self.board[i][j][0] == "w":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break

    def getBishopMoves(self, r, c, moves):
        if self.whitemove:
            i = r - 1
            j = c + 1
            while (i >= 0 and j < 8):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    i = i - 1
                    j = j + 1
                elif self.board[i][j][0] == "b":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
            i = r + 1
            j = c + 1
            while (i < 8 and j < 8):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    i = i + 1
                    j = j + 1
                elif self.board[i][j][0] == "b":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
            i = r - 1
            j = c - 1
            while (i > -1 and j >= 0):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    i = i - 1
                    j = j - 1
                elif self.board[i][j][0] == "b":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
            i = r + 1
            j = c - 1
            while (i < 8 and j >= 0):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    i = i + 1
                    j = j - 1
                elif self.board[i][j][0] == "b":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
        else:
            i = r - 1
            j = c + 1
            while (i >= 0 and j < 8):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    i = i - 1
                    j = j + 1
                elif self.board[i][j][0] == "w":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
            i = r + 1
            j = c + 1
            while (i < 8 and j < 8):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    i = i + 1
                    j = j + 1
                elif self.board[i][j][0] == "w":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
            i = r - 1
            j = c - 1
            while (i > -1 and j >= 0):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    i = i - 1
                    j = j - 1
                elif self.board[i][j][0] == "w":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break
            i = r + 1
            j = c - 1
            while (i < 8 and j >= 0):
                if self.board[i][j] == "--":
                    moves.append(move((r, c), (i, j), self.board))
                    i = i + 1
                    j = j - 1
                elif self.board[i][j][0] == "w":
                    moves.append(move((r, c), (i, j), self.board))
                    break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        if self.whitemove:
            if (r - 1 >= 0 and c + 2 < 8) and (self.board[r - 1][c + 2] == "--" or self.board[r - 1][c + 2][0] == "b"):
                moves.append(move((r, c), (r - 1, c + 2), self.board))

            if (r + 1 < 8 and c + 2 < 8) and (self.board[r + 1][c + 2] == "--" or self.board[r + 1][c + 2][0] == "b"):
                moves.append(move((r, c), (r + 1, c + 2), self.board))

            if (r + 2 < 8 and c - 1 >= 0) and (self.board[r + 2][c - 1] == "--" or self.board[r + 2][c - 1][0] == "b"):
                moves.append(move((r, c), (r + 2, c - 1), self.board))

            if (r + 2 < 8 and c + 1 < 8) and (self.board[r + 2][c + 1] == "--" or self.board[r + 2][c + 1][0] == "b"):
                moves.append(move((r, c), (r + 2, c + 1), self.board))

            if (r - 1 > 0 and c - 2 >= 0) and (self.board[r - 1][c - 2] == "--" or self.board[r - 1][c - 2][0] == "b"):
                moves.append(move((r, c), (r - 1, c - 2), self.board))

            if (r + 1 < 8 and c - 2 >= 0) and (self.board[r + 1][c - 2] == "--" or self.board[r + 1][c - 2][0] == "b"):
                moves.append(move((r, c), (r + 1, c - 2), self.board))

            if (r - 2 > 0 and c + 1 < 8) and (self.board[r - 2][c + 1] == "--" or self.board[r - 2][c + 1][0] == "b"):
                moves.append(move((r, c), (r - 2, c + 1), self.board))

            if (r - 2 > 0 and c - 1 >= 0) and (self.board[r - 2][c - 1] == "--" or self.board[r - 2][c - 1][0] == "b"):
                moves.append(move((r, c), (r - 2, c - 1), self.board))
        else:
            if (r - 1 >= 0 and c + 2 < 8) and (self.board[r - 1][c + 2] == "--" or self.board[r - 1][c + 2][0] == "w"):
                moves.append(move((r, c), (r - 1, c + 2), self.board))

            if (r + 1 < 8 and c + 2 < 8) and (self.board[r + 1][c + 2] == "--" or self.board[r + 1][c + 2][0] == "w"):
                moves.append(move((r, c), (r + 1, c + 2), self.board))

            if (r + 2 < 8 and c - 1 >= 0) and (self.board[r + 2][c - 1] == "--" or self.board[r + 2][c - 1][0] == "w"):
                moves.append(move((r, c), (r + 2, c - 1), self.board))

            if (r + 2 < 8 and c + 1 < 8) and (self.board[r + 2][c + 1] == "--" or self.board[r + 2][c + 1][0] == "w"):
                moves.append(move((r, c), (r + 2, c + 1), self.board))

            if (r - 1 > 0 and c - 2 >= 0) and (self.board[r - 1][c - 2] == "--" or self.board[r - 1][c - 2][0] == "w"):
                moves.append(move((r, c), (r - 1, c - 2), self.board))

            if (r + 1 < 8 and c - 2 >= 0) and (self.board[r + 1][c - 2] == "--" or self.board[r + 1][c - 2][0] == "w"):
                moves.append(move((r, c), (r + 1, c - 2), self.board))

            if (r - 2 > 0 and c + 1 < 8) and (self.board[r - 2][c + 1] == "--" or self.board[r - 2][c + 1][0] == "w"):
                moves.append(move((r, c), (r - 2, c + 1), self.board))

            if (r - 2 > 0 and c - 1 >= 0) and (self.board[r - 2][c - 1] == "--" or self.board[r - 2][c - 1][0] == "w"):
                moves.append(move((r, c), (r - 2, c - 1), self.board))

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


class move():
    # GET THE CHESS NOTATION CORRECT

    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    # required in the future to undo moves
    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        # basically a basic HASH function

    def __eq__(self, other):
        if isinstance(other, move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
