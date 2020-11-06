# This is responsible for storing info and state and determine

class GameState():
    def __init__(self):
        # board is a list the first character represent color
        # second denotes type of character
        # "--" denotes no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves,
                              'N': self.getKnightMoves, 'B': self.getBishopMoves, 'K': self.getKingMoves, 'Q': self.getQueenMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = () # coordinates for the square where en passant capture is possible


# takes a move as  a parameter and executes it

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo later
        self.whiteToMove = not self.whiteToMove  # swap players
        # update king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # pawn promotion
        if move.isPawnPromotion:
            promotedPiece = input("Promote to Q, R, B, or N: ")
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece

        #update enpassant variable
        if move.pieceMoved[1]== 'p' and abs(move.startRow - move.endRow) == 2: # only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()
        
        # enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--" # capturing the pawn
# undo function
    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure there is move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turn back
            # update the king's position if needed
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            # undo enpassant moves
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--" # leave landing square block
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            # undo a 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

# all moves considering checks
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:  # only 1 check, block or move king
                moves = self.getAllPossibleMoves()
                # to block a check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                # enemy piece causing the check
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []  # squares that pieces can move to
                # if knight, must capture knight or move king, other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        # check[2] and check[3] are the directions
                        validSquare = (kingRow+check[2]*i, kingCol+check[3]*i)
                        validSquares.append(validSquare)
                        # once you get to piece and checks
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                    # get rid of any moves that dont block check or move king
                    # go through backwards when you are removing form a list as iterating
                for i in range(len(moves)-1, -1, -1):
                        # move doesnt move king so it must block or capture
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow,moves[i].endCol) in validSquares:
                            moves.remove(moves[i])

            else:  # double check , king has to move
                self.getKingMoves(kingRow, kingCol, moves)

        else:  # not in check so all moves are fine
            moves = self.getAllPossibleMoves()
        
        return moves

    # def getValidMoves(self):
    #     # 1.) generate all possible moves
    #     moves = self.getAllPossibleMoves()
    #     # 2.) for each mpve , make the move
    #     # when removing from a list go backwords through that list
    #     for i in range(len(moves)-1, -1, -1):
    #         self.makeMove(moves[i])
    #         # 3.) generate all opponent's moves
    #         # 4.) for each of your opponent's moves, see if thet attack your king
    #         self.whiteToMove = not self.whiteToMove
    #         if self.inCheck():
    #             # 5.) if they do attack your king, not a valid move
    #             moves.remove(moves[i])
    #         self.whiteToMove = not self.whiteToMove
    #         self.undoMove()
    #     if len(moves)==0: # either checkmate or stalemate
    #         if self.inCheck():
    #             self.checkMate = True
    #         else:
    #             self.staleMate = True
    #     else:
    #         self.checkMate = False
    #         self.staleMate = False
    #     return moves  # checks are not implemented

    # Determine if current player is in check

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # Determine if enemy can attack square r,c

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # square is under attack
                return True
        return False
    # All moves withot considering checks

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # no of rows in
            for c in range(len(self.board[r])):  # no of col in row
                turn = self.board[r][c][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    # calls the appropriate move function based on piece type
                    self.moveFunctions[piece](r, c, moves)

        return moves

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'b'
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'w'
        isPawnPromotion = False

        if self.board[r+moveAmount][c] == "--": #1 square move
            if not piecePinned or pinDirection == (moveAmount,0):
                if r+moveAmount == backRow: #if piece gets to back rank it is a pawn promotion
                    isPawnPromotion = True
                moves.append(Move((r,c), (r+moveAmount, c), self.board, isPawnPromotion=isPawnPromotion))
                if r == startRow and self.board[r+2*moveAmount][c] == "--": # 2 square moves
                    moves.append(Move((r,c), (r+2*moveAmount, c), self.board))
        
        if c-1 >= 0: #capture left
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor:
                    if r + moveAmount == backRow: #if piece gets to back rank then it is a pawn promotion
                        isPawnPromotion = True
                    moves.append(Move((r,c), (r+moveAmount, c-1), self.board, isPawnPromotion=isPawnPromotion))
                if (r + moveAmount, c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r+moveAmount, c-1), self.board, isEnpassantMove=True))
        
        if c+1 <= 7: #capture right
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:
                    if r + moveAmount == backRow: #if piece gets to back rank then it is a pawn promotion
                        isPawnPromotion = True
                    moves.append(Move((r,c), (r+moveAmount, c+1), self.board, isPawnPromotion=isPawnPromotion))
                if (r + moveAmount, c+1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r+moveAmount, c+1), self.board, isEnpassantMove=True))

# Get Move Function for  Rook

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                # cannt remove queen form pin on rook moves, only remove it on bishop moves
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])

                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up,down,left,right
        # this is terneary way of writing dont edit
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r+d[0]*i
                endCol = c+d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # empty space valid
                            moves.append(
                                Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:  # enemy piece valid
                            moves.append(
                                Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piece invalid
                            break
                else:
                    break


# Get Move Function for Kinght

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r+m[0]
            endCol = c+m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    # not an ally piece (empty or enemy piece)
                    if endPiece[0] != allyColor:
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))


# Get Move Function for Bishop

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # diagonals
        # this is terneary way of writing dont edit
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r+d[0]*i
                endCol = c+d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # empty space valid
                            moves.append(
                                Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:  # enemy piece valid
                            moves.append(
                                Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piece invalid
                            break
                else:
                    break


# Get Move Function for Queen

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

# Get Move Function for King

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r+rowMoves[i]
            endCol = c+colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)


   # All moves considering checks

    def checkForPinsAndChecks(self):
        pins = []  # squares where the allied pinned pieces is and direction pinned from
        checks = []  # squares where enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        # check outwards from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()  # reset possible pins
            for i in range(1, 8):
                endRow = startRow+d[0]*i
                endCol = startCol+d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1]!='K':
                        if possiblePin == ():  # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if(0 <= j <=3 and type =='R') or (4 <= j <=7 and type=='B') or (i == 1 and type == 'p' and ((enemyColor=='w' and 6<=j<=7) or (enemyColor=='b' and 4<=j<=5))) or (type=='Q') or (i==1 and type=='K'):
                            if possiblePin==(): #no piece blocking, so check
                                inCheck=True
                                checks.append((endRow,endCol,d[0],d[1]))
                                break
                            else:#piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else:#enemy piece not applying check
                            break
                else:
                    break #off board
        # check for knight checks
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        for m in knightMoves:
            endRow=startRow+m[0]
            endCol =startCol+m[1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]==enemyColor and endPiece[1]=='N':#enemy knight attacking king
                    inCheck=True
                    checks.append((endRow,endCol,m[0],m[1]))
        return inCheck, pins,checks
            
            



class Move():

    # maps keys to values
    # key:value
    ranksToRows = {"1": 7, "2": 6, "3": 5,
                   "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    rowsToRanks = {v: k for k, v in ranksToRows.items()}  # reversing keys
    filesToCols = {"a": 0, "b": 1, "c": 2,
                   "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isPawnPromotion=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # pawn promotion
        # self.isPawnPromotion = ((self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7))
        self.isPawnPromotion = isPawnPromotion

        # en passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        self.moveID = self.startRow*1000 + self.startCol*100+self.endRow*10+self.endCol
        # print(self.moveID)

    # overriding the equal method

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # add to make like real chess notation
        return self.getRankFile(self.startRow, self.startCol)+self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c]+self.rowsToRanks[r]
