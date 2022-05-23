from time import time

import pygame_menu
from FAI import *
from NAI import *
from board import *
from win import *
from Constants import *
import pygame
from Node import *
import sys
import math

width = COLUMN * SQUARESIZE  # 700 pixel
height = (ROW + 1) * SQUARESIZE  # 700 pixel
size = (width, height)
k = 3
prune = True


def gui_board():  # for building frame black circles with blue rectangle
    for c in range(COLUMN):
        for r in range(ROW):
            pygame.draw.rect(display, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            # rect(surface, color, Rect, width=0)
            pygame.draw.circle(display, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            # circle(surface, color, pos, radius, width =0)      +SquareSize/2 --> half rectangle(offset)
    pygame.display.update()


def chips_board(Board):  # for building chips red circles and orange circles
    for c in range(COLUMN):
        for r in range(ROW):
            if Board[r][c] == PLAYER_Piece:
                pygame.draw.circle(display, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                # NO + square size  as we fill from the first bottom circle

            elif Board[r][c] == AI_Piece:
                pygame.draw.circle(display, ORANGE, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            # circle(surface, color, pos, radius, width =0)+SquareSize/2 --> half rectangle

    pygame.display.update()


def menu():  # function to display the main menu
    global SCREEN, menu
    pygame.init()

    SCREEN = pygame.display.set_mode(size)
    menu = pygame_menu.Menu('CONNECT FOUR', width, height,
                            theme=pygame_menu.themes.THEME_DARK)
    menu.add.text_input('Depth K :', default=k, onchange=setK)
    menu.add.selector('', [('Minimax with alpha-beta pruning', 1), ('Minimax without alpha-beta pruning', 2)],
                      onchange=setPruning)
    menu.add.button('Play Normal Game', NormalGame)
    menu.add.button('Play Full Board', FullBoardGame)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(SCREEN)


def setPruning(a, b):
    global prune
    prune = not prune


def setK(kInput):
    global k
    k = kInput


def NormalGame():
    global turn, display, height, width, size, k, prune
    board = create_board()
    print_board(board)
    GameOver = False
    pygame.init()

    width = COLUMN * SQUARESIZE  # 700 pixel
    height = (ROW + 1) * SQUARESIZE  # 700 pixel
    size = (width, height)
    display = pygame.display.set_mode(size)
    gui_board()
    chips_board(board)
    pygame.display.update()
    Font = pygame.font.SysFont('Verdana', 70)
    root = Node(None, -sys.maxsize, True)
    while not GameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(display, BLACK, (0, 0, width, SQUARESIZE))
                x_pos = event.pos[0]
                # print(x_pos)
                if turn == PLAYER:
                    pygame.draw.circle(display, RED, (x_pos, SQUARESIZE / 2), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(display, BLACK, (0, 0, width, SQUARESIZE))
                # turn 1
                if turn == PLAYER:
                    x_pos = event.pos[0]  # takes x position of mouse click range (0->700)
                    # print(x_pos)
                    column = (x_pos // SQUARESIZE)
                    # print(column)
                    if valid_location(board, column):
                        row = next_row(board, column)
                        drop_piece(board, row, column, PLAYER_Piece)
                        print_board(board)
                        if wining_move(board, PLAYER_Piece):
                            print("PLAYER 1 WIN")
                            text = Font.render("RED WINS", True, RED)
                            display.blit(text, (160, 10))
                            GameOver = True
                        turn = AI

                    chips_board(board)

        if turn == AI and not GameOver:

            if prune:
                nodes = 0
                start = time()
                column, score, nodes = nMinMaxPrune(board, int(k), -math.inf, math.inf, True, root, nodes)
                end = time()
                print("Prune Expanded Nodes")
                print(nodes)
                print("Total Time:")
                print(end - start)
            else:
                nodes = 0
                start = time()
                column, score, nodes = nMiniMax(board, int(k), True, root, nodes)
                end = time()
                print("No-Prune Expanded Nodes")
                print(nodes)
                print("Total Time:")
                print(end - start)
            # root.printTree(3)
            if valid_location(board, column):
                pygame.time.wait(1000)
                row = next_row(board, column)
                drop_piece(board, row, column, AI_Piece)
                print_board(board)
                if wining_move(board, AI_Piece):
                    print("AI WINS")
                    text = Font.render("AI WINS", True, ORANGE)
                    display.blit(text, (160, 10))
                    GameOver = True
                turn = PLAYER

        chips_board(board)

        if GameOver:
            pygame.time.wait(5000)
            pygame.quit()
            sys.exit()


def FullBoardGame():
    global turn, display, height, width, size, k, prune
    board = create_board()
    print_board(board)
    GameOver = False
    pygame.init()

    width = COLUMN * SQUARESIZE  # 700 pixel
    height = (ROW + 1) * SQUARESIZE  # 700 pixel
    size = (width, height)
    display = pygame.display.set_mode(size)
    gui_board()
    chips_board(board)
    pygame.display.update()
    Font = pygame.font.SysFont('Verdana', 70)
    while not GameOver:
        root = Node(None, -sys.maxsize, True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(display, BLACK, (0, 0, width, SQUARESIZE))
                x_pos = event.pos[0]
                # print(x_pos)
                if turn == PLAYER:
                    pygame.draw.circle(display, RED, (x_pos, SQUARESIZE / 2), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(display, BLACK, (0, 0, width, SQUARESIZE))
                # turn 1
                if turn == PLAYER:
                    x_pos = event.pos[0]  # takes x position of mouse click range (0->700)
                    # print(x_pos)
                    column = (x_pos // SQUARESIZE)
                    # print(column)
                    if valid_location(board, column):
                        row = next_row(board, column)
                        drop_piece(board, row, column, PLAYER_Piece)
                        print_board(board)
                        # if wining_move(board, PLAYER_Piece):
                        #     print("PLAYER 1 WIN")
                        #     text = Font.render("RED WINS", True, RED)
                        #     display.blit(text, (160, 10))
                        #     # GameOver = True
                        turn = AI
                    chips_board(board)
            endgame(GameOver)

        if fullboard(board):
            GameOver = True
            print("Board Full")
            AI_Score = score_board(board, AI_Piece)
            User_Score = score_board(board, PLAYER_Piece)
            print(AI_Score)
            print(User_Score)
            if AI_Score > User_Score:
                print("AI WINS")
                text = Font.render("AI WINS", True, ORANGE)
                display.blit(text, (160, 10))
                chips_board(board)
            else:
                print("PLAYER 1 WIN")
                text = Font.render("User WINS", True, RED)
                display.blit(text, (160, 10))
                chips_board(board)

        if turn == AI and not GameOver:

            if prune:
                nodes = 0
                start = time()
                column, score, nodes = OPminimax(board, int(k), -math.inf, math.inf, True, root, nodes)
                end = time()
                print("Prune Expanded Nodes")
                print(nodes)
                print("Total Time:")
                print(end - start)
            else:
                nodes = 0
                start = time()
                column, score, nodes = minimax(board, int(k), True, root, nodes)
                end = time()
                print("No-Prune Expanded Nodes")
                print(nodes)
                print("Total Time:")
                print(end - start)
            root.printTree(3)
            if valid_location(board, column):
                pygame.time.wait(1000)
                row = next_row(board, column)
                drop_piece(board, row, column, AI_Piece)
                print_board(board)
                # if wining_move(board, AI_Piece):
                #     print("AI WINS")
                #     text = Font.render("AI WINS", True, ORANGE)
                #     display.blit(text, (160, 10))
                #     GameOver = True
                turn = PLAYER
            chips_board(board)
        endgame(GameOver)
        if fullboard(board):
            GameOver = True
            print("Board Full")
            AI_Score = score_board(board, AI_Piece)
            User_Score = score_board(board, PLAYER_Piece)
            print(AI_Score)
            print(User_Score)
            if AI_Score > User_Score:
                print("AI WINS")
                text = Font.render("AI WINS", True, ORANGE)
                display.blit(text, (160, 10))
                chips_board(board)
            else:
                print("PLAYER 1 WIN")
                text = Font.render("User WINS", True, RED)
                display.blit(text, (160, 10))
                chips_board(board)
            endgame(GameOver)


def endgame(GameOver):
    if GameOver:
        pygame.time.wait(5000)
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    menu()
