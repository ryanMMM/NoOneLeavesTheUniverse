import random
# TODO redesign difficulty multiplier

# import Weapons
# import Attacks


class Hostile:

    # 'Starting hostile', 'Goblin', 100, 20, 10, 10, 100, self.difficulty_multiplier
    def __init__(self, name='Starting hostile', species='Goblin', health=100, heal_amount=20,
                 damage=10, defence=10, coins=100, weakness='', alive=True):

        self.species = species
        # hostile's species
        self.name = name
        # hostile's name
        self.difficulty_multiplier = difficulty_multiplier
        self.default_health = health
        self.health = self.default_health
        self.heal_amount = heal_amount
        self.max_health = self.health
        # hostile's health
        # hostile's heal_amount: how much a hostile heals during a battle
        # hostile's max_health: the maximum amount of health a hostile can attain
        self.damage = damage
        self.defence = defence * self.difficulty_multiplier
        self.default_defence = self.defence
        self.base_defence = self.defence
        # self.weapon = Weapons.Weapon('Scythe', 10)
        self.default_coins = coins
        # the amount of coins a hostile drops when killed which is increased in harder difficulties
        self.weakness = weakness
        self.active_buffs = []
        self.alive = alive

    def __str__(self):

        return self.name

    def heal(self):
        """heals the hostile, replenishes their health"""

        self.add_health(self.heal_amount)

    def lose_health_from_attack(self, attack_damage, player_name):
        """causes the hostile to lose health, some is negative by the defence of the hostile"""

        health_lost = self.lose_health(attack_damage)
        print(player_name + " has dealt " + str(health_lost) + " to " + self.name)

    def add_health(self, health_add_amount):

        """adds the amount of health specified in the parameter to the player's health"""

        if self.health + health_add_amount < self.max_health:
            self.health += health_add_amount
            print(self.name + " has replenished " + str(health_add_amount) + " health")
        else:
            health_add_amount = self.max_health - self.health
            print(self.name + " has replenished " + str(health_add_amount) + " health")
            self.health = self.max_health
        if not health_add_amount:
            print("You are already at max health!")
        return health_add_amount

    def lose_health(self, health_lose_amount):
        """causes the hostile to lose an amount of health specified by the parameter"""

        health_lose_amount = (health_lose_amount - (health_lose_amount * (self.defence / 50)))
        if self.health - health_lose_amount > 0:
            self.health -= health_lose_amount
        else:
            health_lose_amount = self.health
            self.health = 0
            self.die()
        return health_lose_amount

    def apply_buffs(self):
        """loops through the hostile's buffs and applies all the effects
        and removes buffs that have finished their duration"""

        for buff in self.active_buffs:
            if buff.get_duration():
                if buff.get_effect() == 'block_defence':
                    print(self.name + "'s defence has been removed'")
                    self.defence = 0
                elif buff.get_effect() == 'regeneration':
                    self.add_health((self.heal_amount / 2) * buff.get_effectiveness())
                elif buff.get_effect() == 'poison':
                    self.lose_health(self.heal_amount * buff.get_effectiveness())
                buff.apply_buff()
            else:
                if buff.get_effect() == 'block_defence':
                    self.defence = self.default_defence
                self.remove_buff(buff)

    '''def get_range(self):
        """randomises distance of hostile from player"""

        # TODO add probability of being close
        range_chance = random.randint(1, 2)
        if range_chance == 1:
            self.range = 'close'
        if range_chance == 2:
            self.range = 'far' '''

    def die(self):

        self.alive = False

    def display_battle_stats(self):
        """display's enemy's statistics relevant to a battle"""

        battle_stats = "#" * 10 + " " + self.name.upper() + " " + "#" * 10 + "\n"
        battle_stats += self.name + "'s Health: " + str(self.health) + "\n"
        battle_stats += "#" * (22 + len(self.name.capitalize())) + "\n"
        return battle_stats

    def change_difficulty_multiplier(self, difficulty_multiplier):
        """changes the difficulty multiplier and impacts the relevant hostile attributes in accordance with the
        new difficulty multiplier"""

        self.difficulty_multiplier = difficulty_multiplier
        self.health = self.default_health * self.difficulty_multiplier
        self.coins = self.default_coins * self.difficulty_multiplier

    def add_buff(self, buff):

        self.active_buffs.append(buff)

    def remove_buff(self, buff):

        self.active_buffs.remove(buff)

    def administer_buff_from_player(self, buff):

        print("You have administered " + str(buff) + " to " + self.name)
        self.add_buff(buff)

    def get_damage(self):

        return self.damage

    def get_health(self):

        return self.health

    def speak(self):
        pass

    def attack(self):
        pass

    def get_coins(self):

        return self.default_coins

    def get_weakness(self):

        return self.weakness

    def is_alive(self):

        return self.alive
