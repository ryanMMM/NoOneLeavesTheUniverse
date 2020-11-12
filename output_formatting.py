import os
import sys


def clear_screen():
    """clears the command line screen, while ensuring portability on different platforms"""

    if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
        clear_command = 'clear'
        # command for clearing the terminal is 'clear' in unix based operating systems
    else:
        clear_command = 'cls'
        # command for clearing the command prompt is 'cls' in windows devices

    try:
        os.system(clear_command)
    except:
        raise Exception("An has occurred while clearing the command line")


def str_input():
    """takes in input and ensures it is a string"""

    try:
        val = str(input('>')).lower()
        return val
    except:
        return ''


def int_input():
    """takes in input and ensures it is an integer"""

    try:
        val = int(input('>'))
        return val
    except:
        return -1


def display_elements_from_list(list):
    """loops through the different types of items in the player's safe and displays them"""

    index = 1
    for item in list:
        print(str(index) + ". " + str(item))
        index += 1
