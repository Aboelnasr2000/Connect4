import sys
from main import *
from board import *
from win import *
from Node import *
import math

WINDOW = 4


def pick_best_move(Board, piece):
    valid_locations = get_valid_locations(Board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        Row = next_row(Board, col)
        temp_board = Board.copy()
        drop_piece(temp_board, Row, col, piece)
        Score = score_position(temp_board, piece)
        if Score > best_score:
            best_score = Score
            best_col = col

    return best_col


def OPminimax(Board, depth, alpha, beta, maximizingPlayer, root, nodes):
    valid_locations = get_valid_locations(Board)
    is_terminal = is_terminal_node(Board)
    if fullboard(Board):
        root.score = score_board(Board, AI_Piece) - score_board(Board, PLAYER_Piece)
        return None, root.score, 1
    elif not depth:  # Depth is zero
        root.score = score_position(Board, AI_Piece)
        return None, root.score, 1
    Nonodes = 1
    if maximizingPlayer:
        value = -math.inf
        Column = random.choice(valid_locations)
        for col in valid_locations:
            Row = next_row(Board, col)
            b_copy = Board.copy()
            drop_piece(b_copy, Row, col, AI_Piece)
            childNode = Node(root, -sys.maxsize, not root.max_or_min)
            root.addChild(childNode)
            array = OPminimax(b_copy, depth - 1, alpha, beta, False, childNode, Nonodes)
            new_score = array[1]
            Nonodes = Nonodes + array[2]
            if new_score > value:
                value = new_score
                Column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                root.score = str(value) + "Pruned"
                break
        root.score = value
        return Column, value, Nonodes

    else:  # Minimizing player
        value = math.inf
        Column = random.choice(valid_locations)
        for col in valid_locations:
            Row = next_row(Board, col)
            b_copy = Board.copy()
            drop_piece(b_copy, Row, col, PLAYER_Piece)
            childNode = Node(root, -sys.maxsize, not root.max_or_min)
            root.addChild(childNode)
            array = OPminimax(b_copy, depth - 1, alpha, beta, False, childNode, Nonodes)
            new_score = array[1]
            Nonodes = Nonodes + array[2]
            if new_score < value:
                value = new_score
                Column = col
            beta = min(beta, value)
            if alpha >= beta:
                root.score = str(value) + "Pruned"
                break
        root.score = value
        return Column, value, Nonodes


def get_valid_locations(Board):
    valid_locations = []
    for col in range(COLUMN):
        if valid_location(Board, col):
            valid_locations.append(col)
    return valid_locations


def evaluate_board(window, piece):
    Score = 0
    if window.count(piece) == 4:
        Score += 100
    return Score


def score_board(Board, piece):
    Score = 0
    # Score Horizontal
    for r in range(ROW):
        row_array = [int(i) for i in list(Board[r, :])]
        for c in range(COLUMN - 3):
            window = row_array[c:c + WINDOW]
            Score += evaluate_board(window, piece)

    # Score Vertical
    for c in range(COLUMN):
        col_array = [int(i) for i in list(Board[:, c])]
        for r in range(ROW - 3):
            window = col_array[r:r + WINDOW]
            Score += evaluate_board(window, piece)

    # Score Positive sloped diagonal
    for r in range(ROW - 3):
        for c in range(COLUMN - 3):
            window = [Board[r + i][c + i] for i in range(WINDOW)]
            Score += evaluate_board(window, piece)
    # Score negative slope
    for r in range(3, ROW):
        for c in range(COLUMN - 3):
            window = [Board[r - i][c + i] for i in range(WINDOW)]
            Score += evaluate_board(window, piece)

    return Score


def evaluate_window(window, piece):
    Score = 0
    opp_piece = PLAYER_Piece
    if piece == PLAYER_Piece:
        opp_piece = AI_Piece

    if window.count(piece) == 4:
        Score += 100
    elif window.count(piece) == 3 and window.count(EMPTY_Spot) == 1:
        Score += 20
    elif window.count(piece) == 2 and window.count(EMPTY_Spot) == 2:
        Score += 2
    if window.count(opp_piece) == 4:
        Score -= 100
    elif window.count(opp_piece) == 3 and window.count(EMPTY_Spot) == 1:
        Score -= 15
    elif window.count(opp_piece) == 2 and window.count(EMPTY_Spot) == 2:
        Score -= 1
    return Score


def score_position(Board, piece):
    Score = 0

    # Score center column
    center_array = [int(i) for i in list(Board[:, COLUMN // 2])]
    center_count = center_array.count(piece)
    Score += center_count * 2

    # Score Horizontal
    for r in range(ROW):
        row_array = [int(i) for i in list(Board[r, :])]
        for c in range(COLUMN - 3):
            if c == 0 or c == 3:
                bonus = 2
            else:
                bonus = 1
            window = row_array[c:c + WINDOW]
            Score += evaluate_window(window, piece) + (7 - r) + bonus

    # Score Vertical
    for c in range(COLUMN):
        col_array = [int(i) for i in list(Board[:, c])]
        for r in range(ROW - 3):
            if c == 0 or c == 3:
                bonus = 2
            else:
                bonus = 1
            window = col_array[r:r + WINDOW]
            Score += evaluate_window(window, piece) + (7 - r) + bonus

    # Score Positive sloped diagonal
    for r in range(ROW - 3):
        for c in range(COLUMN - 3):
            if c == 0 or c == 3:
                bonus = 2
            else:
                bonus = 1
            window = [Board[r + i][c + i] for i in range(WINDOW)]
            Score += evaluate_window(window, piece) + (7 - r) + bonus

    for r in range(3, ROW):
        for c in range(COLUMN - 3):
            if c == 0 or c == 3:
                bonus = 2
            else:
                bonus = 1
            window = [Board[r - i][c + i] for i in range(WINDOW)]
            Score += evaluate_window(window, piece) + (7 - r) + bonus

    return Score


def is_terminal_node(Board):
    # wining_move(Board, PLAYER_Piece) or wining_move(Board, AI_Piece) or
    return len(get_valid_locations(Board)) == 0


def minimax(Board, depth, maximizingPlayer, root, nodes):
    valid_locations = get_valid_locations(Board)
    is_terminal = is_terminal_node(Board)
    if fullboard(Board):
        root.score = score_board(Board, AI_Piece) - score_board(Board, PLAYER_Piece)
        return None, root.score, 1
    elif not depth:  # Depth is zero
        root.score = score_position(Board, AI_Piece)
        return None, root.score, 1
    Nonodes = 1
    if maximizingPlayer:
        value = -math.inf
        Column = random.choice(valid_locations)
        for col in valid_locations:
            childNode = Node(root, -sys.maxsize, not root.max_or_min)
            root.addChild(childNode)
            Row = next_row(Board, col)
            b_copy = Board.copy()
            drop_piece(b_copy, Row, col, AI_Piece)
            array = minimax(b_copy, depth - 1, False, childNode, Nonodes)
            new_score = array[1]
            Nonodes = Nonodes + array[2]
            if new_score > value:
                value = new_score
                Column = col
        root.score = value
        return Column, value, Nonodes

    else:  # Minimizing player
        value = math.inf
        Column = random.choice(valid_locations)
        for col in valid_locations:
            childNode = Node(root, -sys.maxsize, not root.max_or_min)
            root.addChild(childNode)
            Row = next_row(Board, col)
            b_copy = Board.copy()
            drop_piece(b_copy, Row, col, PLAYER_Piece)
            array = minimax(b_copy, depth - 1, True, childNode, Nonodes)
            new_score = array[1]
            Nonodes = Nonodes + array[2]
            if new_score < value:
                value = new_score
                Column = col
        root.score = value
        return Column, value, Nonodes
