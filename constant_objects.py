from armour import *
from attacks import Attack
from weapon import Weapon
from buff import Buff
from hostile import Hostile
from item import Potion, Collectible
from constant_attributes import *

"""
functions MUST be called in the order that they are written in this file
"""


def unpack_armour_into_objects():
    """unpacks armour attributes into objects within a dictionary"""

    armour_output_dictionary = {}

    for armour_key in armour_attribute_dictionary:

        armour_output_dictionary[armour_key] = {}
        helmet_attributes = armour_attribute_dictionary[armour_key]['helmet']
        chestplate_attributes = armour_attribute_dictionary[armour_key]['chestplate']
        boots_attributes = armour_attribute_dictionary[armour_key]['boots']

        armour_output_dictionary[armour_key]['helmet'] = Helmet(helmet_attributes['name'],
                                                              helmet_attributes['defense'],
                                                              helmet_attributes['armour_set'],
                                                              helmet_attributes['cost'])
        armour_output_dictionary[armour_key]['chestplate'] = Chestplate(chestplate_attributes['name'],
                                                                      chestplate_attributes['defense'],
                                                                      chestplate_attributes['armour_set'],
                                                                      chestplate_attributes['cost'])
        armour_output_dictionary[armour_key]['boots'] = Boots(boots_attributes['name'],
                                                            boots_attributes['defense'],
                                                            boots_attributes['armour_set'],
                                                            boots_attributes['cost'])

    return armour_output_dictionary


def unpack_buffs_into_objects():
    """unpacks buff attributes into objects within a dictionary"""

    buff_output_dictionary = {}

    for buff_key in buff_attribute_dictionary:

        buff_attributes = buff_attribute_dictionary[buff_key]

        buff_output_dictionary[buff_key] = Buff(buff_attributes['name'],
                                                buff_attributes['effect'],
                                                buff_attributes['effectiveness'],
                                                buff_attributes['duration'])

    return buff_output_dictionary


def unpack_potions_into_objects(buff_output_dictionary):
    """unpacks potion attributes into objects within a dictionary"""

    output_potion_dictionary = {}

    for potion_key in potion_attribute_dictionary:

        potion_attributes = potion_attribute_dictionary[potion_key]
        potion_buff = buff_output_dictionary[potion_attributes['buff']]

        output_potion_dictionary[potion_key] = Potion(potion_attributes['name'],
                                                      potion_attributes['description'],
                                                      potion_buff,
                                                      potion_attributes['cost'])

    return output_potion_dictionary


def unpack_attacks_into_objects(buff_output_dictionary):
    """unpacks attack attributes into objects within a dictionary"""

    attack_output_dictionary = {}

    for attack_group_key in attack_attribute_dictionary:

        attack_list = []

        for attack_attributes in attack_attribute_dictionary[attack_group_key]:

            if attack_attributes['buff'] in buff_object_dictionary:

                attack_buff = buff_output_dictionary[attack_attributes['buff']]

            else:

                attack_buff = ""

            attack_list.append(Attack(attack_attributes['name'],
                                      attack_attributes['multiplier'],
                                      attack_attributes['variance'],
                                      attack_buff))

        attack_output_dictionary[attack_group_key] = attack_list

    return attack_output_dictionary


def unpack_weapons_into_objects(attack_output_dictionary):
    """unpacks weapon attributes into objects within a dictionary"""

    weapon_output_dictionary = {}

    for weapon_key in weapon_attribute_dictionary:

        weapon_attributes = weapon_attribute_dictionary[weapon_key]
        weapon_attacks = attack_output_dictionary[weapon_key]

        weapon_output_dictionary[weapon_key] = Weapon(weapon_attributes['name'],
                                                      weapon_attributes['description'],
                                                      weapon_attributes['default_damage'],
                                                      weapon_attributes['weapon_type'],
                                                      weapon_attributes['cost'],
                                                      'sturdy',
                                                      weapon_attacks)

    return weapon_output_dictionary


