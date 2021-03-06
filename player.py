import time

from armour import *
from weapon import Weapon
from calculations import *
from constant_attributes import upgrade_progression_dictionary, upgrade_cost_dictionary
from output_formatting import *


class Player:

    def __init__(self, name='', coordinates=[0, 0], inventory_space=3, inventory=[],
                 safe={'weapon': [], 'armour': [], 'potion': [], 'collectible': []},
                 weapon=Weapon(), armour={'helmet': Helmet(), 'chestplate': Chestplate(), 'boots': Boots()},
                 default_health=300, health=300, max_health=100, default_heal_amount=20, heal_amount=20, reputation=50,
                 intimidation=50, coins=100, default_charge=3, charge=3, max_charge=3, charge_add_amount=1,
                 default_attack_amplification_amount=1, attack_amplification_amount=1, gamesave=None):

        self.name = name
        # player name string
        self.gamesave = gamesave
        # gives the player a reference to the gamesave object that they are playing in
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
        self.update_tile_list_index()
        # sets coordinates to village coordinates, and updates the tile list index

    def heal(self):
        """heals the player, replenishing their health"""

        return self.add_health(self.heal_amount)

    def move(self, vector):
        """moves player to their intended destination"""

        destination_coordinates = [self.x + vector[0], self.y + vector[1]]
        # applies the effects of the vector passed in to the player coordinates
        destination_index = calculate_tile_list_index(self.gamesave.get_x_size(), destination_coordinates)

        # checking edge cases
        if destination_coordinates[0] > self.gamesave.get_x_size():

            colour_print("You cannot move north, you are on the north edge of the UNIVERSE")
            self.gamesave.wilderness()

        elif destination_coordinates[0] < 1:

            colour_print("You cannot move south, you are on the south edge of the UNIVERSE")
            self.gamesave.wilderness()

        elif destination_coordinates[1] > self.gamesave.get_y_size():

            colour_print("You cannot move east, you are on the east edge of the UNIVERSE")
            self.gamesave.wilderness()

        elif destination_coordinates[1] < 1:

            colour_print("You cannot move west, you are on the west edge of the UNIVERSE")
            self.gamesave.wilderness()

        elif self.gamesave.tile_list[destination_index].is_passable(self.coordinates):

            self.update_coordinates(destination_coordinates)
            self.update_tile_list_index()
            self.gamesave.enter_new_tile()
            self.gamesave.wilderness()
            # if the player can move through the tile, then the player's coordinates are updated
            # and they are taken back to the wilderness game loop

        else:

            self.gamesave.wilderness()

    def update_coordinates(self, coordinates):

        self.coordinates = coordinates
        self.x = self.coordinates[0]
        self.y = self.coordinates[1]

    def teleport(self, coordinates):
        """alters player's coordinates to provided coordinates"""

        colour_print("Teleporting...")
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

            colour_print("Your inventory is full!")

            return True

        else:

            return False

    def inventory_empty(self):
        """checks if inventory is empty"""

        if len(self.inventory) == 0:

            colour_print("Your inventory is empty!")

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
        # sends the armour piece to the correct safe armour slot by checking the armour piece's slot
        self.armour[armour_piece.get_slot()] = armour_piece
        # equips the armour piece in the correct player armour slot by checking the armour piece's slot

    def equip_weapon(self, new_weapon):
        """equips a new weapon for the player to use and puts their old weapon in their inventory"""

        colour_print("You have equipped " + str(self.safe['weapon']) + " and " + str(self.weapon) +
                     " has been added to your safe")
        self.safe['weapon'].append(self.weapon)
        self.weapon = new_weapon

    def add_item_to_inventory(self, item):
        """equips a new item into the players inventory"""

        if not self.inventory_full():

            self.inventory.append(item)

        else:

            colour_print("Your inventory is full. Item has been adeed to your safe")
            self.safe[item.get_type()].append(item)
            # if a player's inventory is full, the item is sent to the safe

    def remove_item_from_inventory(self, item):
        """removes an item from the inventory"""

        if item in self.inventory:
            self.safe[item.get_type()].append(item)
            self.inventory.remove(item)

    def inventory_interface(self):
        """allows the player to look through their inventory and send items to their safe"""

        while not self.inventory_empty():

            # inventory interface is not available if a player's inventory is empty
            self.display_inventory()
            colour_print("Would you like to (S)end an item to your safe or (B)ack out")
            inventory_choice = str_input()

            if inventory_choice == 'send' or inventory_choice == 's':

                colour_print("Which item would you like to send to your safe (enter the number)")
                safe_choice = int_input()

                if 0 < safe_choice <= len(self.inventory):
                    # checks if the selected choice is within the bounds of the inventory

                    self.safe[self.inventory[safe_choice - 1].get_type()].append(self.inventory[safe_choice - 1])
                    # sends the item to the safe
                    self.inventory.pop(safe_choice - 1)
                    # removes the item from the inventory

                else:

                    invalid_input()

            elif inventory_choice == 'back' or inventory_choice == 'b':

                break
                # if the player chooses to back out of their safe, the loop ends

            else:

                invalid_input()

    def safe_interface(self):
        """allows the player to look through their safe and send items to their inventory"""

        while True:

            self.display_safe()

            colour_print("Would you like to (T)ake an item into your inventory, "
                         "(P)ut an item into your safe, (E)xchange a weapon, (C)hange armour, or (B)ack out")
            safe_choice = str_input()

            if safe_choice == 't' or safe_choice == 'take' and not self.inventory_full():

                while True:

                    colour_print("Would you like to take a (P)otion, (C)ollectible, or (B)ack out")
                    equip_choice = str_input()

                    if equip_choice == 'p' or equip_choice == 'potion':

                        display_elements_from_list(self.safe['potion'])
                        colour_print("Enter the potion number you would like to equip")
                        potion_choice = int_input()

                        if 0 < potion_choice <= len(self.safe['potion']):
                            # checks if the selected potion is within the bounds of the potion list

                            self.add_item_to_inventory(self.safe['potion'][potion_choice - 1])
                            # item is appended to the inventory
                            self.safe['potion'].pop(potion_choice - 1)
                            # item is removed from safe

                        else:

                            invalid_input()

                    elif equip_choice == 'c' or equip_choice == 'collectible':

                        display_elements_from_list(self.safe['collectible'])
                        colour_print("Enter the weapon number you would like to equip")
                        collectible_choice = int_input()

                        if collectible_choice <= len(self.safe['collectible']):

                            self.add_item_to_inventory(self.safe['collectible'][collectible_choice - 1])
                            self.safe['collectible'].pop(collectible_choice - 1)

                        else:

                            invalid_input()

                    elif equip_choice == 'b' or equip_choice == 'back':

                        break

                    else:

                        invalid_input()

            elif safe_choice == 'p' or safe_choice == 'put':

                self.inventory_interface()
                # launches the inventory interface if the player chooses to put items from inventory into the safe

            elif safe_choice == 'e' or safe_choice == 'exchange':

                display_elements_from_list(self.safe['weapon'])
                colour_print("Enter the weapon number you would like to equip")
                weapon_choice = int_input()

                if 0 < weapon_choice <= len(self.safe['weapon']):
                    # checks if the weapon choice is within the bounds of the list of weapons

                    self.safe['weapon'].append(self.weapon)
                    # adds player's weapon to safe
                    self.weapon = self.safe['weapon'][weapon_choice - 1]
                    # makes player's weapon attribute equal to the weapon choice from the safe
                    self.safe['weapon'].pop(weapon_choice - 1)
                    # removes the chosen weapon from the safe as it has been taken by the player

                    break

                else:

                    invalid_input()

            elif safe_choice == 'c' or safe_choice == 'change':

                display_elements_from_list(self.safe['armour'])
                colour_print("Enter the armour number you would like to equip")
                armour_choice = int_input()

                if armour_choice <= len(self.safe['armour']):

                    self.safe['armour'].append(self.armour[self.safe['armour'][armour_choice - 1].get_slot()])
                    # adds the player's armour piece (of the same slot as the player's armour selection) to the safe
                    self.armour[armour_choice - 1] = self.safe['armour'][armour_choice - 1]
                    # equips the player's armour selection into the respective armour slot
                    self.safe['armour'].pop(armour_choice - 1)
                    # removes the player's armour selection from the safe as it has been taken out by the player

                    break

                else:

                    invalid_input()

            elif safe_choice == 'b' or safe_choice == 'back':

                break

            elif self.inventory_full():

                colour_print("Your inventory is full")

            else:

                invalid_input()

    def display_inventory(self):

        colour_print("INVENTORY (inventory size " + str(self.inventory_space) + "): ")
        display_elements_from_list(self.inventory)

    def display_safe(self):

        colour_print("SAFE:")

        for item_group in self.safe:
            colour_print("\n" + item_group.capitalize() + ":\n")
            display_elements_from_list(self.safe[item_group])
            # separates the item types in the safe and displays them in groups

    def lose_health_from_attack(self, attack_damage, hostile_name):
        """causes the player to lose health due to hostile attack as specified by parameter attack_damage"""

        health_lost = self.lose_health(attack_damage)
        colour_print(hostile_name + " has dealt " + str(health_lost) + " to " + self.name)

    def gain_charge(self):
        """causes the player to gain charge"""

        if self.charge < self.default_charge:

            colour_print("Charging...")
            time.sleep(1)

            if self.charge + self.charge_add_amount <= self.default_charge:

                colour_print("You have gained " + str(self.charge_add_amount) + " charge")
                self.charge += self.charge_add_amount

            else:

                colour_print("You have gained " + str(self.default_charge - self.charge) + " charge")
                self.charge = self.default_charge
                # if the player's charge would be past maximum charge after charging, then it sets the charge to maximum
                # to prevent the player getting more charge than the maximum amount of charge

    def add_money(self, amount):
        """causes the player to gain the amount of money specified in the parameter amount"""

        self.coins += amount
        colour_print("You gained " + str(amount) + " coins")

    def apply_buffs(self):
        """loops through the player's buffs and applies all the effects
        and removes buffs that have finished their duration"""

        for buff in self.active_buffs:

            buff.apply_buff()

            if buff.get_duration():
                # every round in a fight the duration of a buff is checked by this method

                if buff.get_effect() == 'block_healing':

                    colour_print("Your healing has been blocked!")
                    self.heal_amount = 0

                elif buff.get_effect() == 'block_defence':

                    colour_print("Your defence has been removed!")
                    self.defence = 0

                elif buff.get_effect() == 'regeneration':

                    regeneration_amount = self.default_heal_amount * buff.get_effectiveness()
                    colour_print("You have regenerated " + str(regeneration_amount) + " health")
                    self.add_health(int(self.default_heal_amount * buff.get_effectiveness()))

                elif buff.get_effect() == 'poison':

                    poison_amount = (self.heal_amount / 2) * buff.get_effectiveness()
                    colour_print("You have lost " + str(poison_amount) + " from poison")
                    self.lose_health((self.heal_amount / 2) * buff.get_effectiveness())

                buff.apply_buff()

            else:

                if buff.get_effect() == 'block_healing':

                    self.heal_amount = self.default_heal_amount
                    # removing the changes made by the buff when the duration runs out

                elif buff.get_effect() == 'block_defence':

                    self.defence = self.calculate_defence()

                self.remove_buff(buff)

                # when the duration of a buff reaches 0, the buff is removed

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

            colour_print("You cannot afford this")

            return False

    def reforge_weapon(self):
        """reforges the player's weapon for 20 coins"""

        if self.purchase(20):
            self.weapon.reforge()
            colour_print("Your weapon has been reforged, it is now " + str(self.weapon.get_condition()))

    def buy_item(self, price, item):
        """allows the player to buy an item for a price and adds it to their inventory"""

        if not self.inventory_full():

            if self.purchase(price):
                self.inventory.append(item)
                colour_print(item + " has been added to your inventory")

    def spare(self):
        """method that does all of the attribute changes when a player spares a hostile"""

        self.reputation = min(self.reputation + 5, 100)
        self.intimidation = max(self.intimidation - 5, 0)
        # min and max ensure that neither intimidation nor reputation fall above 100 or below 0 as they are percentages
        colour_print("You have gained 5% more reputation")
        colour_print("You have lost 5% of your intimidation")

    def kill(self):
        """method that does all of the attribute changes when a player kills a hostile"""

        self.intimidation = min(self.intimidation + 5, 100)
        self.reputation = max(self.reputation - 5, 0)
        # min and max ensure that neither intimidation nor reputation fall above 100 or below 0 as they are percentages
        colour_print("You have gained 5% more intimidation")
        colour_print("You have lost 5% of your reputation")

    def die(self, starting_health, starting_inventory):
        """initiates dying sequence and respawns the player with the amount of health they had before the fight"""

        colour_print("You Died.")
        self.set_health(starting_health)
        self.set_inventory(starting_inventory)

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

            if self.affordable(upgrade_cost_dictionary['health']):
                colour_print("Your health has been upgraded by " +
                             str((self.default_health * upgrade_progression_dictionary['health'][0]) - self.max_health)
                             + " points")
                self.max_health *= upgrade_progression_dictionary['health'][0]
                # if the player's max health still has not been upgraded
                # then multiply max health by the first multiplier

        elif self.max_health / upgrade_progression_dictionary['health'][-1] == self.default_health:

            colour_print("You have already maximized your health upgrades!")
            # if the player's max health is at the last multiplier then they can no longer upgrade their health

        else:

            index = 0

            while index < len(upgrade_progression_dictionary['health']) - 1:

                multiplier = upgrade_progression_dictionary['health'][index]

                if self.max_health / multiplier == self.default_health:
                    # loops through all the multipliers in the list of multipliers and checks which one is applied

                    if self.affordable(upgrade_cost_dictionary['health']):
                        self.max_health = self.default_health * upgrade_progression_dictionary['health']
                        colour_print("Your health has been upgraded by " +
                                     str((self.default_health * upgrade_progression_dictionary['health'][index])
                                         - self.max_health) + " points")

                        break

                index += 1

            self.health = self.max_health
            # refills the player's health after every upgrade

    def upgrade_max_charge(self):
        """upgrades the player's max charge by adding the multiplier in the upgrade progression dictionary"""

        if self.max_charge == self.default_charge:

            if self.affordable(upgrade_cost_dictionary['charge']):
                colour_print("Your charge has been upgraded by " +
                             str(upgrade_progression_dictionary['charge'][0]) + " points")
                self.max_charge += upgrade_progression_dictionary['charge'][0]
                # if the player's max health still has not been upgraded
                # then multiply max health by the first multiplier

        elif self.max_charge - upgrade_progression_dictionary['charge'][-1] == self.default_charge:

            colour_print("You have already maximized your charge upgrades!")
            # if the player's max health is at the last multiplier then they can no longer upgrade their health

        else:

            index = 0

            while index < len(upgrade_progression_dictionary['charge']) - 1:

                add_amount = upgrade_progression_dictionary['charge'][index]

                if self.max_charge - add_amount == self.default_charge:
                    # loops through all the addition amounts in the list and checks which one is applied

                    if self.affordable(upgrade_cost_dictionary['charge']):
                        self.max_charge = self.default_health + upgrade_progression_dictionary['charge']
                        colour_print("Your charge has been upgraded by " +
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

            if self.affordable(upgrade_cost_dictionary['attack_amplification']):
                colour_print("Your attack amplification has been upgraded by " +
                             str(upgrade_progression_dictionary['attack_amplification'][0]) + " points")
                self.attack_amplification_amount = \
                    self.default_attack_amplification_amount + upgrade_progression_dictionary['attack_amplification'][0]
                # if the player's max health still has not been upgraded
                # then multiply max health by the first multiplier

        elif self.attack_amplification_amount - upgrade_progression_dictionary['attack_amplification'][-1] \
                == self.default_attack_amplification_amount:

            colour_print("You have already maximized your attack amplification upgrades!")
            # if the player's max health is at the last multiplier then they can no longer upgrade their health

        else:

            index = 0

            while index < len(upgrade_progression_dictionary['attack_amplification']) - 1:

                add_amount = upgrade_progression_dictionary['attack_amplification'][index]

                if self.attack_amplification_amount - add_amount == self.default_attack_amplification_amount:

                    if self.affordable(upgrade_cost_dictionary['attack_amplification']):
                        self.max_charge = self.default_health + upgrade_progression_dictionary['attack_amplification']
                        colour_print("Your attack amplification has been upgraded by " +
                                     str((self.default_charge + upgrade_progression_dictionary['attack_amplification']
                                          [index + 1]) - self.attack_amplification_amount) + " points")

                    break

                index += 1

    def add_health(self, health_add_amount):
        """adds the amount of health specified in the parameter to the player's health"""

        if self.health + health_add_amount < self.max_health:

            self.health += health_add_amount
            colour_print("You have replenished " + str(self.heal_amount) + " health")

        elif self.health < self.max_health:

            health_add_amount = self.max_health - self.health
            colour_print("You have replenished " + str(health_add_amount) + " health")
            self.health = self.max_health

        else:

            colour_print("You are already at max health")

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

    def set_inventory(self, inventory):
        """sets inventory to the value within the parameter"""

        self.inventory = inventory

    def change_weapon(self, weapon):

        self.weapon = weapon

    def is_reputation_high(self):
        """returns true if reputation is above or equal to 50%, and returns false if reputation is below 50%"""

        if self.reputation >= 50:

            return True

        else:

            return False

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

    def get_leaderboard_data(self):
        """returns player attributes that are relevant to the online leaderboard"""

        player_leaderboard_list = [self.name, self.reputation, self.intimidation, self.coins]

        return player_leaderboard_list

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

    def get_price_multiplier(self):
        """returns how much the price is multiplied by, which is dependant on reputation"""

        return (150 - self.reputation) / 100
        # the higher the reputation, the smaller the multiplier, thus the prices are cheaper

    def is_alive(self):

        if self.health > 0:

            return True

        else:

            return False
