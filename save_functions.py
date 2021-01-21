import pickle
import sys
import time
from os import path

from output_formatting import clear_screen, str_input, colour_print, loading_bar
from constant_objects import weapon_object_dictionary


def save_game(gamesave_object):

    save_path = 'saves/' + str(gamesave_object.get_player()) + '.pickle'
    absolute_save_path = path.abspath(save_path)

    # checks if player has already created a save
    if path.exists(absolute_save_path):

        colour_print("Saving data in " + str(gamesave_object.get_player()) + "'s save")

    else:

        colour_print("Creating a new save")

    loading_bar("Saving...")

    with open(save_path, 'wb') as save:

        pickle.dump(gamesave_object, save, protocol=pickle.HIGHEST_PROTOCOL)


def load_save(player_name):
    """loads gamesave object from pickle file"""

    save_path = 'saves/' + player_name + '.pickle'

    with open(save_path, 'rb') as save:

        loaded_save = pickle.load(save)

    return loaded_save


def new_game(gamesave):
    """starts a new gamesave object, taking in user inputs then generating a player object with the desired
    attributes"""

    new_gamesave = gamesave
    # creates a new game save with default attributes

    while True:

        colour_print("Enter your name warrior")
        player_name = str_input()

        save_path = 'saves/' + player_name + '.pickle'
        absolute_save_path = path.abspath(save_path)

        # checks if a save already exists under the player name
        if path.exists(absolute_save_path):

            colour_print("The name " + player_name + " is already taken on this device. Please try another name")

        else:

            time.sleep(0.25)
            colour_print("Welcome to the UNIVERSE, " + player_name.capitalize())
            time.sleep(0.5)

            break

    while True:

        colour_print("What difficulty would you like to play on?\n(E)asy\n(M)edium\n(H)ard\n(Q) to Quit Game")
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

        elif difficulty == 'q' or difficulty == 'quit':

            save_quit()

        else:

            colour_print("Invalid input", "red")
            time.sleep(2)
            # prompts the user again

    new_gamesave.player.change_weapon(weapon_object_dictionary['starter_weapon'])
    # gives the player the starter weapon at the beginning of the game
    new_gamesave.change_difficulty_multiplier(difficulty_multiplier)
    # goes through the enemies in the enemy object dictionary and applies difficulty multiplier
    new_gamesave.player.change_name(player_name)
    # change's the player object's name to the chosen name
    new_gamesave.player.change_gamesave(new_gamesave)
    # gives the player reference to the current gamesave
    new_gamesave.player.spawn_at_village()
    # spawns the player at the village when initialized
    time.sleep(0.25)
    new_gamesave.tutorial()
    # starts the tutorial at the beginning of a new game


def load_game(gamesave):
    """checks if player exists already, if not, the player is initialized"""

    while True:

        clear_screen()
        colour_print("Enter the name associated with your save")
        player_name = str_input()

        save_path = 'saves/' + player_name + '.pickle'
        absolute_save_path = path.abspath(save_path)

        # checks if player has already created a save
        if path.exists(absolute_save_path):

            colour_print("Found " + player_name + "'s save. Would you like to load the save? (Y)es or (N)o"
                                                  "\n\n(Q) to Quit Game")
            load_choice = str_input()

            if load_choice == 'y' or load_choice == 'yes':

                loaded_gamesave = load_save(player_name)
                start_loaded_game(loaded_gamesave)

                break

            elif load_choice == 'q' or load_choice == 'quit':

                save_quit()

            elif load_choice == 'n' or load_choice == 'no':

                break
                # returns player to menu screen

            else:

                colour_print("Invalid input", "red")

        else:

            while True:

                colour_print("No save was found under your name. "
                             "Would you like to (E)nter another name, (S)tart a new game,"
                             " or (Q)uit game")
                no_save_choice = str_input()

                if no_save_choice == 'e' or no_save_choice == 'enter':

                    break

                elif no_save_choice == 's' or no_save_choice == 'start':

                    new_game(gamesave)

                elif no_save_choice == 'q' or no_save_choice == 'quit':

                    save_quit()

                else:

                    colour_print("Invalid input", "red")


def start_loaded_game(gamesave):
    """starts the gameplay"""

    gamesave.player.spawn_at_village()
    gamesave.gates_of_village()
    # starts the gates of village gameplay loop, which is where the player can choose to enter wilderness or the village


def save_quit(gamesave=False):
    """saves the gamesave data and quits the game"""

    # checks if a gamesave is passed to the function, if so, then the gamesave is saved to a file
    if gamesave:

        save_game(gamesave)

    sys.exit(0)
