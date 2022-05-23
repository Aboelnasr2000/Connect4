import numpy as np
from Constants import *


def create_board():
    matrix = np.zeros((ROW, COLUMN))
    return matrix


def print_board(board):
    new_board = np.flip(board, 0)
    print(new_board)


def valid_location(board, column):
    return board[5][column] == 0


def fullboard(board):
    for c in range(COLUMN):
        if board[5][c] == 0:
            return False
    return True


def next_row(board, column):
    for r in range(ROW):
        if board[r][column] == 0:
            return r


def drop_piece(board, row, column, piece):
    board[row][column] = piece
