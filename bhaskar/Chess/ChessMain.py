# This is the main driver code responsible of user input


import pygame as p
import ChessEngine

# from Chess import ChessEngine  #this is not working

WIDTH = HEIGHT = 800  # 400 is another option
DIMENSION = 8  # CHESSBOARD 8*8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # FOR ANIMATION LATER ON
IMAGES = {}

# load image will initialize a global dictionary of images only once in a code


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK',
              'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        # IMAGES[piece] =p.image.load("./"+piece+".png" )
        IMAGES[piece] = p.transform.scale(p.image.load(
            "images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))

# this will be main driver it will handle
# user input and update the graphics


def main():
    p.init()
    screen = p.display.set_mode((WIDTH+50, 50+HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color(0x000F0F))
    gs = ChessEngine.GameState()
    # print(gs.board)

    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable when a move is made
    animate = False #flag variable for when we should animate a move
    loadImages()
    running = True
    initial = ()
    final = ()
    sqSelected = ()  # keeps track of last call of user
    playerClicks = []  # keeps track of players click
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # mouse handler

            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()  # get mouse coordinates
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):  # reset if clicked on same block
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        # append for both first and second clicks
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:  # after 2nd click
                        move = ChessEngine.Move(
                            playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()  # reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            # key handler

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo a move by pressing z
                    # need to implement this using undo button also %%
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: #reset the board when 'r' is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    final = ()
                    initial = ()
                    sqSelected = ()
                    final=()
                    initial=()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            # if(gs.moveLog[-1]):
            if(len(gs.moveLog)>=1):
                final = (gs.moveLog[-1].endRow, gs.moveLog[-1].endCol)
                initial = (gs.moveLog[-1].startRow, gs.moveLog[-1].startCol)
            else:
                initial = ()
                final = ()

        drawGameState(screen, gs, validMoves, sqSelected, initial ,final)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')
        
        clock.tick(MAX_FPS)
        p.display.flip()

#highlight last move made by opponent
def lastMove(screen, gs, initial, final):
    if initial != () and final != ():
        ri, ci = initial
        rf, cf = final
        si = p.Surface((SQ_SIZE, SQ_SIZE))
        si.set_alpha(100)
        si.fill(p.Color('green'))
        sf = p.Surface((SQ_SIZE, SQ_SIZE))
        sf.set_alpha(100)
        sf.fill(p.Color('purple'))
        # print(initial, final)
        screen.blit(si, (ci*SQ_SIZE, ri*SQ_SIZE))
        screen.blit(sf, (cf*SQ_SIZE, rf*SQ_SIZE))

# Highlight square selected and moves for piece selected
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # square selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100) # transparency value (0,255)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))



# Responsible for all the graphics within a current game state

def drawGameState(screen, gs, validMoves, sqSelected, initial ,final):
    drawBoard(screen)  # drawa sqares on board
    # add in piece highlighting or move suggestion (later)
    highlightSquares(screen, gs, validMoves, sqSelected)
    lastMove(screen, gs,initial ,final)
    drawPieces(screen, gs.board)  # draw pieces on top of those squares


# Draw the squares on the board top left is always white

def drawBoard(screen):
    global colors
    colors = [p.Color(202,164,114), p.Color(93,67,44)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            # color = colors[((1) % 2)]
            p.draw.rect(screen, color, p.Rect(
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    for r in range(1,9):
        var=chr(96+r)
        drawText2(screen,var,r*100-50,825)
    for r in range(1,9):
        var=chr(48-r+9)
        drawText2(screen,var,825,r*100-50)
    


# Draw the pieces on the board using the current GameState.board

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], p.Rect(
                    c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Animating a move
def animateMove(move, screen, board, clock):
    global colors
    coords = [] # list of coords that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square
    frameCount = (abs(dR) + abs(dC))*framesPerSquare
    for frame in range(frameCount + 1):
        r, c = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the pice moved from its ending swuare
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject =  font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2,2))

def drawText2(screen, text ,a,b):
    font = p.font.SysFont("Helvitca", 50, True, False)
    textObject =  font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(a - textObject.get_width()/2, b - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("white"))
    screen.blit(textObject, textLocation.move(2,2))




if __name__ == "__main__":
    main()
