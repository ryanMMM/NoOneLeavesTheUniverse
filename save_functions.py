import pickle
import sys
import time
from os import path

import winsound

from gamesave import GameSave
from output_formatting import clear_screen, str_input
from constant_objects import weapon_object_dictionary


def save_game(gamesave_object):

    save_path = 'saves/' + str(gamesave_object.get_player()) + '.pickle'
    absolute_save_path = path.abspath(save_path)

    # checks if player has already created a save
    if path.exists(absolute_save_path):

        pass
        # TODO add message to show user that save exists (thank you for playing again)

    else:

        pass
        # TODO add message to show user that it is their first time

    with open(save_path, 'wb') as save:

        pickle.dump(gamesave_object, save, protocol=pickle.HIGHEST_PROTOCOL)


def load_save(player_name):
    """loads gamesave object from pickle file"""

    save_path = 'saves/' + player_name + '.pickle'

    with open(save_path, 'rb') as save:

        loaded_save = pickle.load(save)

    return loaded_save


def title_screen():
    """starts the beginning title screen at the beginning of a game launch"""

    winsound.PlaySound("Soundtrack/title.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)
    # plays title music
    time.sleep(5)
    print("No One")
    time.sleep(0.5)
    print("Leaves")
    time.sleep(0.5)
    print("The UNIVERSE")
    time.sleep(4)
    clear_screen()

    while True:

        print("Menu:\n(N)ew game\n(L)oad game\n(Q)uit game")
        menu_choice = str_input()

        if menu_choice == 'n' or menu_choice == 'new':

            new_game()

        elif menu_choice == 'l' or menu_choice == 'load':

            load_game()

        elif menu_choice == 'q' or menu_choice == 'quit':

            save_quit()

        else:

            print("Invalid input")


def new_game():

    new_gamesave = GameSave()
    # creates a new game save with default attributes

    while True:

        clear_screen()
        print("Enter your name warrior")
        player_name = str_input()

        save_path = 'saves/' + player_name + '.pickle'
        absolute_save_path = path.abspath(save_path)

        # checks if a save already exists under the player name
        if path.exists(absolute_save_path):

            print("The name " + player_name + " is already taken on this device. Please try another name")

        else:

            time.sleep(0.25)
            print("Welcome to the UNIVERSE " + player_name)
            time.sleep(0.5)

            break

    while True:

        print("What difficulty would you like to play on?\n(E)asy\n(M)edium\n(H)ard")
        difficulty = str_input()

        # changes difficulty multiplier based on user input
        if difficulty == 'e' or difficulty == 'easy':

            difficulty_multiplier = 0.8

            break

        elif difficulty == 'm' or difficulty == 'medium':

            difficulty_multiplier = 1

            break

        elif difficulty == 'h' or difficulty == 'hard':

            difficulty_multiplier = 1.2

            break

        else:

            print("Invalid input")
            time.sleep(2)
            # prompts the user again

    new_gamesave.player.change_weapon(weapon_object_dictionary['starter_weapon'])
    # gives the player the starter weapon at the beginning of the game
    new_gamesave.set_up_difficulty_multiplier(difficulty_multiplier)
    # goes through the enemies in the enemy object dictionary and applies difficulty multiplier
    new_gamesave.player.change_name(player_name)
    # change's the player object's name to the chosen name
    new_gamesave.player.change_gamesave(new_gamesave)
    # gives the player reference to the current gamesave
    new_gamesave.player.spawn_at_village()
    # spawns the player at the village when initialized
    time.sleep(0.25)
    new_gamesave.tutorial()


def load_game():
    """checks if player exists already, if not, the player is initialized"""

    while True:

        clear_screen()
        print("Enter the name associated with your save")
        player_name = str_input()

        save_path = 'saves/' + player_name + '.pickle'
        absolute_save_path = path.abspath(save_path)

        # checks if player has already created a save
        if path.exists(absolute_save_path):

            print("Found " + player_name + "'s save. Would you like to load the save? (Y)es or (N)o")
            load_choice = str_input()

            if load_choice == 'y' or load_choice == 'yes':

                loaded_gamesave = load_save(player_name)
                start_loaded_game(loaded_gamesave)

                break

            elif load_choice != 'n' or load_choice != 'no':

                print("Invalid input")

        else:

            while True:

                print("No save was found under your name. Would you like to (E)nter another name, (S)tart a new game,"
                      " or (Q)uit game")
                no_save_choice = str_input()

                if no_save_choice == 'e' or no_save_choice == 'enter':

                    break

                elif no_save_choice == 's' or no_save_choice == 'start':

                    new_game()

                elif no_save_choice == 'q' or no_save_choice == 'quit':

                    save_quit()

                else:

                    print("Invalid input")


def start_loaded_game(gamesave):

    gamesave.player.spawn_at_village()
    gamesave.gates_of_village()


def save_quit(gamesave=False):

    if gamesave:

        save_game(gamesave)

    sys.exit(0)
