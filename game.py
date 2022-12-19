import itertools
from array import *
import numpy as np
import time
import sys, pygame as pg
import Differential

# This Program is a simulation for Sudoko Game

##############################################################################################################
##############################################################################################################
####################                      PART 1 : Game Setup                          #######################
##############################################################################################################
##############################################################################################################

# Checking Row
def row_check(Grid, row, n):
    return next((0 for i in range(9) if Grid[row][i] == n), 1)


#####################################################################################################

# Checking Column
def column_check(Grid, col, n):
    return next((0 for i in range(9) if Grid[i][col] == n), 1)


#####################################################################################################

# Check Block
def block_check(Grid, row, col, n):
    return next(
        (
            0
            for i, j in itertools.product(range(3), range(3))
            if Grid[i + (row // 3) * 3][j + (col // 3) * 3] == n
        ),
        1,
    )


#####################################################################################################

# Check index with value 0
def check_index(Grid, arr):
    for i, j in itertools.product(range(9), range(9)):
        if Grid[i][j] == 0:
            arr[0] = i
            arr[1] = j
            return True
    return False


#####################################################################################################

# Check Possible:
def possible(x, y, n):
    for i in range(9):
        if Grid[i][x] == n:
            return False
    for i in range(9):
        if Grid[y][i] == n:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    return all(
        Grid[Y][X] != n
        for X, Y in itertools.product(range(x0, x0 + 3), range(y0, y0 + 3))
    )


#####################################################################################################

# Create Grid
def create_grid():
    h = 9
    w = 9
    global Grid
    Grid = [[0 for _ in range(w)] for _ in range(h)]


#####################################################################################################

# Solving Grid
def solve_sudoko(counter):
    global Grid
    arr = [0, 0]
    if not check_index(Grid, arr):
        return True
    row = arr[0]
    col = arr[1]

    for i in range(1, 10):
        if (
            row_check(Grid, row, i)
            and column_check(Grid, col, i)
            and block_check(Grid, row, col, i)
        ):
            if counter == 0:
                pg.display.update()
                counter += 1
                time.sleep(3)
            Grid[row][col] = i
            time.sleep(0.06)
            pg.draw.rect(
                screen, pg.Color("white"), ((col * 65) + 50, (row * 56) + 25, 31, 37)
            )
            n_text = font.render(str(i), True, pg.Color("green"))
            screen.blit(n_text, pg.Vector2((col * 65) + 50, (row * 56) + 25))
            pg.display.update()
            if solve_sudoko(counter):
                return True
            Grid[row][col] = 0
            pg.draw.rect(
                screen, pg.Color("white"), ((col * 65) + 50, (row * 56) + 25, 31, 37)
            )
            n_text = font.render(str(i), True, pg.Color("red"))
            screen.blit(n_text, pg.Vector2((col * 65) + 50, (row * 56) + 25))
            pg.display.update()
            time.sleep(1)
    return False


#####################################################################################################

# Set Random values for Random Places in the Grid :
def random_sudoko(Grid):
    arr = [0, 0]
    if not check_index(Grid, arr):
        return True
    row = arr[0]
    column = arr[1]

    for _ in range(9):
        x = np.random.randint(1, 10)
        if (
            row_check(Grid, row, x)
            and column_check(Grid, column, x)
            and block_check(Grid, row, column, x)
        ):
            Grid[row][column] = x
            if random_sudoko(Grid):
                return True
            Grid[row][column] = 0
    return False


#####################################################################################################

# Free some Cells from Random Grid


def empty_cells(Grid, n):
    for _ in range(n):
        rows = np.random.randint(9)
        cols = np.random.randint(9)
        while Grid[rows][cols] == 0:
            rows = np.random.randint(9)
            cols = np.random.randint(9)
        Grid[rows][cols] = 0


#####################################################################################################

# Prepare Grid for Sudoko Game before starting the Game


def initialize(Difficulty_mode):
    for i, j in itertools.product(range(9), range(9)):
        Matrix[i][j] = False
    create_grid()
    random_sudoko(Grid)
    # Modes for Difficulty
    # [ Easy , Medium , Hard ]

    global number_of_free_cells
    if Difficulty_mode == Easy:
        number_of_free_cells = np.random.randint(17, 25)
    elif Difficulty_mode == Medium:
        number_of_free_cells = np.random.randint(25, 36)
    elif Difficulty_mode == Hard:
        number_of_free_cells = np.random.randint(36, 47)
    else:
        number_of_free_cells = np.random.randint(10, 47)
    empty_cells(Grid, number_of_free_cells)
    return Grid


#####################################################################################################

##############################################################################################################
##############################################################################################################
####################                    PART 2 : Game Display                          #######################
##############################################################################################################
##############################################################################################################

# Initialize screen with size
pg.init()
screen_size = 650, 650
screen = pg.display.set_mode(screen_size)
font = pg.font.SysFont(None, 65)


#####################################################################################################

# Show Background
def draw_background():
    SCREEN = pg.display.set_mode((650, 650))
    BG = pg.image.load("assets/sudoku.jpg")
    SCREEN.blit(BG, (0, 0))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(15, 15, 610, 520), 10)
    i = 1
    while i < 620 / 69:
        # The Width of Line
        line_width = 5 if i % 3 > 0 else 10
        # Draw Grid Lines
        pg.draw.line(
            screen,
            pg.Color("black"),
            pg.Vector2((i * 68) + 15, 15),
            pg.Vector2(((i * 68) + 15), 530),
            line_width,
        )
        pg.draw.line(
            screen,
            pg.Color("black"),
            pg.Vector2(15, (i * 56) + 15),
            pg.Vector2(623, ((i * 56) + 15)),
            line_width,
        )
        i += 1


#####################################################################################################


# Show Grid Using GUI

# Boolean Grid to check the places of empty cells #
w, h = 9, 9
Matrix = [[False for _ in range(w)] for _ in range(h)]


def draw_numbers():
    offset1 = 50
    offset2 = 25
    flag = False
    for row in range(9):
        col = 0
        while col < 9:
            output = Grid[row][col]
            if output == 0:
                Matrix[row][col] = True
                col += 1
                continue
            n_text = 0
            if not Matrix[row][col]:
                n_text = font.render(str(output), True, pg.Color("black"))
            else:
                flag = True
                n_text = font.render(str(output), True, pg.Color("green"))
            screen.blit(n_text, pg.Vector2((col * 65) + offset1, (row * 56) + offset2))
            col += 1

    # if flag:
    #     draw_background()
    #     x = 0
    #     y = 255
    #     z = 0
    #     row = 0
    #     while row < 9:
    #         col = 0
    #         while col < 9:
    #             x = (x + 0) % 256
    #             y = (y - 15 + 256) % 256
    #             z = (z + 0) % 256
    #             for i in range(row, row + 3):
    #                 for j in range(col, col + 3):
    #                     if not Matrix[i][j]:
    #                         n_text = font.render(str(Grid[i][j]), True, pg.Color("black"))
    #                     else:
    #                         n_text = font.render(str(Grid[i][j]), True, pg.Color((x, y, z)))
    #                     screen.blit(n_text, pg.Vector2((i * 65) + offset1, (j * 56) + offset2))
    #             col += 3
    #         row += 3


#####################################################################################################

# Printing Solution of Sudoko Game
def draw_solution():
    counter = 0
    solve_sudoko(counter)


# print(np.matrix(Grid))
#####################################################################################################

# initialize game with certain difficulty mode

########################################################
###########   OPTIONS For Difficulty mode    ###########
#######   0- Easy     1- Medium       2- Hard    #######
########################################################
global Easy, Medium, Hard
Easy = 0
Medium = 1
Hard = 2
difficulty_mode = Easy


#####################################################################################################
# Starting Game


def game_loop():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
    draw_background()
    draw_numbers()
    draw_solution()
    # display.flip() -> used to update screen
    pg.display.flip()


# for i in range(2):
#     game_loop()
#     if i == 1:
#         exit_window = False
#         while not exit_window:
#             for event in pg.event.get():
#                 if event.type == pg.QUIT:
#                     exit_window = True
#         pg.quit()

#####################################################################################################

# Change Game Difficulty Mode
def change_game_difficulty_mode(difficulty):
    global difficulty_mode
    difficulty_mode = difficulty


#####################################################################################################

# Get Game Difficulty Mode
def get_game_difficulty_mode():
    global difficulty_mode
    return difficulty_mode


#####################################################################################################

global Backtracking, Differential
Backtracking = 0
Differential = 1
method_mode = Backtracking

#####################################################################################################

# Change Game Method Mode
def change_game_method_mode(method):
    global method_mode
    method_mode = method


#####################################################################################################

# Get Game Method Mode
def get_game_method_mode():
    global method_mode
    return method_mode


#####################################################################################################

# Make User able to enter Numbers in the GUI


# Checking that the values entered by User is valid


# Show the Solution of Grid using GUI
