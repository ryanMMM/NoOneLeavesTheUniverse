# TODO make whole fight buff that multiplies health by 1.5 and costs 500 coins
# TODO make heal amount upgradable
# TODO make spare and kill percentages non hard coded

import time
import re

from armour import *
from weapon import Weapon

from calculations import *
from constant_attributes import upgrade_progression_dictionary
from output_formatting import *


class Player:

    def __init__(self, name='', coordinates=[0, 0], inventory_space=3, inventory=[],
                 safe={'weapon': [], 'armour': [], 'potion': [], 'collectible': []},
                 weapon=Weapon(), armour={'helmet': Helmet(), 'chestplate': Chestplate(), 'boots': Boots()},
                 default_health=100, health=100, max_health=100, default_heal_amount=20, heal_amount=20, reputation=50,
                 intimidation=50, coins=100, default_charge=3, charge=3, max_charge=3, charge_add_amount=1,
                 default_attack_amplification_amount=1, attack_amplification_amount=1, gamesave=None):

        self.name = name
        # player name string
        self.gamesave = gamesave
        self.coordinates = coordinates
        self.x = coordinates[0]
        self.y = coordinates[0]
        # player's coordinates and position on the map, default spawns at the 0, 0
        self.tile_list_index = 0
        # list index of player is always defaulted to the village coordinates
        self.inventory_space = inventory_space
        self.inventory = inventory
        # player's inventory list contain's the players items currently being held
        # player can hold a default amount of 3 items in their inventory
        self.safe = safe
        # player's safe list contain's the items a player is storing in the village
        self.weapon = weapon
        # player weapon, object of weapon class
        self.armour = armour
        self.defence = self.calculate_defence()
        # sums up the defence of all the player's armour pieces
        # player armour, objects of respective armour classes
        self.default_health = default_health
        self.health = health
        self.max_health = max_health
        self.default_heal_amount = default_heal_amount
        self.heal_amount = heal_amount
        # player health points
        # player healamount: how much health is replenished when a player heals
        # player max_health: the maximum amount of health a player can attain
        self.reputation = reputation
        self.intimidation = intimidation
        # player reputation %: reputation of player in a village, impacts prices of items in shops
        # player intimidation %: how intimidated enemies are by a player,
        self.coins = coins
        # player coins, can be used to purchase services or items during gameplay
        self.default_charge = default_charge
        self.charge = charge
        self.max_charge = max_charge
        self.charge_add_amount = charge_add_amount
        # player charge points
        # player charge add amount: how much charge is replenished when a player charges
        # player max charge: the maximum amount of charge a player can attain
        self.attack_amplification_amount = attack_amplification_amount
        self.default_attack_amplification_amount = default_attack_amplification_amount
        # player attack amplification amount: how much a player can amplify their attack
        self.active_buffs = []
        # stores all of the active buffs working on the player

    def __str__(self):

        return self.name

    def spawn_at_village(self):
        """moves the player to the village"""

        self.update_coordinates(self.gamesave.village_coordinates)
        self.tile_list_index = calculate_tile_list_index(self.gamesave.get_x_size(), self.coordinates)

    def heal(self):
        """heals the player, replenishing their health"""

        return self.add_health(self.heal_amount)

    def move(self, direction, steps):
        """moves player to their intended destination"""

        destination_coordinates = self.get_destination_coordinates_and_entrance(direction, steps)['destination']
        destination_entrance = self.get_destination_coordinates_and_entrance(direction, steps)['entrance']
        destination_index = self.get_destination_tile_index(direction, steps)

        # CHECKING EDGE CASES

        if destination_coordinates[0] > self.gamesave.get_x_size():

            print("You cannot move north, you are on the north edge of the UNIVERSE")
            self.gamesave.wilderness()

        elif destination_coordinates[0] < 1:

            print("You cannot move south, you are on the south edge of the UNIVERSE")
            self.gamesave.wilderness()

        elif destination_coordinates[1] > self.gamesave.get_y_size():

            print("You cannot move east, you are on the east edge of the UNIVERSE")
            self.gamesave.wilderness()

        elif destination_coordinates[1] < 1:

            print("You cannot move west, you are on the west edge of the UNIVERSE")
            self.gamesave.wilderness()

        elif self.gamesave.tile_list[destination_index].is_passable(destination_entrance):

            self.update_coordinates(destination_coordinates)
            self.update_tile_list_index()
            self.gamesave.enter_new_tile()
            self.gamesave.wilderness()

        else:

            self.gamesave.wilderness()

    def update_coordinates(self, coordinates):

        self.coordinates = coordinates
        self.x = self.coordinates[0]
        self.y = self.coordinates[1]

    def teleport(self, coordinates):
        """alters player's coordinates to provided coordinates"""

        print("Teleporting...")
        time.sleep(1.5)
        self.update_coordinates(coordinates)
        self.update_tile_list_index()

    def update_tile_list_index(self):
        """updates the value of the tile list index"""

        self.tile_list_index = calculate_tile_list_index(self.gamesave.get_x_size(), self.coordinates)

    def inspect_item(self, index):
        """displays the details of a specific item in the player's inventory"""

        inspected_item = self.inventory[index - 1]

        return inspected_item.get_details()

    def change_gamesave(self, gamesave):
        """gives the player a new reference to a game save"""

        self.gamesave = gamesave

    def inventory_full(self):
        """checks if the player's inventory is full and whether they can pick up more items or not"""

        if len(self.inventory) >= self.inventory_space:

            print("Your inventory is full")

            return True

        else:

            return False

    def armour_set_check(self):
        """checks if the player's armour is all the same set"""

        set_list = [armour_piece.get_set() for armour_piece in self.armour.values()]

        if len(set(set_list)) == 1:

            # puts list into set, if the set has length of 1, then all armour set values are equal
            return True

        else:

            return False

    def equip_armour(self, armour_piece):
        """equips a new armour piece on the player's person and puts their old armour piece in their safe"""

        self.safe['armour'].append(self.armour[armour_piece.get_slot()])
        self.armour[armour_piece.get_slot()] = armour_piece

    def equip_weapon(self, new_weapon):
        """equips a new weapon for the player to use and puts their old weapon in their inventory"""

        print("You have equipped " + str(self.safe['weapon']) + " and " + str(self.weapon) +
              " has been added to your safe")
        self.safe['weapon'].append(self.weapon)
        self.weapon = new_weapon

    def add_item_to_inventory(self, item):
        """equips a new item into the players inventory"""

        if not self.inventory_full():

            self.inventory.append(item)

        else:

            print("Your inventory is full. Item has been adeed to your safe")
            self.safe[item.get_type()].append(item)

    def remove_item_from_inventory(self, item):
        """removes an item from the inventory"""

        if item in self.inventory:

            self.safe[item.get_type()].append(item)
            self.inventory.remove(item)

    def inventory_interface(self):
        """allows the player to look through their inventory and send items to their safe"""

        while len(self.inventory) > 0:

            # inventory interface is not available if a player's inventory is empty
            self.display_inventory()
            print("Would you like to (S)end an item to your safe or (B)ack out")
            inventory_choice = str_input()

            if inventory_choice == 'send' or inventory_choice == 's':

                print("Which item would you like to send to your safe (enter the number)")
                safe_choice = int_input()

                if safe_choice <= len(self.inventory):

                    self.safe[self.inventory[safe_choice - 1].get_type()].append(self.inventory[safe_choice - 1])
                    self.inventory.pop(safe_choice - 1)

                else:

                    print("Invalid Input")
                    # prompts the player again if invalid input

            elif inventory_choice == 'back' or inventory_choice == 'b':

                break

            else:

                print("Invalid Input")
                # prompts the user again if invalid input

    def safe_interface(self):
        """allows the player to look through their safe and send items to their inventory"""

        while True:

            self.display_inventory()
            self.display_safe()

            print("Would you like to (T)ake an item into your inventory, "
                  "(P)ut an item into your safe, (E)xchange a weapon, (C)hange armour, or (B)ack out")
            safe_choice = str_input()

            if safe_choice == 't' or safe_choice == 'take' and not self.inventory_full():

                while True:

                    print("Would you like to take a (P)otion, (C)ollectible, or (B)ack out")
                    equip_choice = str_input()

                    if equip_choice == 'p' or equip_choice == 'potion':

                        display_elements_from_list(self.safe['potion'])
                        print("Enter the potion number you would like to equip")
                        potion_choice = int_input()

                        if potion_choice <= len(self.safe['potion']):

                            self.add_item_to_inventory(self.safe['potion'][potion_choice - 1])
                            self.safe['potion'].pop(potion_choice - 1)

                        else:

                            print("Invalid input")

                    elif equip_choice == 'c' or equip_choice == 'collectible':

                        display_elements_from_list(self.safe['collectible'])
                        print("Enter the weapon number you would like to equip")
                        collectible_choice = int_input()

                        if collectible_choice <= len(self.safe['collectible']):

                            self.add_item_to_inventory(self.safe['collectible'][collectible_choice - 1])
                            self.safe['collectible'].pop(collectible_choice - 1)

                        else:

                            print("Invalid input")

                    elif equip_choice == 'b' or equip_choice == 'back':

                        break

                    else:

                        print("Invalid Input")

            elif safe_choice == 'p' or safe_choice == 'put':

                self.inventory_interface()

            elif safe_choice == 'e' or safe_choice == 'exchange':

                display_elements_from_list(self.safe['weapon'])
                print("Enter the weapon number you would like to equip")
                weapon_choice = int_input()

                if weapon_choice <= len(self.safe['weapon']):

                    self.safe['weapon'].append(self.weapon)
                    self.weapon = self.safe['weapon'][weapon_choice - 1]
                    self.safe['weapon'].pop(weapon_choice - 1)

                    break

                else:

                    print("Invalid input")

            elif safe_choice == 'c' or safe_choice == 'change':

                display_elements_from_list(self.safe['armour'])
                print("Enter the armour number you would like to equip")
                armour_choice = int_input()
                if armour_choice <= len(self.safe['armour']):

                    self.safe['armour'].append(self.armour[self.safe['armour'][armour_choice - 1].get_slot()])
                    self.armour[armour_choice - 1] = self.safe['armour'][armour_choice - 1]
                    self.safe['armour'].pop(armour_choice - 1)

                    break

                else:

                    print("Invalid input")

            elif safe_choice == 'b' or safe_choice == 'back':

                break

            elif self.inventory_full():

                print("Your inventory is full")

            else:

                print("Invalid input")

    def display_inventory(self):

        print("INVENTORY (inventory size " + str(self.inventory_space) + "): ")
        display_elements_from_list(self.inventory)

    def display_safe(self):

        print("SAFE:")

        for item_group in self.safe:

            print("\n" + item_group.capitalize() + ":\n")
            display_elements_from_list(self.safe[item_group])

    def lose_health_from_attack(self, attack_damage, hostile_name):
        """causes the player to lose health due to hostile attack as specified by parameter attack_damage"""

        health_lost = self.lose_health(attack_damage)
        print(hostile_name + " has dealt " + str(health_lost) + " to " + self.name)

    def gain_charge(self):
        """causes the player to gain charge"""

        if self.charge < self.default_charge:

            print("Charging...")
            time.sleep(1)

            if self.charge + self.charge_add_amount <= self.default_charge:

                print("You have gained " + str(self.charge_add_amount) + " charge")
                self.charge += self.charge_add_amount

            else:

                print("You have gained " + str(self.default_charge - self.charge) + " charge")
                self.charge = self.default_charge

    def add_money(self, amount):
        """causes the player to gain the amount of money specified in the parameter amount"""

        self.coins += amount
        print("You gained " + str(amount) + " coins")

    def apply_buffs(self):
        """loops through the player's buffs and applies all the effects
        and removes buffs that have finished their duration"""

        # TODO buff that negates defence

        for buff in self.active_buffs:

            if buff.get_duration():

                if buff.get_effect() == 'block_healing':

                    print("Your healing has been blocked!")
                    self.heal_amount = 0

                elif buff.get_effect() == 'block_defence':

                    print("Your defence has been removed!")
                    self.defence = 0

                elif buff.get_effect() == 'regeneration':

                    self.add_health(self.default_heal_amount * buff.get_effectiveness())

                elif buff.get_effect() == 'poison':

                    self.lose_health((self.heal_amount / 2) * buff.get_effectiveness())

                buff.apply_buff()

            else:

                if buff.get_effect() == 'block_healing':

                    self.heal_amount = self.default_heal_amount
                    # removing the changes made by the buff when the duration runs out

                elif buff.get_effect() == 'block_defence':

                    self.defence = self.calculate_defence()

                self.remove_buff(buff)

    def affordable(self, price):
        """checks if player can afford an item by comparing the parameter price to the player's coin balance"""

        if self.coins >= price:

            return True

        else:

            return False

    def purchase(self, price):
        """causes the player to lose an amount of money after a purchase"""

        if self.affordable(price):

            self.coins -= price

            return True

        else:

            print("You cannot afford this")

            return False

    def reforge_weapon(self):
        """reforges the player's weapon for 20 coins"""

        if self.purchase(20):

            self.weapon.reforge()
            print("Your weapon has been reforged, it is now " + str(self.weapon.get_condition()))

    def buy_item(self, price, item):
        """allows the player to buy an item for a price and adds it to their inventory"""

        if not self.inventory_full():

            if self.purchase(price):

                self.inventory.append(item)
                print(item + " has been added to your inventory")

    def spare(self):
        """method that does all of the attribute changes when a player spares a hostile"""

        self.reputation = min(self.reputation + 5, 100)
        self.intimidation = max(self.intimidation - 5, 0)
        # min and max ensure that neither intimidation nor reputation fall above 100 or below 0 as they are percentages
        print("You have gained 5% more reputation")
        print("You have lost 5% of your intimidation")

    def kill(self):
        """method that does all of the attribute changes when a player kills a hostile"""

        self.intimidation = min(self.intimidation + 5, 100)
        self.reputation = max(self.reputation - 5, 0)
        # min and max ensure that neither intimidation nor reputation fall above 100 or below 0 as they are percentages
        print("You have gained 5% more intimidation")
        print("You have lost 5% of your reputation")

    def die(self, starting_health):
        """initiates dying sequence and respawns the player with the amount of health they had before the fight"""

        print("You Died.")
        self.set_health(starting_health)

    def respawn(self):
        """respawns the player after a death"""

        self.coordinates = self.gamesave.get_village_coordinates()
        self.coordinates = self.gamesave.get_village_coordinates()

    def change_name(self, name):

        self.name = name

    def add_buff(self, buff):

        self.active_buffs.append(buff)

    def remove_buff(self, buff):

        self.active_buffs.remove(buff)

    def upgrade_max_health(self):
        """upgrades the player's max health by multiplying the default health by a the multiplier in the parameter"""

        if self.max_health == self.default_health:

            print("Your health has been upgraded by " +
                  str((self.default_health * upgrade_progression_dictionary['health'][0]) - self.max_health)
                  + " points")
            self.max_health *= upgrade_progression_dictionary['health'][0]
            # if the player's max health still has not been upgraded then multiply max health by the first multiplier

        elif self.max_health / upgrade_progression_dictionary['health'][-1] == self.default_health:

            print("You have already maximized your health upgrades!")
            # if the player's max health is at the last multiplier then they can no longer upgrade their health

        else:

            index = 0

            while index < len(upgrade_progression_dictionary['health']) - 1:

                multiplier = upgrade_progression_dictionary['health'][index]

                if self.max_health / multiplier == self.default_health:

                    self.max_health = self.default_health * upgrade_progression_dictionary['health']
                    print("Your health has been upgraded by " +
                          str((self.default_health * upgrade_progression_dictionary['health'][index]) - self.max_health)
                          + " points")

                    break

                index += 1

            self.health = self.max_health
            # refills the player's health after every upgrade

    def upgrade_max_charge(self):
        """upgrades the player's max charge by adding the multiplier in the upgrade progression dictionary"""

        if self.max_charge == self.default_charge:

            print("Your charge has been upgraded by " +
                  str(upgrade_progression_dictionary['charge'][0]) + " points")
            self.max_charge += upgrade_progression_dictionary['charge'][0]
            # if the player's max health still has not been upgraded then multiply max health by the first multiplier

        elif self.max_charge - upgrade_progression_dictionary['charge'][-1] == self.default_charge:

            print("You have already maximized your charge upgrades!")
            # if the player's max health is at the last multiplier then they can no longer upgrade their health

        else:

            index = 0

            while index < len(upgrade_progression_dictionary['charge']) - 1:

                add_amount = upgrade_progression_dictionary['charge'][index]

                if self.max_charge - add_amount == self.default_charge:

                    self.max_charge = self.default_health + upgrade_progression_dictionary['charge']
                    print("Your charge has been upgraded by " +
                          str((self.default_charge + upgrade_progression_dictionary['charge'][index + 1])
                              - self.max_charge) + " points")

                    break

                index += 1

            self.charge = self.max_charge
            # refills the player's charge after an upgrade

    def upgrade_attack_amplification(self):
        """upgrades the player's max attack amplification by adding the
        multiplier in the upgrade progression dictionary"""

        if self.attack_amplification_amount == self.default_attack_amplification_amount:

            print("Your attack amplification has been upgraded by " +
                  str(upgrade_progression_dictionary['attack_amplification'][0]) + " points")
            self.attack_amplification_amount = \
                self.default_attack_amplification_amount + upgrade_progression_dictionary['attack_amplification'][0]
            # if the player's max health still has not been upgraded then multiply max health by the first multiplier

        elif self.attack_amplification_amount - upgrade_progression_dictionary['attack_amplification'][-1]\
                == self.default_attack_amplification_amount:

            print("You have already maximized your attack amplification upgrades!")
            # if the player's max health is at the last multiplier then they can no longer upgrade their health

        else:

            index = 0

            while index < len(upgrade_progression_dictionary['attack_amplification']) - 1:

                add_amount = upgrade_progression_dictionary['attack_amplification'][index]

                if self.attack_amplification_amount - add_amount == self.default_attack_amplification_amount:

                    self.max_charge = self.default_health + upgrade_progression_dictionary['attack_amplification']
                    print("Your attack amplification has been upgraded by " +
                          str((self.default_charge + upgrade_progression_dictionary['attack_amplification'][index + 1])
                              - self.attack_amplification_amount) + " points")

                    break

                index += 1

    def add_health(self, health_add_amount):
        """adds the amount of health specified in the parameter to the player's health"""

        if self.health + health_add_amount < self.max_health:

            self.health += health_add_amount
            print("You have replenished " + str(self.heal_amount) + " health")

        elif self.health < self.max_health:

            health_add_amount = self.max_health - self.health
            print("You have replenished " + str(health_add_amount) + " health")
            self.health = self.max_health

        else:

            print("You are already at max health")

            return False

        return health_add_amount

    def lose_health(self, health_lose_amount):
        """subtracts the amount of health specified in the paramter from the player's health"""

        health_lose_amount = (health_lose_amount - (health_lose_amount * (self.defence / 100)))

        if self.health - health_lose_amount > 0:

            self.health -= health_lose_amount

        else:

            health_lose_amount = self.health
            self.health = 0

        return health_lose_amount

    def set_health(self, health):
        """sets health to the value within the parameter"""

        self.health = health

    def calculate_defence(self):
        """calculates the defence by summing up the defence points in each armour set"""

        defence = {armour_piece: armour_piece.get_defence() for armour_piece in self.armour.values()}

        return sum(defence.values())

    def display_battle_stats(self):
        """displays player attributes relevant to a battle"""

        battle_stats = "\n" + "#" * 10 + " " + self.name.upper() + " " + "#" * 10 + "\n"
        battle_stats += self.name.capitalize() + "'s Health: " + str(self.health) + "\n"
        battle_stats += self.name.capitalize() + "'s Charge: " + str(self.charge) + "\n"
        battle_stats += "#" * (22 + len(self.name)) + "\n"

        return battle_stats

    def display_monetary_stats(self):
        """displays player attributes relevant to a shop"""

        shop_stats = self.name + "'s coins: " + str(self.coins) + "\n"
        shop_stats += self.name + "'s Reputation: " + str(self.reputation)

        return shop_stats

    def display_navigation_stats(self):
        """displays player attributes and information relevant to navigation through the map"""

        navigation_stats = self.name + "'s coordinates: [" + str(self.x) + ", " + str(self.y) + "]\n"

        return navigation_stats

    def get_destination_coordinates_and_entrance(self, direction, steps):
        """returns the coordinates of the tile that the player chooses to walk to, and the tile they will enter from"""

        if direction == 'n':

            return {'destination': [self.x, self.y + steps], 'entrance': [self.x, self.y + steps - 1]}

        elif direction == 's':

            return {'destination': [self.x, self.y - steps], 'entrance': [self.x, self.y - steps + 1]}

        elif direction == 'e':

            return {'destination': [self.x + steps, self.y], 'entrance': [self.x + steps - 1, self.y]}

        elif direction == 'w':

            return {'destination': [self.x - steps, self.y], 'entrance': [self.x - steps + 1, self.y]}

        else:

            raise ValueError

    def get_destination_tile_index(self, direction, steps):
        """returns the tile index of the tile that the player chooses to walk to"""

        return calculate_tile_list_index(self.gamesave.get_x_size(),
                                         self.get_destination_coordinates_and_entrance(direction, steps)['destination'])

    def get_potions(self):
        """loops through the inventory and returns a list of potions"""

        potions = [item for item in self.inventory if item.get_type() == 'potion']

        return potions

    def get_collectibles(self):
        """loops through the inventory and returns a list of collectibles"""

        collectibles = [item for item in self.inventory if item.get_type() == 'collectible']

        return collectibles

    def get_potion_names(self):
        """returns the names of the potions within the inventory"""

        potion_names = [str(potion) for potion in self.get_potions()]

        return potion_names

    def get_collectible_names(self):
        """returns the names of the collectibles within the inventory"""

        collectible_names = [str(collectible) for collectible in self.get_collectibles()]

        return collectible_names

    def get_attribute_dictionary(self):
        """returns player attributes in a dictionary format to be saved into JSON"""

        attribute_dictionary = {
            'name': self.name,
            'coordinates': self.coordinates,
            'inventory_space': self.inventory_space,
            'inventory': self.inventory,
            'safe': self.safe,
            'weapon': self.weapon.get_attribute_dictionary(),
            'armour': {'helmet': self.armour['helmet'].get_set(),
                      'chestplate': self.armour['chestplate'].get_set(),
                      'boots': self.armour['boots'].get_set()},
            'default_health': self.default_health,
            'health': self.health,
            'max_health': self.max_health,
            'default_heal_amount': self.default_heal_amount,
            'heal_amount': self.heal_amount,
            'reputation': self.reputation,
            'intimidation': self.intimidation,
            'coins': self.coins,
            'default_charge': self.default_charge,
            'charge': self.charge,
            'charge_add_amount': self.charge_add_amount,
        }

        return attribute_dictionary

    def get_coordinates(self):

        return [self.x, self.y]

    def get_x(self):

        return self.x

    def get_y(self):

        return self.y

    def get_tile_list_index(self):

        return self.tile_list_index

    def get_inventory_space(self):

        return self.inventory_space

    def get_inventory(self):

        return self.inventory

    def get_safe(self):

        return self.safe

    def get_defence(self):

        return self.defence

    def get_default_health(self):

        return self.default_health

    def get_health(self):

        return self.health

    def get_default_heal_amount(self):

        return self.default_heal_amount

    def get_heal_amount(self):

        return self.heal_amount

    def get_reputation(self):

        return self.reputation

    def get_intimidation(self):

        return self.intimidation

    def get_coins(self):

        return self.coins

    def get_default_charge(self):

        return self.default_charge

    def get_charge(self):

        return self.charge

    def get_charge_add_amount(self):

        return self.charge_add_amount

    def is_alive(self):

        if self.health > 0:
            return True
        else:
            return False
