import time

from output_formatting import *


class Tile:
    """class for each tile of the 2d map"""

    def __init__(self, x, y, biome, composition='', walls=None, item_key='', x_size=15, y_size=13):
        """x_size and y_size denote the dimensions of the map"""

        self.x = x
        self.y = y
        self.coordinates = [self.x, self.y]
        self.biome = biome
        # biome is the type of area it is, i.e. desert or forest
        self.composition = composition
        # composition is what the tile is composed of, i.e. a boss or a chest
        self.item_key = item_key
        # the item that allows a player to enter a tile regardless of the composition
        # this is defaulted to an empty string unless specified that a tile has unlockable walls

        if not walls:

            self.walls_surrounding_tile = []

        else:

            self.walls_surrounding_tile = walls
        # list of the coordinates of walls one tile away from the tile in any cardinal direction

        if x_size > self.x > 1 and y_size > self.y > 1:

            self.entrances = [[self.x + 1, self.y], [self.x - 1, self.y], [self.x, self.y + 1], [self.x, self.y - 1]]
            # if the tile isn't at the edge or corner of the map
            # the default entrances to the tile are all the tiles one block away in any cardinal direction

        elif self.x == 1:

            if y_size > self.y > 1:

                self.entrances = [[self.x + 1, self.y], [self.x, self.y + 1], [self.x, self.y - 1]]
                # if the tile is at the left edge but not at a corner
                # it can only be entered from the east, north, or south

            elif self.y == y_size:

                self.entrances = [[self.x + 1, self.y], [self.x, self.y - 1]]
                # if the tile is at the top left corner
                # it can only be entered from the east and south

            else:

                self.entrances = [[self.x + 1, self.y], [self.x, self.y + 1]]
                # if the tile is at the bottom left corner
                # it can only be entered from the west and north

        elif self.x == x_size:

            if y_size > self.y > 1:

                self.entrances = [[self.x - 1, self.y], [self.x, self.y + 1], [self.x, self.y - 1]]
                # if the tile is at the right edge but not at a corner
                # it can only be entered from the west, north, or south

            elif self.y == y_size:

                self.entrances = [[self.x - 1, self.y, ], [self.x, self.y - 1]]
                # if the tile is at the top right corner
                # it can only be entered from the west and south

            else:

                self.entrances = [[self.x - 1, self.y], [self.x, self.y + 1]]
                # if the tile is at the bottom right corner
                # it can only be entered from the west and north

        elif self.y == 1:

            '''there is no need to account for the top right or top left corner edge cases as 
            they have been checked in the previous conditional statements'''
            self.entrances = [[self.x + 1, self.y], [self.x - 1, self.y], [self.x, self.y + 1]]
            # if the tile is at the bottom edge but not at a corner
            # it can only be entered from the east, west, and north

        elif self.y == y_size:

            '''there is no need to account for the bottom right or bottom left corner edge cases as 
            they have been checked in the previous conditional statements'''
            self.entrances = [[self.x + 1, self.y], [self.x - 1, self.y], [self.x, self.y - 1]]
            # if the tile is at the top edge but not at a corner
            # it can only be entered from the east, west, and south

        for wall in self.walls_surrounding_tile:

            if wall in self.entrances:

                self.entrances.remove(wall)
                # removes an entrance to a tile if there is a wall there, as players cannot enter tiles through walls

    def is_passable(self, player_coordinates):
        """checks if the player can enter this tile from their position (player_coords)"""

        block_compositions = ['river', 'mountain']
        # TODO implement this to be generated, fix this

        if player_coordinates in self.entrances:

            if self.composition in block_compositions:

                print("You cannot go there, there is a " + self.composition + " in your way")

                return False

            else:

                return True

        elif player_coordinates in self.walls_surrounding_tile:

            print("You cannot go there, there is a wall in your way")

            return False

        elif self.item_key:

            print("This place is locked")

            return False

        else:

            print("TEST")

    def unlock(self, item_key):

        """removes the walls from the tiles and allows player to enter from the previous wall location"""

        if item_key == self.item_key:

            for wall in self.walls_surrounding_tile:

                self.entrances.append(wall)
                # appends the wall coordinates to the entrances, making it accessible from the wall coordinates

            return True

        else:

            print("Not unlocked")

            return False

    def remove_composition(self):
        """deletes the composition within a tile"""

        self.composition = ''

    def get_coordinates(self):

        return self.coordinates

    def get_biome(self):

        return self.biome

    def get_composition(self):

        return self.composition

    def get_item_key(self):

        return self.item_key
