import json
from ast import literal_eval


def write_tiles(file_data, file_path):
    """writes the file data provided into the json file provided"""

    with open(file_path, 'w', newline='\n') as tile_file_path:

        json.dump(file_data, tile_file_path, indent=2)


def set_up_tile_and_biomes(x_bound, y_bound, biome_bounds):
    """sets up a list of dictionaries for each tile including their x, y, and biome parameters"""

    json_output = []

    for y in range(1, y_bound + 1):

        for x in range(1, x_bound + 1):

            # loops through every x coordinate in every row of y coordinates

            for element in biome_bounds:

                x_lower_limit = biome_bounds[element]['x'][0]
                x_upper_limit = biome_bounds[element]['x'][1]
                y_lower_limit = biome_bounds[element]['y'][0]
                y_upper_limit = biome_bounds[element]['y'][1]
                # sets up the dimensions of the specific biome

                if x_lower_limit <= x <= x_upper_limit and y_lower_limit <= y <= y_upper_limit:

                    # checks which biome that the coordinate from x and y fall into
                    tile_data = {'x': x, 'y': y, 'biome': element, 'walls': [], 'composition': '', 'item_key': ''}
                    json_output.append(tile_data)
                    # appends the coordinate to the output with the correct biome

    return json_output


def set_up_walls(x_bound, dict_of_tiles_with_walls, json_list):
    """goes through a provided dictionary of tiles and their walls
    and adds them to their respective tile's dictionary in the list"""

    for element in dict_of_tiles_with_walls:

        actual_element = literal_eval(element)
        # turns the string representation of the list into an actual list
        x_value = actual_element[0]
        y_value = actual_element[1]
        index_in_json = (((y_value - 1) * x_bound) + x_value) - 1
        # as the tiles are added to the list incrementing x to it's limit within every one increment of y
        # the way to calculate the index of the tile needed is using the equation above
        json_list[index_in_json]['walls'] = dict_of_tiles_with_walls[element]
        # sets a new key 'walls' to the value of the list of walls for that tile

    return json_list


def set_up_composition(x_bound, dict_of_tiles_with_composition, json_list):
    """goes through a provided dictionary of tiles and their compositions
    and adds them to their respective tile's dictionary in the list"""

    for element in dict_of_tiles_with_composition:

        actual_element = literal_eval(element)
        x_value = actual_element[0]
        y_value = actual_element[1]
        index_in_json_list = (((y_value - 1) * x_bound) + x_value) - 1
        # as the tiles are added to the list incrementing x to it's limit within every one increment of y
        # the way to calculate the index of the tile needed is using the equation above
        json_list[index_in_json_list]['composition'] = dict_of_tiles_with_composition[element]

    return json_list


def set_up_item_keys(x_bound, dict_of_tiles_with_item_keys, json_list):
    """goes through a provided dictionary of tiles with item keys and adds the keys to their respective
    dictionaries in the list"""

    for element in dict_of_tiles_with_item_keys:

        actual_element = literal_eval(element)
        x_value = actual_element[0]
        y_value = actual_element[1]
        index_in_json_list = (((y_value - 1) * x_bound) + x_value) - 1
        # as the tiles are added to the list incrementing x to it's limit within every one increment of y
        # the way to calculate the index of the tile needed is using the equation above
        json_list[index_in_json_list]['item_key'] = dict_of_tiles_with_item_keys[element]

    return json_list


def set_up_tiles(x_bound, y_bound, biome_bounds, tiles_with_walls, tiles_with_compositions, tiles_with_item_keys):
    """uses all set up functions to set up all the required parameters for a tile object"""

    json_list = set_up_tile_and_biomes(x_bound, y_bound, biome_bounds)
    json_list = set_up_walls(x_bound, tiles_with_walls, json_list)
    json_list = set_up_composition(x_bound, tiles_with_compositions, json_list)
    json_list = set_up_item_keys(x_bound, tiles_with_item_keys, json_list)

    return json_list


# SETTING UP MY MAP
path = 'tiles.json'
x_size = 15
y_size = 13
biome_limits = {
    'grass_lands': {'x': [6, 10], 'y': [5, 9]},
    'offices': {'x': [1, 5], 'y': [1, 9]},
    'lava_lake': {'x': [6, 10], 'y': [1, 4]},
    'tundra': {'x': [1, 10], 'y': [10, 13]},
    'goblin_forest': {'x': [11, 15], 'y': [8, 13]},
    'sycamore_forest': {'x': [11, 15], 'y': [1, 7]}
}
tile_walls = {
    '[1, 1]': [[2, 1]],
    '[2, 1]': [[1, 2]],
    '[14, 1]': [[14, 2]],
    '[1, 2]': [[2, 2]],
    '[2, 2]': [[1, 2], [2, 3]],
    '[14, 2]': [[14, 1], [15, 2]],
    '[1, 3]': [[1, 4]],
    '[2, 3]': [[2, 2], [2, 4]],
    '[15, 3]': [[15, 2]],
    '[1, 4]': [[1, 3]],
    '[2, 4]': [[2, 3]],
    '[14, 4]': [[13, 4], [14, 5]],
    '[9, 8]': [[8, 8], [10, 8], [9, 7], [9, 9]]
}
# MUST INCLUDE THE STRING 'boss' AT THE END OFTILE COMPOSITIONS WITH BOSSES IN THEM
tile_compositions = {
    '[11, 1]': 'river',
    '[15, 2]': 'leah_boss',
    '[1, 2]': 'janice_boss',
    '[12, 2]': 'river',
    '[15, 5]': 'river',
    '[8, 7]': 'village',
    '[9, 8]': 'grave_boss',
    '[15, 10]': 'mountain',
    '[14, 11]': 'entrance',
    '[3, 12]': 'giant_boss',
    '[13, 12]': 'mountain',
    '[12, 13]': 'mountain',
    '[14, 13]': 'barry_goblin_boss'
}
tile_item_keys = {
}

tiles_list = set_up_tiles(x_size, y_size, biome_limits, tile_walls, tile_compositions, tile_item_keys)
write_tiles(tiles_list, path)
