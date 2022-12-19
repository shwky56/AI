import numpy as np
import pygame, sys
import time
from button import Button
import game
import Differential

pygame.init()

SCREEN = pygame.display.set_mode((650, 650))
pygame.display.set_caption("Sudoku")

BG = pygame.image.load("assets/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def play():
    SCREEN.fill("black")
    if game.get_game_method_mode() == 0:
        start = time.time()
        game.initialize(game.difficulty_mode)
        for _ in range(2):
            game.game_loop()
    else:
        start = time.time()
        temp = np.zeros((9, 9))
        temp = game.initialize(game.difficulty_mode)
        Differential.initialize_puzzle(temp)
        Differential.start()
    end = time.time()
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # print Time Label
        TIME_TEXT = get_font(35).render("TIME:", True, "black")
        TIME_RECT = TIME_TEXT.get_rect(center=(100, 600))
        SCREEN.blit(TIME_TEXT, TIME_RECT)
        TIME2_TEXT = get_font(35).render(f"{int(end - start)}ms", True, "black")
        TIME2_RECT = TIME2_TEXT.get_rect(center=(240, 600))
        SCREEN.blit(TIME2_TEXT, TIME2_RECT)

        PLAY_BACK = Button(
            image=None,
            pos=(520, 600),
            text_input="BACK",
            font=get_font(45),
            base_color="black",
            hovering_color="Green",
        )

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and PLAY_BACK.checkForInput(
                PLAY_MOUSE_POS
            ):
                main_menu()

        pygame.display.update()


def options():
    while True:
        BG = pygame.image.load("assets/sudoku.jpg")
        SCREEN.blit(BG, (0, 0))

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        OPTIONS_TEXT = get_font(75).render("OPTIONS", True, "red")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(340, 120))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # Write Select Word
        SELECT_TEXT = get_font(35).render("SELECT", True, "black")
        SELECT_RECT = OPTIONS_TEXT.get_rect(center=(490, 240))
        SCREEN.blit(SELECT_TEXT, SELECT_RECT)

        # Write Difficulty Word
        DIFFICULTY_TEXT = get_font(20).render("DIFFICULTY:", True, "black")
        DIFFICULTY_RECT = OPTIONS_TEXT.get_rect(center=(280, 320))
        SCREEN.blit(DIFFICULTY_TEXT, DIFFICULTY_RECT)

        # Show Decrease Difficulty Button
        image = pygame.image.load("assets/left_arrow.png")
        newimage = pygame.transform.scale(image, (40, 40))
        DECREASE_DIFFICULTY = Button(
            image=newimage,
            pos=(140, 360),
            text_input="",
            font=get_font(65),
            base_color="black",
            hovering_color="Green",
        )
        DECREASE_DIFFICULTY.update(SCREEN)

        # Show Increase Difficulty Button
        image2 = pygame.image.load("assets/left_arrow.png")
        rot = pygame.transform.rotate(image2, 180)
        newimage2 = pygame.transform.scale(rot, (40, 40))
        INCREASE_DIFFICULTY = Button(
            image=newimage2,
            pos=(537, 360),
            text_input="",
            font=get_font(65),
            base_color="black",
            hovering_color="Green",
        )
        INCREASE_DIFFICULTY.update(SCREEN)

        # Show Difficulty Button
        image3 = pygame.image.load("assets/Play Rect.png")
        newimage3 = pygame.transform.scale(image3, (300, 60))
        DIFFICULTY_BUTTON = 0
        if game.get_game_difficulty_mode() == 0:
            DIFFICULTY_BUTTON = Button(
                image=newimage3,
                pos=(340, 360),
                text_input="EASY",
                font=get_font(40),
                base_color="lightgreen",
                hovering_color="green",
            )
        elif game.get_game_difficulty_mode() == 1:
            DIFFICULTY_BUTTON = Button(
                image=newimage3,
                pos=(340, 360),
                text_input="Medium",
                font=get_font(40),
                base_color="orange",
                hovering_color="darkorange",
            )
        else:
            DIFFICULTY_BUTTON = Button(
                image=newimage3,
                pos=(340, 360),
                text_input="Hard",
                font=get_font(40),
                base_color="red",
                hovering_color="darkred",
            )
        DIFFICULTY_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        DIFFICULTY_BUTTON.update(SCREEN)

        # Write Method Word
        SELECT_TEXT = get_font(20).render("Method:", True, "black")
        SELECT_RECT = OPTIONS_TEXT.get_rect(center=(280, 460))
        SCREEN.blit(SELECT_TEXT, SELECT_RECT)

        # Show Decrease Method Button
        image = pygame.image.load("assets/left_arrow.png")
        newimage = pygame.transform.scale(image, (40, 40))
        DECREASE_METHOD = Button(
            image=newimage,
            pos=(140, 500),
            text_input="",
            font=get_font(65),
            base_color="black",
            hovering_color="Green",
        )
        DECREASE_METHOD.update(SCREEN)

        # Show Increase Method Button
        image2 = pygame.image.load("assets/left_arrow.png")
        rot = pygame.transform.rotate(image2, 180)
        newimage2 = pygame.transform.scale(rot, (40, 40))
        INCREASE_METHOD = Button(
            image=newimage2,
            pos=(537, 500),
            text_input="",
            font=get_font(65),
            base_color="black",
            hovering_color="Green",
        )
        INCREASE_METHOD.update(SCREEN)

        # Show Method Button
        image3 = pygame.image.load("assets/Play Rect.png")
        newimage3 = pygame.transform.scale(image3, (300, 60))
        METHOD_BUTTON = 0
        if game.get_game_method_mode() == 0:
            METHOD_BUTTON = Button(
                image=newimage3,
                pos=(340, 500),
                text_input="BACKTRACKING",
                font=get_font(25),
                base_color=(0, 255, 255),
                hovering_color="lightblue",
            )
        else:
            METHOD_BUTTON = Button(
                image=newimage3,
                pos=(340, 500),
                text_input="DIFFERENTIAL",
                font=get_font(25),
                base_color=(0, 136, 202),
                hovering_color=(55, 190, 255),
            )
        METHOD_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        METHOD_BUTTON.update(SCREEN)

        OPTIONS_BACK = Button(
            image=None,
            pos=(340, 600),
            text_input="BACK",
            font=get_font(45),
            base_color="Black",
            hovering_color="Green",
        )

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # click on Back
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                # change in Difficulty mode
                if INCREASE_DIFFICULTY.checkForInput(OPTIONS_MOUSE_POS):
                    x = (game.get_game_difficulty_mode() + 1) % 3
                    game.change_game_difficulty_mode(x)
                    break
                if DECREASE_DIFFICULTY.checkForInput(OPTIONS_MOUSE_POS):
                    x = (game.get_game_difficulty_mode() - 1 + 3) % 3
                    game.change_game_difficulty_mode(x)
                    break
                # change in method mode
                if INCREASE_METHOD.checkForInput(OPTIONS_MOUSE_POS):
                    x = (game.get_game_method_mode() + 1) % 2
                    game.change_game_method_mode(x)
                    game.change_game_difficulty_mode(0)
                    break
                if DECREASE_METHOD.checkForInput(OPTIONS_MOUSE_POS):
                    x = (game.get_game_method_mode() - 1 + 2) % 2
                    game.change_game_method_mode(x)
                    game.change_game_difficulty_mode(0)
                    break

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("Sudoku", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(340, 100))

        PLAY_BUTTON = Button(
            image=pygame.image.load("assets/Play Rect.png"),
            pos=(340, 250),
            text_input="PLAY",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="red",
        )
        OPTIONS_BUTTON = Button(
            image=pygame.image.load("assets/Options Rect.png"),
            pos=(340, 400),
            text_input="OPTIONS",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="green",
        )
        QUIT_BUTTON = Button(
            image=pygame.image.load("assets/Quit Rect.png"),
            pos=(340, 550),
            text_input="QUIT",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="black",
        )

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
