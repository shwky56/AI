import itertools
import numpy as np
import random as rndm
import time
import math
import sys, pygame as pg
import game

flag = False
answer = None

puzzle = [[0 for _ in range(9)] for _ in range(9)]


def initialize_puzzle(grid):
    global puzzle
    puzzle = grid
    print(np.matrix(puzzle))


def printBoard(board):
    print("=============================")
    for row in range(len(board)):
        for column in range(len(board[row])):
            print(board[row][column], end=" ")
        print("")
    print("=============================")


def copyBoard(copyFrom):
    return [copyFrom[row].copy() for row in range(len(copyFrom))]


def make_population(startedBoard, length):
    pop = []
    for _ in range(length):
        person = copyBoard(startedBoard)
        for row, column in itertools.product(range(9), range(9)):
            if person[row][column] == 0:
                person[row][column] = int(rndm.uniform(1, 9))
        pop.append(person)
    return pop


# check row
def row_fitness(chromo):
    fit = 0
    for row in range(9):
        sett = {chromo[row][col] for col in range(9)}
        fit += 9 - len(sett)
    return fit


# check column
def col_fitness(chromo):
    fit = 0
    for col in range(9):
        sett = {chromo[row][col] for row in range(9)}
        fit += 9 - len(sett)
    return fit


# check 3X3 grid
def fitness9x9(board):
    return sum(
        fitness3X3Cells(board, row, column)
        for row, column in itertools.product(range(0, 9, 3), range(0, 9, 3))
    )


def fitness3X3Cells(board, rowIndex, columnIndex):
    startRow = 3 * math.floor(rowIndex / 3)
    startColumn = 3 * math.floor(columnIndex / 3)
    setNumbers = {
        board[i][j]
        for i, j in itertools.product(
            range(startRow, startRow + 3), range(startColumn, startColumn + 3)
        )
    }
    return 9 - len(setNumbers)


# get the sum of fitnees
def fit_sum(chromosome):
    return row_fitness(chromosome) + col_fitness(chromosome) + fitness9x9(chromosome)


def clp(value):
    value = int(value)
    return 1 if value < 1 else min(value, 9)


def mutation(parent, chromosome, mutation_factor=0.3):
    parent_size = len(parent)
    random_vectors = []  # a,b,c vectors
    x1 = x2 = x3 = None
    while x1 == x2 or x1 == x3 or x2 == x3:
        x1 = parent[rndm.randint(0, parent_size - 1)]  # 0
        x2 = parent[rndm.randint(0, parent_size - 1)]  # 1
        x3 = parent[rndm.randint(0, parent_size - 1)]  # 2
    donor_vector = copyBoard(puzzle)
    # making donor vector mutated vector idex by idex
    for row, col in itertools.product(range(9), range(9)):
        if donor_vector[row][col] == 0:
            donor_vector[row][col] = clp(
                x3[row][col] + (mutation_factor * (x1[row][col] - x2[row][col]))
            )
    return donor_vector


def recombination(donor_vector, parent, chromosome_index, cross_probability=0.4):
    trail_vector = copyBoard(
        puzzle
    )  # make my trail vector from the parent and donor vector
    for row, col in itertools.product(range(9), range(9)):
        if puzzle[row][col] == 0:
            trail_vector[row][col] = (
                donor_vector[row][col]
                if cross_probability >= rndm.random()
                else parent[chromosome_index][row][col]
            )
    return trail_vector


def selection(trail_vector, parent, chromosome_index):
    global flag
    flag = False
    global answer
    mutant_vector_fitness = fit_sum(trail_vector)
    target_vector_fitness = fit_sum(parent[chromosome_index])
    if target_vector_fitness > mutant_vector_fitness:
        parent[chromosome_index] = trail_vector
    if fit_sum(parent[chromosome_index]) == 0:
        # graded = [(fit_sum(member), member) for member in parent]
        # parent = [x[1] for x in sorted(graded)]
        answer = parent[chromosome_index]
        flag = True
    return parent


def grade(pop):
    total = [fit_sum(member) for member in pop]
    return sum(total) / len(pop) * 1.0


def start():
    pg.init()
    screen_size = 650, 650
    screen = pg.display.set_mode(screen_size)
    font = pg.font.SysFont(None, 65)
    population_size = 200
    population = make_population(puzzle.copy(), population_size)
    evo = 1
    fits = 100000
    fitnessHistory = [(evo, grade(population))]
    answer_index = 0
    for i in range(fits):
        for pop in range(len(population)):
            donor_vector = mutation(population, population[pop])
            trail_vector = recombination(donor_vector, population, pop)
            population = selection(trail_vector, population, pop)
            if flag:
                answer_index = pop
                break
        if flag:
            print("gen num: ", i, " ", fit_sum(population[0]), "flag : ", flag)
            game.draw_background()
            game.draw_numbers()
            for row, col in itertools.product(range(9), range(9)):
                pg.draw.rect(
                    screen,
                    pg.Color("white"),
                    ((col * 65) + 50, (row * 56) + 25, 31, 37),
                )
                n_text = (
                    font.render(str(answer[row][col]), True, pg.Color("green"))
                    if game.Matrix[row][col]
                    else font.render(str(answer[row][col]), True, pg.Color("black"))
                )
                screen.blit(n_text, pg.Vector2((col * 65) + 50, (row * 56) + 25))
                pg.display.update()
            break
        # print grid
        if i % 100 == 0:
            print("gen num: ", i, " ", fit_sum(population[0]), "flag : ", flag)
            game.draw_background()
            game.draw_numbers()
            for row, col in itertools.product(range(9), range(9)):
                pg.draw.rect(
                    screen,
                    pg.Color("white"),
                    ((col * 65) + 50, (row * 56) + 25, 31, 37),
                )
                n_text = (
                    font.render(str(population[0][row][col]), True, pg.Color("red"))
                    if game.Matrix[row][col]
                    else font.render(
                        str(population[0][row][col]), True, pg.Color("black")
                    )
                )
                screen.blit(n_text, pg.Vector2((col * 65) + 50, (row * 56) + 25))
                pg.display.update()

        # if i % 100 == 0 or flag:
        #     pass


# printBoard(answer)

# import matplotlib.pyplot as plt
#
# listX = [x[0] for x in fitnessHistory]
# listY = [x[1] for x in fitnessHistory]
# plt.plot(listY, listX)
# plt.title("Differential Evolution For Sudoku")
# plt.ylabel("Number of generations")
# plt.xlabel("Fitness")
# plt.show()
