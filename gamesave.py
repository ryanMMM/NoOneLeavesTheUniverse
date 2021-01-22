# TODO aadd timers in the battles
# TODO look up how to improve incremental gameplay, add timers for battles, maybe add different soundtracks maybe
# TODO weapon suggestions from game
# TODO weapon with debuffs effective for certain enemies
# TODO add hostile progression and weapon progression
# TODO add npcs in taverns who ask for items
# TODO if someone runs from a fight, they can no longer explore the wilderness for that day
# TODO make weighted decision tree for enemies
# TODO make it so that new players have a new map generated
# TODO make dictionary of soundtrack file paths
# TODO change player tile so it calls from player class
# TODO make display active buffs method
# TODO setup invalid input function

# TODO add formatting function as a list that colour_prints each text after a certain amount of time
# TODO use regex for fights to allow experienced players to attack quickly, and display list for new players
# TODO implement multiple steps, i.e. north 3
# TODO show map display
# TODO implement help to show objectives, bosses, etc.
# TODO implement boss dialogue and shop dialogue, for entering and leaving the shop
# TODO use isnum() for output formatting instead
# TODO set -1 exception for if statements
# TODO remove directed buff

import time
import random
import json

from player import Player
from hostile import Hostile
from buff import Buff
from map_tiles import Tile
from constant_objects import *
from constant_attributes import shop_dialogue
from output_formatting import *
from save_functions import save_game, save_quit


