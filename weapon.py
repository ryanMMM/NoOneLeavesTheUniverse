import random

from attacks import Attack
from constant_attributes import condition_dictionary


class Weapon:

    def __init__(self, name='Stick', description='', damage=10, weapon_type='', cost=0, condition='sturdy',
                 attacks=[Attack(), Attack(), Attack()]):

        self.name = name
        # a weapon's name consists of it's condition and regular name, e.g. 'Sturdy Sword'
        self.description = description
        self.condition = condition
        # condition effects the weapon's damage and other attributes, condition is defaulted to sturdy
        self.default_damage = damage
        self.damage = int(self.default_damage * condition_dictionary[self.condition]['damage_multiplier'])
        # damage changes depending on condition, but it is defaulted at the default damage
        # weapon's default damage is set by the parameter damage
        self.weapon_type = weapon_type
        self.cost = cost
        # how much it costs to purchase the weapon
        self.attacks = attacks
        # list of attacks that the weapon can perform
        self.critical_chance = condition_dictionary[self.condition]['critical_chance']
        self.critical_multiplier = condition_dictionary[self.condition]['critical_multiplier']
        # critical chance is the probability of achieving a stronger attack multiplied by the critical multiplier

    def __str__(self):

        return self.name

    def random_attack_choice(self):
        """chooses a random attack from the weapon's list of attacks"""

        random_attack = random.choice(self.attacks)

        return random_attack

    def reforge(self):
        """randomly changes the condition of a weapon with set chances of getting each condition,
        this method is used when a player reforges their weapon at the forgery"""

        reforge_chance = random.randint(1, 10)

        if reforge_chance <= 2:

            self.condition = "puny"

        elif reforge_chance <= 5:

            self.condition = "sturdy"

        elif reforge_chance <= 8:

            self.condition = "hardened"

        else:

            self.condition = "draconic"

        self.damage = int(self.default_damage * condition_dictionary[self.condition]['damage_multiplier'])
        self.critical_chance = condition_dictionary[self.condition]['critical_chance']
        self.critical_multiplier = condition_dictionary[self.condition]['critical_multiplier']

    def get_attribute_dictionary(self):
        """returns attributes in a dictionary format to be saved into JSON"""

        attribute_dictionary = {
            'name': self.name,
            'description': self.description,
            'default_damage': self.default_damage,
            'weapon_type': self.weapon_type,
            'cost': self.cost,
            'condition': self.condition
        }

        return attribute_dictionary

    def get_details(self):

        details = self.name
        details += ":\nDamage: " + str(self.damage)
        details += "\nCondition: " + self.condition
        details += "\nCritical hit chance: " + str(self.critical_chance)
        details += "\nCritical hit damage: " + str(self.critical_multiplier * self.damage)

        return details

    def get_default_damage(self):

        return self.default_damage

    def get_damage(self):

        return self.damage

    def get_description(self):

        return self.description

    def get_weapon_type(self):

        return self.weapon_type

    def get_cost(self):

        return self.cost

    def get_condition(self):

        return self.condition

    def get_attacks(self):

        return self.attacks

    def get_critical_chance(self):

        return self.critical_chance

    def get_critical_multiplier(self):

        return self.critical_multiplier
