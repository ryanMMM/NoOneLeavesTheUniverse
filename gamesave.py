# TODO aadd timers in the battles
# TODO look up how to improve incremental gameplay, add timers for battles, maybe add different soundtracks maybe
# TODO weapon suggestions from game
# TODO weapon with debuffs effective for certain enemies
# TODO add hostile progression and weapon progression
# TODO add npcs in taverns who ask for items
# TODO if someone runs from a fight, they can no longer explore the wilderness for that day
# TODO add formatting function as a list that prints each text after a certain amount of time
# TODO use regex for fights to allow experienced players to attack quickly, and display list for new players
# TODO make weighted decision tree for enemies
# TODO implement multiple steps, i.e. north 3
# TODO show map display
# TODO implement help to show objectives, bosses, etc.
# TODO use conditions for while loops
# TODO make it so that new players have a new map generated
# TODO run through code, space things out, and comment as much as you can
# TODO implement boss dialogue and shop dialogue, for entering and leaving the shop
# TODO make dictionary of soundtrack file paths
# TODO use isnum() for output formatting instead
# TODO set -1 exception for if statements
# TODO display monetary stats and prices in upgrade center
# TODO make attack amplification a player attribute
# TODO change player tile so it calls from player class
# TODO make display active buffs method
# TODO setup invalid input function
# TODO remove directed buff

import time
import random
import json
import re

import winsound

from player import Player
from hostile import Hostile
from buff import *
from map_tiles import Tile
from constant_objects import *
from constant_attributes import upgrade_cost_dictionary
from output_formatting import *


