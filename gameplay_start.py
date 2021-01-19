import time

from pygame import mixer

from output_formatting import colour_print
from gamesave import GameSave
from save_functions import *


def start_game():

    new_gamesave = GameSave()
    title_screen(new_gamesave)


def title_screen(gamesave):
    # TODO mention that you added a parameter to remove circular dependencies
    """starts the beginning title screen at the beginning of a game launch"""

    clear_screen()

    mixer.init()
    mixer.music.load('soundtrack/title_screen_music.mp3')
    mixer.music.play(-1)
    # loops the title music
    time.sleep(5)
    colour_print("No One")
    time.sleep(0.5)
    colour_print("Leaves")
    time.sleep(0.5)
    colour_print("The UNIVERSE")
    time.sleep(4)
    clear_screen()

    while True:

        colour_print("Menu:\n(N)ew game\n(L)oad game\n(Q)uit game")
        menu_choice = str_input()

        if menu_choice == 'n' or menu_choice == 'new':

            new_game(gamesave)

        elif menu_choice == 'l' or menu_choice == 'load':

            load_game(gamesave)

        elif menu_choice == 'q' or menu_choice == 'quit':

            save_quit()

        else:

            colour_print("Invalid input", "red")
