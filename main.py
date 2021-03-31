import pygame as game

from chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_Fps = 69
IMAGES = {}


# initialize a global dictionary - it will be called once to make the board
def loadImages():
    pieces = ['wp', 'bp', 'wR', 'bR', 'wN', 'bN', 'wB', 'bB', 'wQ', 'bQ', 'wK', 'bK']
    for piece in pieces:
        IMAGES[piece] = game.transform.scale(game.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


# handles use cases
def main():
    game.init()
    screen = game.display.set_mode((WIDTH, HEIGHT))
    clock = game.time.Clock()
    screen.fill(game.Color("white"))
    gs = ChessEngine.ChessState()
    validMoves = gs.get_Valid_Moves()
    moveMade = False
    print(gs.board)
    loadImages()
    running = True
    squareSelected = ()  # keep track of the last click  (row, col)
    playerClicks = []  # keep traack of player clicks  [(),()]

    while running:
        for i in game.event.get():
            if i.type == game.QUIT:
                running = False
            # mouse handler
            elif i.type == game.MOUSEBUTTONDOWN:
                location = game.mouse.get_pos()  # x,y location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if squareSelected == (row, col):  # same click twice
                    squareSelected = ()
                    playerClicks = []
                else:
                    squareSelected = (row, col)
                    playerClicks.append(squareSelected)
                if len(playerClicks) == 2:  # a move has been made
                    move = ChessEngine.move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.get_chess_notation())
                    if move in validMoves:
                        gs.make_move(move)
                        moveMade = True

                    squareSelected = ()  # reset user clicks to play along
                    playerClicks = []

            # key_handlers
            elif i.type == game.KEYDOWN:
                if i.key == game.K_z:
                    gs.undo_move()
                    moveMade = True
        if moveMade:
            validMoves = gs.get_Valid_Moves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_Fps)
        game.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [game.Color("white"), game.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            game.draw.rect(screen, color, game.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], game.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
