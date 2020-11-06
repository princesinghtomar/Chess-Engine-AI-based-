# This is the main driver code responsible of user input


import pygame as p
import ChessEngine

# from Chess import ChessEngine  #this is not working

WIDTH = HEIGHT = 512 *2 # 400 is another option
DIMENSION = 8  # CHESSBOARD 8*8
SQ_SIZE = HEIGHT  // DIMENSION
MAX_FPS = 15  # FOR ANIMATION LATER ON
IMAGES = {}

# load image will initialize a global dictionary of images only once in a code


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK','wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        # IMAGES[piece] =p.image.load("./"+piece+".png" )
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))

# this will be main driver it will handle
# user input and update the graphics


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    # print(gs.board)
    
    validMoves=gs.getValidMoves()
    moveMade=False  # flag variable when a move is made

    loadImages()
    running = True
    sqSelected=() # keeps track of last call of user
    playerClicks=[] #keeps track of players click
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False 
           
            #mouse handler

            elif e.type==p.MOUSEBUTTONDOWN:
                location=p.mouse.get_pos() #get mouse coordinates 
                col=location[0]//SQ_SIZE
                row=location[1]//SQ_SIZE
                if sqSelected==(row,col): #reset if clicked on same block
                    sqSelected=()
                    playerClicks=[]
                else:
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected) #append for both first and second clicks
                if len(playerClicks)==2: #after 2nd click
                    move=ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade=True
                        sqSelected=() #reset user clicks
                        playerClicks=[]
                    else:
                        playerClicks=[sqSelected]

            #key handler

            elif e.type==p.KEYDOWN:
                if e.key==p.K_z:#undo a move by pressing z 
                #need to implement this using undo button also %%
                    gs.undoMove()
                    moveMade=True
        
        if moveMade:
            validMoves=gs.getValidMoves()
            moveMade=False       
                 


        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()



# Responsible for all the graphics within a current game state

def drawGameState(screen, gs):
    drawBoard(screen)  # drawa sqares on board
    # add in piece highlighting or move suggestion (later)
    drawPieces(screen, gs.board)  # draw pieces on top of those squares


# Draw the squares on the board top left is always white

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            # color = colors[((1) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


# Draw the pieces on the board using the current GameState.board

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece=board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

if __name__ == "__main__":
    main()
