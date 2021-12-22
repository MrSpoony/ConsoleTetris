import time
import random
import getch



# Important Variables
rows = 12
collumns = 10


def cleanBoard():
# makes a clean 2x2Board with rows x collumns 
    board = [[]] * (rows+2)
    board[0].append(" "*collumns)

    for j in range(len(board)):
        for i in range(len(board[j])):
            board[j] = [char for char in board[j][i]]
    return board

def combineBoards(mainBoard, pieceBoard):
# Combines two boards to draw them
    finalBoard = cleanBoard()
    for i in range(len(mainBoard)):
        for j in range(len(mainBoard[i])):
            if mainBoard[i][j] != " ":
                finalBoard[i][j] = mainBoard[i][j]
            elif pieceBoard[i][j] != " ":
                finalBoard[i][j] = pieceBoard[i][j]
            else:
                finalBoard[i][j] = " "
    return finalBoard

def draw(board):
# Draws the 'board'
    print("\n\n\n\n\n")

    for i in range((len(board)-2)):
        print("\n#", end="", flush=True)
        for j in range(len(board[i+1])):
            print(board[i+2][j], end="", flush=True)
        print("#", end="", flush=True)

    print("\n", end="", flush=True)
    print("#"*(len(board[0])+2))
    print(f"\nSCORE: {Score}")

def addPieceatPos(block, x, y, board):
    # Adds Piece at exact pos to new Board
    pieceWidth = len(block[0])
    pieceHeight = len(block)
    pieceBoard = board

    for row in range(len(pieceBoard)):
        for j in range(len(pieceBoard[row])):
            if row >= y and row < y + pieceHeight and j >= x and j < x+pieceWidth:    
                pieceBoard[row][j] = block[row-y][j-x]
    return pieceBoard

def movePieceDown(board):
# Moves Piece one Line down
    newBoard = board
    newBoard.insert(0, newBoard.pop())
    return newBoard

def movePieceRight(board):
# Moves Piece one block to the right
    newBoard = board
    for row in newBoard:
        row.insert(0, row.pop())
    return newBoard

def movePieceLeft(board):
# Moves Piece one block to the left
    newBoard = board
    for row in newBoard:
        row.insert(len(row)-1, row.pop(0))
    return newBoard

def rotateLeft(board):
    return(reverseRows(giveTransformationOfPiece(board)))

def rotateRight(board):
    return(reverseCollumns(giveTransformationOfPiece(board)))

def deleteLine(board, lineNr):
# Removes bottom line
    global Score
    Score += 10
    newBoard = board
    newBoard.insert(0, newBoard.pop(lineNr))
    for i in range(len(newBoard[0])):
        newBoard[0][i] = " "

    if isFullLine(newBoard) != -1:
        draw(newBoard)
        time.sleep(0.4)
        deleteLine(newBoard, isFullLine(newBoard))
    else:
        return newBoard

def giveTransformationOfPiece(piece):
# Mirrors matrix diagonally
    transformedPiece = [[0 for x in range(len(piece))] for y in range(len(piece[0]))] 
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            transformedPiece[j][i] = piece[i][j]
    return transformedPiece


def reverseCollumns(piece):
# Reverses the Collumns of the matrix
    for i in piece:
        i.reverse()
    return piece

def reverseRows(piece):
# Reverses the Rows of the matrix
    piece.reverse()
    return piece


def nearBorder(piece):
# Is 'piece' near bottom
    for i in piece[-1]:
        if i != " ":
            return True
    return False


def nearPiece(piece, board):
# Gives a valid offset for block
    for row in range(len(piece)):
        for collum in range(len(piece[row])):
            if piece[row][collum] != " ":
                if board[row+1][collum] != " ":
                    return True
    return False


def giveOffset(piece):
# Gives a valid offset for block
    board = cleanBoard()
    widthBoard = len(board[0])
    pieceWidth = len(piece[0])
    return random.randint(0, widthBoard - pieceWidth)


def canMoveDown(piece, board):
# Kann man piece nach unten bewegen 
    if not nearBorder(piece):
        if not nearPiece(piece, board):
            return True
        else:
            return False
    else:
        return False


def isFullLine(board):
# If full line returns numer of line else returns -1
    for i in range(len(board)-1, -1, -1):
        count = 0
        for j in board[i]:
            if j != " ":
                count += 1
        if count == len(board[0]):
            return i
        else:
            return -1

def canRotateRight(piece, x, y, board):
# Can piece be rotated left
    piece = rotateRight(piece)
    pieceBoard = addPieceatPos(piece, x, y, cleanBoard())
    tetrominos = 0
    inOtherPieces = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != " ":
                pass
            elif pieceBoard[i][j] != " ":
                inOtherPieces += 1
    for i in range(len(pieceBoard)):
        for j in pieceBoard[i]:
            if j != " ":
                tetrominos += 1
    if tetrominos == 4 and inOtherPieces == 4:
        return True
    else:
        return False

def canRotateLeft(piece, x, y, board):
# Can piece be rotated right
    piece = rotateLeft(piece)
    pieceBoard = addPieceatPos(piece, x, y, cleanBoard())
    tetrominos = 0
    inOtherPieces = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != " ":
                pass
            elif pieceBoard[i][j] != " ":
                inOtherPieces += 1
    for i in range(len(pieceBoard)):
        for j in pieceBoard[i]:
            if j != " ":
                tetrominos += 1

    if tetrominos == 4 and inOtherPieces == 4:
        return True
    else:
        return False