def unpack_weapon_dealer_weapons_into_dictionary(weapon_output_dictionary):
    weapon_dealer_weapons_output_dictionary = {}

    keys_of_weapons_in_chests = [chest_contents_dictionary[chest_key]['weapon']
                                 for chest_key in chest_contents_dictionary]
    keys_of_weapons_not_in_chests = [weapon_key for weapon_key in weapon_output_dictionary
                                     if weapon_key not in keys_of_weapons_in_chests]
    # finds the weapons that aren't in chests to be sold by the arms dealer, as the arms dealer shouldn't sell weapons
    # that are hidden in chests

    for weapon_dealer_weapon_key in keys_of_weapons_not_in_chests:

        weapon_dealer_weapons_output_dictionary[weapon_dealer_weapon_key] = \
            weapon_output_dictionary[weapon_dealer_weapon_key]
    # sets up the list of arms dealer weapons from from the weapons that aren't in chests

    return weapon_dealer_weapons_output_dictionary


def unpack_hostiles_into_objects():
    """unpacks hostile attributes and creates a list of objects with those attributes"""

    hostile_output_dictionary = {}

    for hostile_group_key in hostile_attribute_dictionary:

        hostile_list = []

        for hostile_attributes in hostile_attribute_dictionary[hostile_group_key]:

            hostile_list.append(Hostile(hostile_attributes['name'],
                                        hostile_attributes['species'],
                                        hostile_attributes['health'],
                                        hostile_attributes['heal_amount'],
                                        hostile_attributes['damage'],
                                        hostile_attributes['defense'],
                                        hostile_attributes['coins'],
                                        hostile_attributes['difficulty_multiplier'],
                                        hostile_attributes['weakness']))

        hostile_output_dictionary[hostile_group_key] = hostile_list

    return hostile_output_dictionary


def unpack_bosses_into_objects():
    """unpacks boss attributes into objects within a dictionary"""

    boss_output_dictionary = {}

    for boss_key in boss_attribute_dictionary:

        boss_attributes = boss_attribute_dictionary[boss_key]

        boss_output_dictionary[boss_key] = Hostile(boss_attributes['name'],
                                                   boss_attributes['species'],
                                                   boss_attributes['health'],
                                                   boss_attributes['heal_amount'],
                                                   boss_attributes['damage'],
                                                   boss_attributes['defense'],
                                                   boss_attributes['coins'],
                                                   boss_attributes['difficulty_multiplier'],
                                                   boss_attributes['weakness'])

    return boss_output_dictionary


def unpack_landmark_collectibles_into_objects():
    """unpacks landmark collectible attributes into objects within a dictionary"""

    landmark_collectible_output_dictionary = {}

    for landmark_collectible_key in landmark_collectible_attribute_dictionary:

        landmark_collectible_attributes = landmark_collectible_attribute_dictionary[landmark_collectible_key]

        landmark_collectible_output_dictionary[landmark_collectible_key] = \
            Collectible(
                landmark_collectible_attributes['name'],
                landmark_collectible_attributes['description'],
                landmark_collectible_attributes['value'])

    return landmark_collectible_output_dictionary


def unpack_treasure_collectibles_into_objects():
    """unpacks landmark collectible attributes into objects within a dictionary"""

    treasure_collectible_output_dictionary = {}

    for treasure_collectible_key in treasure_collectible_attribute_dictionary:

        treasure_collectible_attributes = treasure_collectible_attribute_dictionary[treasure_collectible_key]

        treasure_collectible_output_dictionary[treasure_collectible_key] = \
            Collectible(
                treasure_collectible_attributes['name'],
                treasure_collectible_attributes['description'],
                treasure_collectible_attributes['value'])

    return treasure_collectible_output_dictionary


armour_object_dictionary = unpack_armour_into_objects()
buff_object_dictionary = unpack_buffs_into_objects()
attack_object_dictionary = unpack_attacks_into_objects(buff_object_dictionary)
weapon_object_dictionary = unpack_weapons_into_objects(attack_object_dictionary)
weapon_dealer_weapons = unpack_weapon_dealer_weapons_into_dictionary(weapon_object_dictionary)
potion_object_dictionary = unpack_potions_into_objects(buff_object_dictionary)
landmark_collectible_object_dictionary = unpack_landmark_collectibles_into_objects()
treasure_collectible_object_dictionary = unpack_treasure_collectibles_into_objects()
hostile_object_dictionary = unpack_hostiles_into_objects()
boss_object_dictionary = unpack_bosses_into_objects()
