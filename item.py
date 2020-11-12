from buff import Buff


class Item:
    """class of items, anything that isnt a weapon or armor that can be added to a player's inventory, e.g. potions"""

    def __init__(self, name, description):

        self.name = name
        self.type = 'item'
        self.description = description

    def __str__(self):

        return self.name

    def display_details(self):

        details = self.name
        details += ":\nDescription:" + self.description

        return details

    def get_type(self):

        return self.type


class Potion(Item):
    """potions store a buff that players can use in battle"""

    def __init__(self, name='', description='', buff=Buff(), cost=0):

        super().__init__(name, description)
        self.type = 'potion'
        self.buff = buff
        self.name = self.name
        self.cost = cost

    def get_buff(self):

        return self.buff

    def get_cost(self):

        return self.cost

    def display_details(self):

        details = self.name
        details += self.buff.display_details()

        return details


class Collectible(Item):
    """Collectibles are items that have value and can be sold"""

    def __init__(self, name='', description='', value=0):

        super().__init__(name, description)
        self.type = 'collectible'
        self.value = value

    def get_value(self):

        return self.value

    def display_details(self):

        details = self.name
        details += ":\nValue: " + str(self.value) + " coins\n"
        details += "Description: " + str(self.description)