def canMoveRight(piece, board):
# Can piece be rotated right 
    for row in range(len(piece)):
        for collum in range(len(piece[row])):
            if piece[row][collum] != " ": 
                if collum == len(piece[row])-1:
                    return False
                elif board[row][collum+1] != " ":
                    return False
    return True


def canMoveLeft(piece, board):
# Kann man piece nach links bewegen
    for row in range(len(piece)):
        for collum in range(len(piece[row])):
            if piece[row][collum] != " ": 
                if collum == 0:
                    return False
                elif board[row][collum-1] != " ":
                    return False
    return True

def countHashtags(board):
    count = 0
    for i in range(len(board)):
        for j in board[i]:
            if j != " ":
                count += 1
    return count
# Pieces
pieces = [

    [[" ", "#", " ", " "], 
     [" ", "#", " ", " "],
     [" ", "#", " ", " "], 
     [" ", "#", " ", " "]],

    [[" ", " ", "@"],
     ["@", "@", "@"],
     [" ", " ", " "]],

    [["*", " ", " "],
     ["*", "*", "*"],
     [" ", " ", " "]],

    [["%", "%", " "],
     [" ", "%", "%"],
     [" ", " ", " "]],

    [[" ", "&", "&"],
     ["&", "&", " "],
     [" ", " ", " "]],

    [[" ", "$", " "],
     ["$", "$", "$"],
     [" ", " ", " "]],

    [["#", "#"],
     ["#", "#"]]
]





mainBoard = cleanBoard()

gameOver = False
Score = 0


while True:




    currPiece = random.choice(pieces)
    randomRot = random.randint(0, 3)

    for i in range(randomRot):
        currPiece = rotateRight(currPiece)

    pieceBoard = cleanBoard()
    beginningOffset = giveOffset(currPiece)

    xPoscurrentPiece = beginningOffset
    yPoscurrentPiece = 0

    pieceBoard = addPieceatPos(currPiece, beginningOffset, 0, pieceBoard)
    Score += 1

    countMainBoard = countHashtags(mainBoard)
    countbothBoards = countHashtags(combineBoards(pieceBoard, mainBoard))

    if countbothBoards-4 != countMainBoard:
        break

    while True:
        if canMoveDown(pieceBoard, mainBoard):
            pass
        else:
            draw(combineBoards(pieceBoard, mainBoard))
            break

        draw(combineBoards(pieceBoard, mainBoard))


        key = ord(getch.getch())

        if key == 3:
            exit()
        if key == 113:
            if canRotateLeft(currPiece, xPoscurrentPiece, yPoscurrentPiece, mainBoard):
                currPiece = rotateLeft(currPiece)
                pieceBoard = addPieceatPos(currPiece, xPoscurrentPiece, yPoscurrentPiece, cleanBoard())
                key = 0
            if canMoveDown(pieceBoard, mainBoard):
                pieceBoard = movePieceDown(pieceBoard)
                yPoscurrentPiece += 1
            else:
                draw(combineBoards(pieceBoard, mainBoard))
                break
        elif key == 102:
            if canRotateRight(currPiece, xPoscurrentPiece, yPoscurrentPiece, mainBoard):
                currPiece = rotateRight(currPiece)
                pieceBoard = addPieceatPos(currPiece, xPoscurrentPiece, yPoscurrentPiece, cleanBoard())
                key = 0
            if canMoveDown(pieceBoard, mainBoard):
                pieceBoard = movePieceDown(pieceBoard)
                yPoscurrentPiece += 1
            else:
                draw(combineBoards(pieceBoard, mainBoard))
                break                
        elif key == 75 or key == 97:
            if canMoveLeft(pieceBoard, mainBoard):
                pieceBoard = movePieceLeft(pieceBoard)
                xPoscurrentPiece -= 1
                key = 0
            if canMoveDown(pieceBoard, mainBoard):
                pieceBoard = movePieceDown(pieceBoard)
                yPoscurrentPiece += 1
            else:
                draw(combineBoards(pieceBoard, mainBoard))
                break                
        elif key == 77 or key == 115:
            if canMoveRight(pieceBoard, mainBoard):
                pieceBoard = movePieceRight(pieceBoard)
                xPoscurrentPiece += 1
                key = 0
            if canMoveDown(pieceBoard, mainBoard):
                pieceBoard = movePieceDown(pieceBoard)
                yPoscurrentPiece += 1
            else:
                draw(combineBoards(pieceBoard, mainBoard))
                break
        elif key == 114:
            while canMoveDown(pieceBoard, mainBoard):
                pieceBoard = movePieceDown(pieceBoard)
                yPoscurrentPiece += 1
            else:
                draw(combineBoards(pieceBoard, mainBoard))
                break
        else:
            if canMoveDown(pieceBoard, mainBoard):
                pieceBoard = movePieceDown(pieceBoard)
                yPoscurrentPiece += 1
            else:
                draw(combineBoards(pieceBoard, mainBoard))
                break


        
    mainBoard = combineBoards(mainBoard, pieceBoard)
    if isFullLine(mainBoard) != -1:
        mainBoard = deleteLine(mainBoard, isFullLine(mainBoard))
        draw(mainBoard)

print("\n GAME OVER\n")
