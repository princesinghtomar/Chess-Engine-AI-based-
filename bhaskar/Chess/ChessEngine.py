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
        self.moveFunctions={'p':self.getPawnMoves,'R':self.getRookMoves,
        'N':self.getKnightMoves,'B':self.getBishopMoves,'K':self.getKingMoves,'Q':self.getQueenMoves}
        self.whiteToMove = True
        self.moveLog = []


# takes a move as  a parameter and executes it


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo later
        self.whiteToMove = not self.whiteToMove  # swap players

# undo function
    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure there is move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turn back

    # All moves considering checks

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    # All moves withot considering checks

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # no of rows in
            for c in range(len(self.board[r])):  # no of col in row
                turn = self.board[r][c][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) #calls the appropriate move function based on piece type

        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn move
            if self.board[r-1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:  #captures to the left 
                if self.board[r-1][c-1][0]=='b': #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            
            if c+1 < 7: #captures to the right
                if self.board[r-1][c+1][0] =='b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else: #black pawn moves

            





# Get Move Function for  Rook

    def getRookMoves(self, r, c, moves):
        pass


# Get Move Function for Kinght

    def getKnightMoves(self, r, c, moves):
        pass

# Get Move Function for Bishop 

    def getBishopMoves(self, r, c, moves):
        pass

# Get Move Function for Queen

    def getQueenMoves(self, r, c, moves):
        pass

# Get Move Function for King

    def getKingMoves(self, r, c, moves):
        pass




class Move():

    # maps keys to values
    # key:value
    ranksToRows = {"1": 7, "2": 6, "3": 5,
                   "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    rowsToRanks = {v: k for k, v in ranksToRows.items()}  # reversing keys
    filesToCols = {"a": 0, "b": 1, "c": 2,
                   "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
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
