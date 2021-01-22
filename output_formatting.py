import os
import sys
import time

from pygame import mixer
from rich.progress import track
from rich.console import Console


def colour_print(string, font_colour="blue", background_colour="white",
                 allignment="center"):

    console = Console()
    style = "bold " + font_colour + " on " + background_colour
    console.print(string, justify=allignment, style=style)


def loading_bar(string, font_colour="green", background_colour="black"):

    style = "bold " + font_colour + " on " + background_colour

    for percentage in track(range(100), description=string, style=style):
        time.sleep(0.025)


def invalid_input():

    colour_print("Invalid input!", "red")
    time.sleep(0.3)


def clear_screen():
    """clears the command line screen, while ensuring portability on different platforms"""

    if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":

        clear_command = 'clear'
        # command for clearing the terminal is 'clear' in unix based operating systems

    else:

        clear_command = 'cls'
        # command for clearing the command prompt is 'cls' in windows devices

    os.system(clear_command)


def str_input():
    """takes in input and ensures it is a string"""

    val = str(input('>')).lower()

    return val


def int_input():
    """takes in input and ensures it is an integer"""

    try:

        val = int(input('>'))
        return val

    except TypeError:

        return -1
    # returns an invalid input in the format of an integer


def play_music(music_path):

    mixer.init()
    mixer.music.load(music_path)
    mixer.music.play(-1)
    # an input of -1 loops the music


def display_elements_from_list(input_list):
    """loops through the different types of items in the player's safe and displays them"""

    index = 1

    for item in input_list:
        colour_print(str(index) + ". " + str(item))
        index += 1
