def calculate_tile_list_index(x_size, coordinates):
    """calculates the index of coordinates on the map"""

    x = coordinates[0]
    y = coordinates[1]
    return (((y - 1) * x_size) + x) - 1


def calculate_length_of_lists_in_dictionary(dictionary):
    """finds the sum of the lengths of all lists in a dictionary"""

    list_of_lengths = [len(dictionary[list_value]) for list_value in dictionary]
    return sum(list_of_lengths)

