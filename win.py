from Constants import *


def wining_move(board, piece):
    for c in range(COLUMN - 3):  # Horizontal win
        for r in range(ROW):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                # print("Congrats You Won !!!")
                return True

    for c in range(COLUMN):
        for r in range(ROW - 3):  # Vertical Win
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                # print("Congrats You Won !!!")
                return True

    for c in range(COLUMN - 3):
        for r in range(ROW - 3):  # Right slope Win
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                # print("Congrats You Won !!!")
                return True

    for c in range(COLUMN - 3):
        for r in range(3, ROW):  # Left slope Win
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                # print("Congrats You Won !!!")
                return True
