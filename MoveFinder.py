import random

PieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0


def FindRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def FindBestMove(game_state, validMoves):
    TurnMultiplier = 1 if game_state.white_to_move else -1  # to tell whose turn it is and we trying to minimise of maximise
    OpponentMinmaxScore = CHECKMATE  # from black perspective it is worst possible score as it is positive
    bestPlayerMove = None
    random.shuffle(validMoves)

    for playerMove in validMoves:
        game_state.makeMove(playerMove)
        opponentMoves = game_state.getValidMoves()
        OpponentMaxScore = -CHECKMATE


        for opponentMove in opponentMoves:
            game_state.makeMove(opponentMove)
            if game_state.checkmate:
                score = -TurnMultiplier * CHECKMATE
            elif game_state.stalemate:
                score = STALEMATE
            else:
                score = -TurnMultiplier * scoreMaterial(game_state.board)

            if (score > OpponentMaxScore):
                OpponentMaxScore = score
            game_state.undoMove()
        if OpponentMaxScore < OpponentMinmaxScore:
            OpponentMinmaxScore = OpponentMaxScore
            bestPlayerMove = playerMove
        game_state.undoMove()

    return bestPlayerMove


'''
Score the board on the basis of material
'''


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += PieceScore[square[1]]
            if square[0] == "b":
                score -= PieceScore[square[1]]
    return score
