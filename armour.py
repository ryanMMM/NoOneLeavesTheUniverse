class Armour:

    def __init__(self, name, defence, armour_set, cost):
        self.name = name
        self.defence = defence
        # base defence points for an armour piece
        self.set = armour_set
        # set of armour, if all a player's armour pieces are the same group, they get a special set bonus
        self.slot = ''
        # slot of armour, where it is equipped by the player, i.e. head, chest, feet
        self.cost = cost

    def __str__(self):

        return self.name

    def get_defence(self):

        return self.defence

    def get_set(self):

        return self.set

    def get_slot(self):

        return self.slot

    def get_cost(self):

        return self.cost

    def display_details(self):

        details = self.name
        details += ":\nDefense points: " + str(self.defence)
        details += "\nCost" + str(self.cost)

        return details


class Helmet(Armour):

    def __init__(self, name='baseball cap', defence=3, armour_set='starting_clothes', cost=0):
        super().__init__(name, defence, armour_set, cost)
        self.slot = 'head'


class Chestplate(Armour):

    def __init__(self, name='yankees t-shirt', defence=5, armour_set='starting_clothes', cost=0):
        super().__init__(name,  defence, armour_set, cost)
        self.slot = 'chest'


class Boots(Armour):

    def __init__(self, name='converse sneakers', defence=2, armour_set='starting_clothes', cost=0):
        super().__init__(name,  defence, armour_set, cost)
        self.slot = 'feet'