class GameSave:
    """GameSave objects represent every new game a player creates"""

    def __init__(self, played_before=False, difficulty_multiplier=1, village_coordinates=[8, 7],
                 player=Player(), hostile=Hostile()):

        self.played_before = played_before
        # variable that checks if the player has played the game before
        self.difficulty_multiplier = difficulty_multiplier
        self.village_coordinates = village_coordinates
        # location of village on map
        self.player = player
        # stores the object of the current player
        self.hostile = hostile
        # stores the current loaded hostile object
        self.attack_amplification = 1
        # initialize the attack amplification at 1, to be changed dynamically in combat
        # the dimensions of the map
        self.tile_list = []
        self.unpack_tiles()
        # pulls all the attribute data from the JSON and python files and creates arrays of objects
        self.x_size = self.tile_list[-1].get_coordinates()[0]
        self.y_size = self.tile_list[-1].get_coordinates()[1]
        # finds how large the map is by checking the coordinates of the last tile in the tile list
        self.player_tile = self.tile_list[self.player.get_tile_list_index()]

    def title_screen(self):
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

        if not self.played_before:

            self.initialize_player()

    def initialize_player(self):
        """initializes a new player, taking inputs and creates a player class"""

        clear_screen()
        print("Enter your name warrior")
        name = str_input()

        while True:

            print("What difficulty would you like to play on?\n(E)asy\n(M)edium\n(H)ard")
            difficulty = str_input()

            # changes difficulty multiplier based on user input
            if difficulty == 'e' or difficulty == 'easy':

                self.difficulty_multiplier = 0.8

                break

            elif difficulty == 'm' or difficulty == 'medium':

                self.difficulty_multiplier = 1

                break

            elif difficulty == 'h' or difficulty == 'hard':

                self.difficulty_multiplier = 1.2

                break

            else:

                print("Invalid input")
                time.sleep(2)

                self.initialize_player()
                # prompts the user again

        self.set_up_difficulty_multiplier(self.difficulty_multiplier)
        # goes through the enemies in the enemy object dictionary and applies difficulty multiplier
        self.player.change_name(name)
        # change's the player object's name to the chosen name
        self.player.change_gamesave(self)
        # gives the player reference to the current gamesave
        self.player.spawn_at_village()
        # spawns the player at the village when initialized
        time.sleep(0.25)
        self.gates_of_village()

    def gates_of_village(self):
        """starts the gameplay loops of being at the gates of the village,
         asking the user where they would like to travel"""

        # starts the respective methods to take the user to the location they choose based on input
        while True:

            clear_screen()
            print("You are at the gates of the village. Would you like to venture to the (W)ilderness or (V)illage")
            venture_choice = str_input()

            if venture_choice == 'w' or venture_choice == 'wilderness':

                self.wilderness()
                break
                # once they enter the wilderness, they no longer need the gates of the village gameplay loop

            elif venture_choice == 'v' or venture_choice == 'village':

                self.village()
                # village does not break as once a player leaves the village, they remain at the gates

            else:

                print("Invalid input")
                # prompts the user again if invalid input

    def random_event(self, biome):
        """starts a random event with a 10% chance"""

        random_event_chance = random.randint(1, 10)

        if random_event_chance == 1:

            starting_health = self.player.get_health()
            # starting health is the player's health before the battle
            print("A hostile appeared!")
            time.sleep(0.25)
            clear_screen()
            self.hostile = random.choice(hostile_object_dictionary[biome])
            # loads a random hostile from the list of hostiles

            if self.fight():

                self.wilderness()
                # if the fight is won by the player they can return to the wilderness

            else:

                self.player.die(starting_health)
                self.player.respawn()
                self.enter_new_tile()
                # if the player dies during the fight,
                # then they are returned to their village with their starting health

    def wilderness(self):
        """starts the wilderness gameplay loop"""

        winsound.PlaySound("Soundtrack/village.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)

        while True:

            clear_screen()
            print(self.player.display_navigation_stats())
            print("Would you like to move (N)orth, (S)outh, (E)ast, (W)est, or (R)eturn to village?")
            wilderness_choice = str_input()
            # displays the player's location and stats and asks them with direction they would like to go

            if wilderness_choice == 'n' or wilderness_choice == 'north':

                # TODO implement regex and steps

                self.player.move('n', 1)
                break

            elif wilderness_choice == 's' or wilderness_choice == 'south':

                self.player.move('s', 1)
                break

            elif wilderness_choice == 'e' or wilderness_choice == 'east':

                self.player.move('e', 1)
                break

            elif wilderness_choice == 'w' or wilderness_choice == 'west':

                self.player.move('w', 1)
                break

            else:

                print("Invalid input")

    def enter_new_tile(self):
        """updates all the necessary player attributes and starts any events based on the tile position of the player"""

        self.player.update_tile_list_index()
        self.player_tile = self.tile_list[self.player.get_tile_list_index()]
        # updates the player's tile index and sets the attribute player tile to the
        # tile object in the tile list that corresponds with the player's location

        if self.player_tile.get_composition()[-4:] == 'boss':

            self.boss_fight(self.player_tile.get_composition())
            # checks if the composition is a type of boss by checking the last 4 characters of the composition
            # and if so, begins the bossfight with the boss in the composition of the tile

        elif self.player_tile.get_composition() == 'drawbridge':

            pass

        elif self.player_tile.get_composition() == 'landmarks':

            pass

        elif self.player_tile.get_composition() == 'chest':

            pass

        elif self.player_tile.get_composition() == 'village':

            self.gates_of_village()

        else:

            self.random_event(self.player_tile.get_biome())
            self.wilderness()
            # if there is nothing in the tile, then a random event is run for the chance of a fight starting
            # with a random hostile, then the player begins the wilderness gameplay loop

    def village(self):
        """starts the village gameplay loop"""

        winsound.PlaySound("Soundtrack/village.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)
        # plays the village music

        # starts the respective methods to take the user to where they would like to go based on input
        while True:

            print("Would you like to visit the (F)orgery, (P)otion shop, (W)eapon Dealer, (A)rmor shop, "
                  "(U)pgrade center, (M)arketplace, (S)afe, or (L)eave?")
            village_choice = str_input()

            if village_choice == 'f' or village_choice == 'forgery':

                self.forgery()

            elif village_choice == 'p' or village_choice == 'potion':

                self.potion_shop()

            elif village_choice == 'w' or village_choice == 'weapon':

                self.weapon_dealer()

            elif village_choice == 'a' or village_choice == 'armour':

                self.armour_shop()

            elif village_choice == 'u' or village_choice == 'upgrade':

                self.upgrade_center()

            elif village_choice == 'm' or village_choice == 'marketplace':

                self.marketplace()

            elif village_choice == 's' or village_choice == 'safe':

                self.open_safe()

            elif village_choice == 'l' or village_choice == 'leave':

                break

            else:

                print("Invalid input")
                # prompts the user again if invalid input

    def forgery(self):
        """starts the forgery gameplay loop, giving the player the option to reforge their weapon or leave"""

        # executes the player's choice based on input
        while True:

            self.player.display_monetary_stats()
            print("Would you like to (R)eforge your weapon for 20 coins or (L)eave the shop?")
            forgery_choice = str_input()

            if forgery_choice == 'r' or forgery_choice == 'reforge':

                self.player.reforge_weapon()
                # once a player reforges their weapon, they remain in the shop until they chose to leave
                # they remain in the shop through recursion of the forgery method

            elif forgery_choice == 'l' or forgery_choice == 'leave':

                print("Thanks for coming by!")
                break

            else:

                print("Invalid statement")
                # prompts the user again

    def potion_shop(self):
        """starts the potion shop game loop, allowing the player to purchase potions"""

        potion_list = [potion_object_dictionary[potion_key] for potion_key in potion_object_dictionary]
        # puts potions into a fixed list for the entire duration of this method's call

        while True:

            print("Welcome to the potion shop! Would you like to (B)uy potions or (L)eave")
            potion_shop_choice = str_input()

            if potion_shop_choice == 'b' or potion_shop_choice == 'buy':

                index = 1
                print("POTIONS: \n")

                for potion in potion_list:

                    print(str(index) + ". " + str(potion).capitalize() + "\nPrice: " + str(potion.get_cost()) + "\n")
                    index += 1
                    # loops through the potions and prints them out in a numbered list
                    # TODO put this all in a grid from rich library

                print(str(index) + ". Back out\n")

                print("Which potion would you like to purchase? (Enter the number of the potion)")
                potion_choice = int_input()

                if 0 < potion_choice < index:
                    # checks if the selection is within range of the list of potions

                    self.player.purchase(potion_list[potion_choice - 1].get_cost())
                    self.player.add_item_to_inventory(potion_list[potion_choice - 1])
                    # removes the cost from the player's balance, and adds the potion of choice to their inventory

                elif potion_choice == index:

                    pass
                    # if player chooses to back out they're returned to the first potion shop prompt

                else:

                    print("Invalid input")

            elif potion_shop_choice == 'l' or potion_shop_choice == 'leave':

                print("Thank you for coming by!")
                break

    def weapon_dealer(self):
        """starts the weapon dealer game loop, allowing the player to purchase weapons"""

        weapon_list = [weapon_dealer_weapons[weapon_key] for weapon_key in weapon_dealer_weapons]
        # puts weapons into a fixed list for the entire duration of this method's call

        while True:

            print("Good morning sir! I am the weapon dealer! Would you like to (B)uy weapons or (L)eave")
            weapon_dealer_choice = str_input()

            if weapon_dealer_choice == 'b' or weapon_dealer_choice == 'buy':

                index = 1
                print("WEAPONS: \n")

                for weapon in weapon_list:

                    print(str(index) + ". " + str(weapon).capitalize() + "\nPrice: " + str(weapon.get_cost()) + "\n")
                    index += 1
                    # loops through the weapons and prints them out in a numbered list

                print(str(index) + ". Back out\n")

                print("Which weapon would you like to purchase? (Enter the number of the weapon)")
                weapon_choice = int_input()

                if 0 < weapon_choice < index:
                    # checks if the selection is within range of the list of weapons

                    self.player.purchase(weapon_list[weapon_choice - 1].get_cost())
                    self.player.equip_weapon(weapon_list[weapon_choice - 1])
                    # removes the cost from the player's balance, and adds the potion of choice to their inventory

                elif weapon_choice == index:

                    pass
                    # if player chooses to back out they're returned to the first potion shop prompt

                else:

                    print("Invalid input")

            elif weapon_dealer_choice == 'l' or weapon_dealer_choice == 'leave':

                print("Thank you for coming by!")
                break

    def armour_shop(self):
        """stars the armour shop game loop, allowing the player to purchase armour"""

        armour_group_key_list = [armour_group_key for armour_group_key in armour_object_dictionary]
        armour_group_list = [armour_object_dictionary[armour_group_key] for armour_group_key in armour_group_key_list]
        # TODO check if this unorders the helment chestplate and boots
        # puts weapons into a fixed list for the entire duration of this method's call
        # to prevent variance in the order displayed, as dictionaries are unordered
        armour_order_list = ['helmet', 'chestplate', 'boots']
        # specifies the types of armour and their order

        while True:

            print("Welcome to the armour shop, would you like to (B)uy armour or (L)eave")
            armour_shop_choice = str_input()

            if armour_shop_choice == 'b' or armour_shop_choice == 'buy':

                index = 1

                for armour_group in armour_group_list:

                    print("\n" + armour_group[random.choice(armour_order_list)].get_set().upper() + "\n")
                    # loops through and prints the sets of armour

                    for armour_piece in armour_group:

                        print(str(index) + ". " + armour_order_list[index % len(armour_order_list)].capitalize() + ": "
                              + str(armour_group[armour_piece]) + "\nCost: " + str(
                            armour_group[armour_piece].get_cost()))
                        # loops through and prints all the armor pieces within each set of armour

                        index += 1

                print(str(index) + ". Back out")

                print("Which armour piece would you like to purchase? (Enter the number of the armour piece)")
                armour_choice = str_input()

                if armour_choice < index:
                    # checks if the selection is within range of the list of weapons

                    self.player.equip_armour(armour_group_list
                                             [armour_choice // len(armour_order_list)][armour_order_list]
                                             [armour_choice % len(armour_order_list)])
                    # uses floored division dividing the armour choice by the amount of pieces of armor per set
                    # to find the index of the armour set in the first set of squared brackets
                    # then uses modulus to find the index of the armour piece within the set of armour in the second
                    # squared brackets

                elif armour_choice == index:

                    pass
                    # if player chooses to back out they're returned to the first armour shop prompt

                else:

                    print("Invalid input")

            elif armour_shop_choice == 'l' or armour_shop_choice == 'leave':

                print("Thanks for coming by!")
                break

            else:

                print("Invalid input")

    def upgrade_center(self):
        """starts the upgrade center game loop, allowing the player to upgrade their attributes"""

        while True:

            print("Welcome to the upgrade center, would you like to upgrade "
                  "(H)ealth, (C)harge, or (A)ttack Amplification, or would you like to (L)eave?")
            upgrade_choice = str_input()

            if upgrade_choice == 'h' or upgrade_choice == 'health':

                self.player.upgrade_max_health()

            elif upgrade_choice == 'c' or upgrade_choice == 'charge':

                self.player.upgrade_max_charge()

            elif upgrade_choice == 'a' or upgrade_choice == 'attack':

                self.player.upgrade_attack_amplification()

            elif upgrade_choice == 'l' or upgrade_choice == 'leave':

                print("Thanks for coming by!")
                break

            else:

                print("Invalid input")

    def marketplace(self):
        """starts the weapon dealer game loop, allowing the player to sell collectibles"""

        while True:

            print("Welcome to the market! Would you like to (S)ell your collectibles or (L)eave?")
            marketplace_choice = str_input()

            if marketplace_choice == 's' or marketplace_choice == 'sell':

                if len(self.player.get_collectibles()):
                    # checks if the player has collectibles to sell

                    collectible_names_and_values = [str(collectible).capitalize() + " \nValue: "
                                                    + collectible.get_value() + "\n"
                                                    for collectible in self.player.get_collectibles()]
                    print("YOUR COLLECTIBLES:\n")
                    display_elements_from_list(collectible_names_and_values)
                    # displays the player's collectibles and their respective values
                    print(str(len(self.player.get_collectibles()) + 1) + ". Back out")
                    print("\nEnter the item number you would like to sell")
                    sell_choice = int_input()

                    if 0 < sell_choice <= len(self.player.get_collectibles()):
                        # checks if the selection is within range of the list of collectibles

                        print("You sold " + self.player.get_collectible_names()[sell_choice] + " for "
                              + str(self.player.get_collectibles()[sell_choice].get_value()) + "coins")
                        self.player.add_money(self.player.get_collectibles()[sell_choice].get_value())
                        # gives the player the amount of money they're owed for selling the collectible
                        # TODO remove collectible

                    elif sell_choice == len(self.player.get_collectibles()):

                        pass
                        # if the player backs out, they are return to the first prompt

                    else:

                        print("Invalid input")

                else:

                    print("You have no collectibles to sell! Get out and come back when you have something for me!")

                    break

            elif marketplace_choice == 'l' or marketplace_choice == 'leave':

                print("Thanks for coming by!")
                break

            else:

                print("Invalid input")

    def open_safe(self):

        while True:

            print("You arrive at your safe. Would you like to (O)pen it or (L)eave?")
            safe_choice = str_input()

            if safe_choice == 'o' or safe_choice == 'open':

                print("You unlock your safe...")
                self.player.safe_interface()

            elif safe_choice == 'l' or safe_choice == 'leave':

                print("You leave your safe")
                break

            else:

                print("Invalid input")

    def fight(self):
        """starts a fight gameplay loop between the current hostile and player"""

        clear_screen()
        winsound.PlaySound("Soundtrack/fight.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)
        # plays fight music
        turn_count = 0
        # turn count is initialized at 0, counts the amount of player turns that occur during the fight
        self.attack_amplification = 1
        # attack amplification is how much an attack is multiplied by, this can be changed by the player during battle
        self.hostile.change_difficulty_multiplier(self.difficulty_multiplier)

        # fight loop, ends when hostile or player health reaches 0 (when either dies)
        while self.player.is_alive() and self.hostile.is_alive():

            time.sleep(0.4)
            print(self.player.display_battle_stats())
            time.sleep(0.4)
            print(self.hostile.display_battle_stats())
            self.player_turn()
            self.hostile_turn()
            self.player.apply_buffs()
            self.hostile.apply_buffs()
            # every loop the player has a turn (player_turn method), then the hostile has a turn (hostile_turn method)
            turn_count += 1

        # once either the player or hostile's health reaches 0 the statement checks who's health reached 0
        # if the hostile is the one who's health reached 0, the player is prompted to spare or kill the hostile
        # otherwise the player has to reset progress to the beginning of the day
        if not self.hostile.is_alive():

            print("You Win!")
            self.spare_or_kill()
            # if the hostile is dead when the battle ends, then the player wins, and they can choose to spare or kill
            # an enemy

            return True
            # returns true if the player wins the battle

        else:

            return False
            # returns false if the player loses the battle

    def boss_fight(self, boss):
        """initiates a boss fight"""

        while True:

            print("You have reached the abode of a boss, would you like to (F)ight or (L)eave")
            boss_fight_choice = str_input()

            if boss_fight_choice == 'f' or boss_fight_choice == 'fight':

                starting_health = self.player.get_health()
                # saves the player's starting health before the fight
                self.hostile = boss_object_dictionary[boss]
                # loads the boss object into the game save's hostile attribute

                if self.fight():

                    # initiates a boss fight and checks if the player wins
                    self.tile_list[self.player.get_tile_list_index()].remove_composition()
                    # if boss is defeated, it is removed from the tile
                    self.player_tile = self.tile_list[self.player.get_tile_list_index()]
                    # removes the boss from the dictionary as it has been defeated
                    self.wilderness()
                    # if the player wins the battle, they return to the wilderness

                    break

                else:

                    self.player.die(starting_health)
                    self.player.respawn()
                    self.enter_new_tile()
                    # if the player loses the battle and dies, they spawn back at the village at their starting health

                    break

            elif boss_fight_choice == 'l' or boss_fight_choice == 'leave':

                self.wilderness()
                # sends the player back to the wilderness

            else:

                print("Invalid input")

    def player_turn(self):
        """starts the player's turn during a fight, prompting them on what they would like to do"""

        while True:

            print("Would you like to (A)ttack or (P)erform an action")
            player_choice = str_input()

            # brings up the attack menu or action menu based on the users input
            if player_choice == 'a' or player_choice == 'attack':

                self.choose_attack()

                break

            elif player_choice == 'p' or player_choice == 'perform':

                self.choose_action()

                break

            else:

                print("Invalid input")
                # prompts the user again if invalid input

    def choose_attack(self):
        """brings up the attack menu, displaying the player's attacks"""

        while True:

            clear_screen()
            index = 1

            for attack in self.player.weapon.get_attacks():

                print(str(index) + ". " + str(attack))
                index += 1

            print(str(index) + ". Back out")

            attack_choice = int_input()

            if 0 < attack_choice < index:
                # checks if the selection is within range of the list of attacks

                chosen_attack = self.player.weapon.get_attacks()[attack_choice - 1]
                # loads the attack object corresponding to the player's selection
                base_damage = self.player.weapon.get_damage()
                # loads the base damage in the player's weapon
                attack_multiplier = chosen_attack.get_multiplier()
                # loads the attack multiplier corresponding to the player's selection
                damage = base_damage * attack_multiplier * self.attack_amplification
                # calculates the damage dealt to the enemy by multiplying the variables

                if str(chosen_attack.get_buff()):

                    self.hostile.add_buff(DirectedBuff(chosen_attack.buff))
                    # if the attack has a buff in it, that buff is applied to the enemy

                self.hostile.lose_health_from_attack(damage, str(self.player))
                # removes the damage dealt from the hostile's attack
                self.attack_amplification = 1
                # once an attack has been carried out, the attack amplification is reset to 1

                break

            elif attack_choice == index:

                self.player_turn()

                break
                # if the player backs out, the return the the player turn method

            else:

                print("Invalid input")
                # prompts the user again if invalid input is given

    def choose_action(self):
        """brings up the action menu, displaying the player's actions"""

        while True:

            print("Would you like to (H)eal, (A)mplify attack, (U)se a potion, (R)echarge, or (B)ack out")
            action_choice = str_input()

            # executes an action based on the player's choice, calling the action's respective methods
            if action_choice == 'h' or action_choice == 'heal':

                self.player.heal()

            elif action_choice == 'a' or action_choice == 'amplify':

                self.attack_amplification += 1.5

            elif action_choice == 'u' or action_choice == 'use':

                self.choose_potion()

            elif action_choice == 'b' or action_choice == 'back':

                self.player_turn()

            else:

                print("Invalid input")
                # prompts the user again if invalid input is given

    def choose_potion(self):
        """presents the player's potions"""

        while True:

            clear_screen()
            index = 1
            potions = self.player.get_potions()
            # stores a list of potions, pulled from the player's inventory

            for potion in potions:

                print(str(index) + ". " + str(potion))
                index += 1

            print(str(index) + ". Back out")

            potion_choice = int_input()
            potion = potions[potion_choice]

            if 0 < potion_choice < index:
                # checks if the selection is within range of the list of potions

                self.player.remove_item_from_inventory(potion)
                # once the player uses the potion, it is removed from their inventory
                # TODO apply buff

            elif potion_choice == index:

                self.choose_action()
                # if the player backs out, the return the the choose action method

            else:

                print("Invalid input")
                # prompts the user again if invalid input is given

    def hostile_turn(self):
        """starts the hostile's turn"""

        self.player.lose_health_from_attack(self.hostile.get_damage(), str(self.hostile))

    def spare_or_kill(self):
        """starts the spare of kill part of a battle, when a player chooses whether to spare or kill an hostile"""

        while True:

            print("(S)PARE or (K)ILL")
            spare_or_kill_choice = str_input()

            # starts the player object's respective methods based on the player's choice
            if spare_or_kill_choice == 's' or spare_or_kill_choice == 'spare':

                self.player.spare()

            elif spare_or_kill_choice == 'k' or spare_or_kill_choice == 'kill':

                self.player.kill()

            else:

                print("Invalid input")
                # prompts the user again if invalid input is given

    def unpack_tiles(self):
        """unpacks tile attributes from JSON file and creates a list of objects with those attributes"""

        with open('tiles.json') as t:

            tile_attribute_list = json.load(t)

        for tile in tile_attribute_list:

            self.tile_list.append(Tile(tile['x'], tile['y'], tile['biome'], tile['composition'], tile['item_key']))

    def set_up_difficulty_multiplier(self, difficulty_multiplier):
        """sets the hostiles and bosses to the correct difficulty multiplier"""

        for hostile_group in hostile_object_dictionary:

            for hostile_list in hostile_object_dictionary[hostile_group]:

                hostile_list.change_difficulty_multiplier(difficulty_multiplier)

        for boss_key in boss_object_dictionary:

            boss_object_dictionary[boss_key].change_difficulty_multiplier(difficulty_multiplier)

    def get_attribute_dictionary(self):
        """returns the gamesave's attributes in a dictionary format to be saved into JSON"""

        attribute_dictionary = {
            'played_before': self.played_before,
            'difficulty_multiplier': self.difficulty_multiplier,
            'village_coordinates': self.village_coordinates,
            'player': self.player.get_attribute_dictionary()
        }

        return attribute_dictionary

    def get_undefeated_bosses(self):

        undefeated_boss_keys = [self.tile_list[tile]['composition'] for tile in self.tile_list
                                if self.tile_list[tile]['composition'][-4:] == 'boss']
        undefeated_bosses = [boss_object_dictionary[boss_key] for boss_key in undefeated_boss_keys]

        return undefeated_bosses

    def played_before(self):

        return self.played_before

    def get_difficulty_multiplier(self):

        return self.difficulty_multiplier

    def get_village_coordinates(self):

        return self.village_coordinates

    def get_x_size(self):

        return self.x_size

    def get_y_size(self):

        return self.y_size
