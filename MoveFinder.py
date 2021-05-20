import random

PieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3


def FindRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


# def FindBestMove(game_state, validMoves):
#     TurnMultiplier = 1 if game_state.white_to_move else -1  # to tell whose turn it is and we trying to minimise of maximise
#     OpponentMinmaxScore = CHECKMATE  # from black perspective it is worst possible score as it is positive
#     bestPlayerMove = None
#     random.shuffle(validMoves)
#
#     for playerMove in validMoves:
#         game_state.makeMove(playerMove)
#         opponentMoves = game_state.getValidMoves()
#         if game_state.stalemate:
#             OpponentMaxScore = STALEMATE
#         elif game_state.checkmate:
#             OpponentMaxScore = -CHECKMATE
#         else:
#             OpponentMaxScore = -CHECKMATE
#             for opponentMove in opponentMoves:
#                 game_state.makeMove(opponentMove)  # ineffiency here
#                 # Todo:  Make this work without making this
#                 game_state.getValidMoves()
#                 if game_state.checkmate:
#                     score = CHECKMATE
#                 elif game_state.stalemate:
#                     score = STALEMATE
#                 else:
#                     score = -TurnMultiplier * scoreMaterial(game_state.board)
#
#                 if (score > OpponentMaxScore):
#                     OpponentMaxScore = score
#                 game_state.undoMove()
#         if OpponentMaxScore < OpponentMinmaxScore:
#             OpponentMinmaxScore = OpponentMaxScore
#             bestPlayerMove = playerMove
#         game_state.undoMove()
#
#     return bestPlayerMove
#

'''
Score the board on the basis of material
'''


# helper method to make the first recursive ca;;
def FindBestMove(game_state, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMaxAplhaBetaPruning(game_state, validMoves, DEPTH,-CHECKMATE,CHECKMATE, 1 if game_state.white_to_move else -1)
    return nextMove


def FindMoveMinMax(game_state, validMoves, depth, whiteToMove):
    global nextMove
    # base case
    if depth == 0:
        return scoreMaterial(game_state.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            game_state.makeMove(move)
            nextMoves = game_state.getValidMoves()
            score = FindMoveMinMax(game_state, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            game_state.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            game_state.makeMove(move)
            nextMoves = game_state.getValidMoves()
            score = FindMoveMinMax(game_state, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            game_state.undoMove()
        return minScore


def findMoveNegaMaxAplhaBetaPruning(game_state, validMoves, depth, aplha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(game_state)

    maxScore = -CHECKMATE
    for move in validMoves:
        game_state.makeMove(move)
        nextMoves = game_state.getValidMoves()
        score = -findMoveNegaMaxAplhaBetaPruning(game_state, nextMoves, depth - 1, -beta, -aplha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        game_state.undoMove()
        if maxScore > aplha: #pruning happens
            aplha = maxScore
        if aplha >= beta:
            break
    return maxScore


def findMoveNegaMax(game_state, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreMaterial(game_state.board)

    maxScore = -CHECKMATE
    for move in validMoves:
        game_state.makeMove(move)
        nextMoves = game_state.getValidMoves()
        score = -findMoveNegaMax(game_state, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        game_state.undoMove()
    return maxScore


def scoreBoard(game_state):
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif game_state.stalemate:
        return STALEMATE

    score = 0
    for row in game_state.board:
        for square in row:
            if square[0] == "w":
                score += PieceScore[square[1]]
            if square[0] == "b":
                score -= PieceScore[square[1]]
    return score


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += PieceScore[square[1]]
            if square[0] == "b":
                score -= PieceScore[square[1]]
    return score