class GameSave:
    """GameSave objects represent every new game a player creates"""

    def __init__(self, difficulty_multiplier=1, player=Player(), village_coordinates=[8, 7]):

        self.difficulty_multiplier = difficulty_multiplier
        self.village_coordinates = village_coordinates
        # location of village on map
        self.player = player
        # stores the object of the current player
        self.hostile = Hostile()
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

    def tutorial(self):
        """starts the tutorial gameloop, teaching the player how to fight and giving them some information to understand
        the gameplay mechanics"""

        colour_print("Welcome to the UNIVERSE.\nA 13x15 grid sprawling with monsters to fight."
                     "\nYou can seek refuge in the village, where you can find all kinds of shops to gear up for the "
                     "challenge ahead.\nWhen you're ready for adventure, you can leave into the wilderness."
                     "\nPRESS ENTER TO CONTINUE")
        input()
        colour_print("You will have weapons (each with their own unique attacks) and potions at your disposal."
                     "\nNow you will face a practice enemy in this tutorial before entering the UNIVERSE."
                     "\nPRESS ENTER TO CONTINUE")
        input()

        # starts the fight, if the player loses, the loop will continue
        while not self.fight():

            colour_print("Would you like to (t)ry again or (q)uit?")
            tutorial_death_choice = input()

            if tutorial_death_choice == 't' or tutorial_death_choice == 'try':

                continue

            elif tutorial_death_choice == 'q' or tutorial_death_choice == 'quit':

                save_quit()

            else:

                invalid_input()

        time.sleep(0.5)
        colour_print("Impressive. You're now ready to go out into the UNIVERSE.\nPRESS ENTER TO CONTINUE")
        input()
        play_music('soundtrack/village_music.mp3')
        self.gates_of_village()

    def gates_of_village(self):
        """starts the gameplay loops of being at the gates of the village,
         asking the user where they would like to travel"""

        # starts the respective methods to take the user to the location they choose based on input
        while True:

            clear_screen()
            colour_print("You are at the gates of the village. "
                         "Would you like to venture to the (W)ilderness or (V)illage\n\n(Q) to Quit Game")
            venture_choice = str_input()

            if venture_choice == 'w' or venture_choice == 'wilderness':

                play_music('soundtrack/wilderness_music.mp3')
                self.wilderness()
                break
                # once they enter the wilderness, they no longer need the gates of the village gameplay loop

            elif venture_choice == 'v' or venture_choice == 'village':

                self.village()
                # village does not break as once a player leaves the village, they remain at the gates

            elif venture_choice == 'q' or venture_choice == 'quit':

                save_quit(self)
                break

            else:

                invalid_input()
                # prompts the user again if invalid input

    def random_event(self, biome):
        """starts a random event with a 10% chance of starting a fight encounter"""

        random_event_chance = random.randint(1, 10)

        if random_event_chance == 1:

            starting_health = self.player.get_health()
            # starting health is the player's health before the battle
            starting_inventory = self.player.get_inventory()
            # starting inventory is the player's inventory before the battle
            colour_print("A hostile appeared!")
            time.sleep(0.25)
            clear_screen()
            self.hostile = random.choice(hostile_object_dictionary[biome])
            # loads a random hostile from the list of hostiles from the biome that the player is in

            if self.fight():

                for buff in self.player.active_buffs:
                    
                    self.player.remove_buff(buff)

                # removes all the active buffs the player recieved during the fight

                self.wilderness()
                # if the fight is won by the player they can return to the wilderness

            else:

                self.player.die(starting_health, starting_inventory)
                self.player.respawn()
                self.enter_new_tile()
                # if the player dies during the fight,
                # then they are returned to their village with their starting health and inventory restored

    def wilderness(self):
        """starts the wilderness gameplay loop"""

        while True:

            clear_screen()
            colour_print(self.player.display_navigation_stats())
            colour_print("Would you like to move (N)orth, (S)outh, (E)ast, (W)est, or (R)eturn to village?"
                         "\n\n(Q) to Quit Game")
            wilderness_choice = str_input()
            # displays the player's location and stats and asks them with direction they would like to go

            if wilderness_choice == 'n' or wilderness_choice == 'north':

                self.player.move([0, 1])
                # north increases the y value by 1
                break

            elif wilderness_choice == 's' or wilderness_choice == 'south':

                self.player.move([0, -1])
                # south decreases the y value by 1
                break

            elif wilderness_choice == 'e' or wilderness_choice == 'east':

                self.player.move([1, 0])
                # east increases the x value by 1
                break

            elif wilderness_choice == 'w' or wilderness_choice == 'west':

                self.player.move([-1, 0])
                # west decreases the x value by 1
                break

            elif wilderness_choice == 'r' or wilderness_choice == 'return':

                self.player.spawn_at_village()
                self.gates_of_village()
                break

            elif wilderness_choice == 'q' or wilderness_choice == 'quit':

                save_quit(self)
                break

            else:

                invalid_input()

    def enter_new_tile(self):
        """updates all the necessary player attributes and starts any events based on the tile position of the player"""

        self.player.update_tile_list_index()
        self.player_tile = self.tile_list[self.player.get_tile_list_index()]
        # updates the player's tile index and sets the attribute player tile to the
        # tile object in the tile list that corresponds with the player's location

        if self.player_tile.get_composition()[-4:] == 'boss':

            self.boss_fight(self.player_tile.get_composition())
            # checks if the composition is a type of boss by checking the last 4 characters of the composition
            # and if so, begins the boss fight with the boss in the composition of the tile

        elif self.player_tile.get_composition() == 'village':

            self.gates_of_village()
            # if player approaches village, call gates of village method

        else:

            self.random_event(self.player_tile.get_biome())
            self.wilderness()
            # if there is nothing in the tile, then a random event is run for the chance of a fight starting
            # with a random hostile, then the player begins the wilderness gameplay loop

    def village(self):
        """starts the village gameplay loop"""

        play_music('soundtrack/village_music.mp3')

        # starts the respective methods to take the user to where they would like to go based on input
        while True:

            colour_print("Would you like to visit the (F)orgery, (P)otion shop, (W)eapon Dealer, (A)rmor shop, "
                         "(U)pgrade center, (M)arketplace, (S)afe, (M)anually save game, or (L)eave?"
                         "\n\n(Q) to Quit Game")
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

            elif village_choice == 'g' or village_choice == 'save':

                self.village_save()

            elif village_choice == 'q' or village_choice == 'quit':

                save_quit(self)

            elif village_choice == 'l' or village_choice == 'leave':

                break

            else:

                invalid_input()
                # prompts the user again if invalid input

    def forgery(self):
        """starts the forgery gameplay loop, giving the player the option to reforge their weapon or leave"""

        # executes the player's choice based on input
        while True:

            self.player.display_monetary_stats()
            colour_print("Would you like to (R)eforge your weapon for 20 coins or (L)eave the shop?"
                         "\n\n(Q) to Quit Game")
            forgery_choice = str_input()

            if forgery_choice == 'r' or forgery_choice == 'reforge':

                self.player.reforge_weapon()
                # once a player reforges their weapon, they remain in the shop until they chose to leave
                # they remain in the shop through recursion of the forgery method

            elif forgery_choice == 'l' or forgery_choice == 'leave':

                if self.player.is_reputation_high():
                    # colour_prints exit dialogue for high reputation if the player has high reputation

                    colour_print(random.choice(shop_dialogue['forgery']['high_reputation']))

                else:
                    # colour_prints exit dialogue for low reputation if player does not have high reputation

                    colour_print(random.choice(shop_dialogue['forgery']['low_reputation']))

                break

            elif forgery_choice == 'q' or forgery_choice == 'quit':

                save_quit(self)

            else:

                invalid_input()
                # prompts the user again

    def potion_shop(self):
        """starts the potion shop game loop, allowing the player to purchase potions"""

        potion_list = [potion_object_dictionary[potion_key] for potion_key in potion_object_dictionary]
        # puts potions into a fixed list for the entire duration of this method's call

        while True:

            self.player.display_monetary_stats()
            colour_print("Welcome to the potion shop! Would you like to (B)uy potions or (L)eave\n\n(Q) to Quit Game")
            potion_shop_choice = str_input()

            if potion_shop_choice == 'b' or potion_shop_choice == 'buy':

                index = 1
                colour_print("POTIONS: \n")

                for potion in potion_list:
                    colour_print(str(index) + ". " + str(potion).capitalize()
                                 + "\nPrice: " + str(potion.get_cost() * self.player.get_price_multiplier()) + "\n")
                    index += 1
                    # loops through the potions and colour_prints them out in a numbered list

                colour_print(str(index) + ". Back out\n")

                colour_print("Which potion would you like to purchase? (Enter the number of the potion)")
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

                    invalid_input()

            elif potion_shop_choice == 'l' or potion_shop_choice == 'leave':

                if self.player.is_reputation_high():
                    # colour_prints exit dialogue for high reputation if the player has high reputation

                    colour_print(random.choice(shop_dialogue['potion_shop']['high_reputation']))

                else:
                    # colour_prints exit dialogue for low reputation if player does not have high reputation

                    colour_print(random.choice(shop_dialogue['potion_shop']['low_reputation']))

                break

            elif potion_shop_choice == 'q' or potion_shop_choice == 'quit':

                save_quit(self)

    def weapon_dealer(self):
        """starts the weapon dealer game loop, allowing the player to purchase weapons"""

        weapon_list = [weapon_dealer_weapons[weapon_key] for weapon_key in weapon_dealer_weapons]
        # puts weapons into a fixed list for the entire duration of this method's call

        while True:

            self.player.display_monetary_stats()
            colour_print("I am Paul the weapon dealer! Would you like to (B)uy weapons or (L)eave\n\n(Q) to Quit Game")
            weapon_dealer_choice = str_input()

            if weapon_dealer_choice == 'b' or weapon_dealer_choice == 'buy':

                index = 1
                colour_print("WEAPONS: \n")

                for weapon in weapon_list:
                    colour_print(str(index) + ". " + str(weapon).capitalize()
                                 + "\nPrice: " + str(weapon.get_cost() * self.player.get_price_multiplier()) + "\n")
                    index += 1
                    # loops through the weapons and colour_prints them out in a numbered list

                colour_print(str(index) + ". Back out\n")

                colour_print("Which weapon would you like to purchase? (Enter the number of the weapon)")
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

                    invalid_input()

            elif weapon_dealer_choice == 'l' or weapon_dealer_choice == 'leave':

                colour_print("Thank you for coming by!")
                break

            elif weapon_dealer_choice == 'q' or weapon_dealer_choice == 'quit':

                save_quit(self)

            else:

                print("Invalid input", "red")

    def armour_shop(self):
        """stars the armour shop game loop, allowing the player to purchase armour"""

        armour_group_key_list = [armour_group_key for armour_group_key in armour_object_dictionary]
        armour_group_list = [armour_object_dictionary[armour_group_key] for armour_group_key in armour_group_key_list]
        # puts weapons into a fixed list for the entire duration of this method's call
        # to prevent variance in the order displayed, as dictionaries are unordered
        armour_order_list = ['helmet', 'chestplate', 'boots']
        # specifies the types of armour and their order

        while True:

            self.player.display_monetary_stats()
            colour_print("Welcome to the armour shop, would you like to (B)uy armour or (L)eave\n\n(Q) to Quit Game")
            armour_shop_choice = str_input()

            if armour_shop_choice == 'b' or armour_shop_choice == 'buy':

                index = 1

                for armour_group in armour_group_list:

                    colour_print("\n" + armour_group[random.choice(armour_order_list)].get_set().upper() + "\n")
                    # loops through and colour_prints the sets of armour

                    for armour_piece in armour_group:
                        colour_print(
                            str(index) + ". " + armour_order_list[index % len(armour_order_list)].capitalize() + ": "
                            + str(armour_group[armour_piece]) + "\nCost: "
                            + str(armour_group[armour_piece].get_cost() * self.player.get_price_multiplier()))
                        # loops through and colour_prints all the armor pieces within each set of armour

                        index += 1

                colour_print(str(index) + ". Back out")

                colour_print("Which armour piece would you like to purchase? (Enter the number of the armour piece)")
                armour_choice = int_input()

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

                    invalid_input()

            elif armour_shop_choice == 'l' or armour_shop_choice == 'leave':

                colour_print("Thanks for coming by!")
                break

            elif armour_shop_choice == 'q' or armour_shop_choice == 'quit':

                save_quit(self)

            else:

                invalid_input()

    def upgrade_center(self):
        """starts the upgrade center game loop, allowing the player to upgrade their attributes"""

        while True:

            self.player.display_monetary_stats()
            colour_print("Welcome to the upgrade center, would you like to upgrade "
                         "(H)ealth, (C)harge, or (A)ttack Amplification, or would you like to (L)eave?")
            upgrade_choice = str_input()

            if upgrade_choice == 'h' or upgrade_choice == 'health':

                self.player.upgrade_max_health()

            elif upgrade_choice == 'c' or upgrade_choice == 'charge':

                self.player.upgrade_max_charge()

            elif upgrade_choice == 'a' or upgrade_choice == 'attack':

                self.player.upgrade_attack_amplification()

            elif upgrade_choice == 'l' or upgrade_choice == 'leave':

                colour_print("Thanks for coming by!")
                break

            else:

                invalid_input()

    def marketplace(self):
        """starts the weapon dealer game loop, allowing the player to sell collectibles"""

        while True:

            self.player.display_monetary_stats()
            colour_print("Welcome to the market! Would you like to (S)ell your collectibles or (L)eave?")
            marketplace_choice = str_input()

            if marketplace_choice == 's' or marketplace_choice == 'sell':

                if len(self.player.get_collectibles()):
                    # checks if the player has collectibles to sell

                    collectible_names_and_values = [str(collectible).capitalize() + " \nValue: "
                                                    + collectible.get_value() + "\n"
                                                    for collectible in self.player.get_collectibles()]
                    colour_print("YOUR COLLECTIBLES:\n")
                    display_elements_from_list(collectible_names_and_values)
                    # displays the player's collectibles and their respective values
                    colour_print(str(len(self.player.get_collectibles()) + 1) + ". Back out")
                    colour_print("\nEnter the item number you would like to sell")
                    sell_choice = int_input()

                    if 0 < sell_choice <= len(self.player.get_collectibles()):
                        # checks if the selection is within range of the list of collectibles

                        colour_print("You sold " + self.player.get_collectible_names()[sell_choice] + " for "
                                     + str(self.player.get_collectibles()[sell_choice].get_value()) + "coins")
                        self.player.add_money(self.player.get_collectibles()[sell_choice].get_value())
                        # gives the player the amount of money they're owed for selling the collectible

                    elif sell_choice == len(self.player.get_collectibles()):

                        pass
                        # if the player backs out, they are return to the first prompt

                    else:

                        invalid_input()

                else:

                    colour_print(
                        "You have no collectibles to sell! Get out and come back when you have something for me!")

                    break

            elif marketplace_choice == 'l' or marketplace_choice == 'leave':

                colour_print("Thanks for coming by!")
                break

            else:

                invalid_input()

    def open_safe(self):

        while True:

            colour_print("You arrive at your safe. Would you like to (O)pen it or (L)eave?\n\n(Q) to Quit Game")
            safe_choice = str_input()

            if safe_choice == 'o' or safe_choice == 'open':

                colour_print("You unlock your safe...")
                self.player.safe_interface()

            elif safe_choice == 'l' or safe_choice == 'leave':

                colour_print("You leave your safe")
                break

            elif safe_choice == 'q' or safe_choice == 'quit':

                save_quit(self)

            else:

                invalid_input()

    def village_save(self):

        colour_print("You sleep for the night. Saving your progress as you dream of another life in another UNIVERSE.")
        save_game(self)

    def fight(self):
        """starts a fight gameplay loop between the current hostile and player"""

        play_music('soundtrack/fight_music.mp3')
        self.hostile.change_difficulty_multiplier(self.difficulty_multiplier)
        # ensures that the hostile has the correct attributes according to the difficulty multiplier
        clear_screen()
        turn_count = 0
        # turn count is initialized at 0, counts the amount of player turns that occur during the fight
        self.attack_amplification = 1
        # attack amplification is how much an attack is multiplied by, this can be changed by the player during battle
        self.hostile.change_difficulty_multiplier(self.difficulty_multiplier)

        # fight loop, ends when hostile or player health reaches 0 (when either dies)
        while self.player.is_alive() and self.hostile.is_alive():
            time.sleep(0.4)
            colour_print(self.player.display_battle_stats())
            time.sleep(0.4)
            colour_print(self.hostile.display_battle_stats())
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

            colour_print("You Win!")
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

            colour_print("You have reached the abode of a boss, would you like to (F)ight or (L)eave"
                         "\n\n(Q) to Quit Game")
            boss_fight_choice = str_input()

            if boss_fight_choice == 'f' or boss_fight_choice == 'fight':

                starting_health = self.player.get_health()
                # saves the player's starting health before the fight
                starting_inventory = self.player.get_inventory()
                # saves the player's starting inventory before the fight
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

                    self.player.die(starting_health, starting_inventory)
                    self.player.respawn()
                    self.enter_new_tile()
                    # if the player loses the battle and dies, they spawn back at the village at their starting health

                    break

            elif boss_fight_choice == 'l' or boss_fight_choice == 'leave':

                self.wilderness()
                # sends the player back to the wilderness

            elif boss_fight_choice == 'q' or boss_fight_choice == 'quit':

                save_quit(self)

            else:

                invalid_input()

    def player_turn(self):
        """starts the player's turn during a fight, prompting them on what they would like to do"""

        while True:

            colour_print("Would you like to (A)ttack or (P)erform an action")
            player_choice = str_input()

            # brings up the attack menu or action menu based on the users input
            if player_choice == 'a' or player_choice == 'attack':

                self.choose_attack()

                break

            elif player_choice == 'p' or player_choice == 'perform':

                self.choose_action()

                break

            else:

                invalid_input()
                # prompts the user again if invalid input

    def choose_attack(self):
        """brings up the attack menu, displaying the player's attacks"""

        while True:

            clear_screen()
            index = 1

            for attack in self.player.weapon.get_attacks():
                colour_print(str(index) + ". " + str(attack))
                index += 1

            colour_print(str(index) + ". Back out")

            attack_choice = int_input()

            if 0 < attack_choice < index:
                # checks if the selection is within range of the list of attacks

                chosen_attack = self.player.weapon.get_attacks()[attack_choice - 1]
                # loads the attack object corresponding to the player's selection
                base_damage = self.player.weapon.get_damage()
                # loads the base damage in the player's weapon
                attack_multiplier = chosen_attack.apply_attack()
                # loads the attack multiplier corresponding to the player's selection
                damage = int(base_damage * attack_multiplier * self.attack_amplification)
                # calculates the damage dealt to the enemy by multiplying the variables

                if str(chosen_attack.get_buff()):

                    self.hostile.add_buff(chosen_attack.get_buff())
                    colour_print("You have inflicted " + str(chosen_attack.get_buff()) + " on " + str(self.hostile))
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

                invalid_input()
                # prompts the user again if invalid input is given

    def choose_action(self):
        """brings up the action menu, displaying the player's actions"""

        while True:

            colour_print("Would you like to (H)eal, (A)mplify attack, (U)se a potion, (R)echarge, or (B)ack out")
            action_choice = str_input()

            # executes an action based on the player's choice, calling the action's respective methods
            if action_choice == 'h' or action_choice == 'heal':

                self.player.heal()

                break

            elif action_choice == 'a' or action_choice == 'amplify':

                self.attack_amplification += 1.5

                break

            elif action_choice == 'u' or action_choice == 'use':

                self.choose_potion()

                break

            elif action_choice == 'b' or action_choice == 'back':

                self.player_turn()

                break

            else:

                invalid_input()
                # prompts the user again if invalid input is given

    def choose_potion(self):
        """presents the player's potions"""

        while True:

            clear_screen()
            index = 1
            potions = self.player.get_potions()
            # stores a list of potions, pulled from the player's inventory

            for potion in potions:
                colour_print(str(index) + ". " + str(potion))
                index += 1

            colour_print(str(index) + ". Back out")

            potion_choice = int_input()
            potion = potions[potion_choice]

            if 0 < potion_choice < index:
                # checks if the selection is within range of the list of potions

                self.player.add_buff(potion.get_buff())
                self.player.remove_item_from_inventory(potion)
                # once the player uses the potion, it is removed from their inventory

            elif potion_choice == index:

                self.choose_action()
                # if the player backs out, the return the the choose action method

            else:

                invalid_input()
                # prompts the user again if invalid input is given

    def hostile_turn(self):
        """starts the hostile's turn"""

        self.player.lose_health_from_attack(self.hostile.get_damage(), str(self.hostile))

    def change_difficulty_multiplier(self, difficulty_multiplier):

        self.difficulty_multiplier = difficulty_multiplier

    def spare_or_kill(self):
        """starts the spare of kill part of a battle, when a player chooses whether to spare or kill an hostile"""

        while True:

            colour_print("(S)PARE or (K)ILL")
            spare_or_kill_choice = str_input()

            # starts the player object's respective methods based on the player's choice
            if spare_or_kill_choice == 's' or spare_or_kill_choice == 'spare':

                self.player.spare()
                time.sleep(3)
                self.wilderness()

            elif spare_or_kill_choice == 'k' or spare_or_kill_choice == 'kill':

                self.player.kill()
                time.sleep(3)
                self.wilderness()

            else:

                invalid_input()
                # prompts the user again if invalid input is given

    def unpack_tiles(self):
        """unpacks tile attributes from JSON file and creates a list of objects with those attributes"""

        with open('tiles.json') as t:
            tile_attribute_list = json.load(t)

        for tile in tile_attribute_list:
            self.tile_list.append(Tile(tile['x'], tile['y'], tile['biome'], tile['composition'], tile['item_key']))

    def get_attribute_dictionary(self):
        """returns the gamesave's attributes in a dictionary format to be saved into JSON"""

        attribute_dictionary = {
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

    def get_player(self):

        return self.player

    def get_difficulty_multiplier(self):

        return self.difficulty_multiplier

    def get_village_coordinates(self):

        return self.village_coordinates

    def get_x_size(self):

        return self.x_size

    def get_y_size(self):

        return self.y_size
