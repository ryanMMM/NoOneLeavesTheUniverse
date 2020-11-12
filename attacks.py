import random
from buff import Buff


class Attack:

    def __init__(self, name='', multiplier=1, variance=0.2, buff=Buff()):

        self.name = name
        self.buff = buff
        self.multiplier = multiplier
        self.variance = variance

    def __str__(self):

        return self.name

    def apply_attack(self):
        """returns the randomized multiplier"""

        return round(self.multiplier * random.random(1 - self.variance, 1 + self.variance))

    def get_buff(self):

        return self.buff

    def get_multiplier(self):

        return self.multiplier

    def get_variance(self):

        return self.variance
