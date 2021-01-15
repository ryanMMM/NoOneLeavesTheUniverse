class Buff:
    """buffs are effects that can be administered to the player or enemy during battle, i.e. increased defense"""

    def __init__(self, name='', effect='', effectiveness=1, duration=3):

        self.name = name
        self.effect = effect
        self.effectiveness = effectiveness
        self.duration = duration

    def __str__(self):

        return self.name

    def display_details(self):

        details = self.name
        details += ":\nEffect: " + self.effect
        details += "\nDuration: " + str(self.duration)

        return details

    def get_effect(self):

        return self.effect

    def get_effectiveness(self):

        return self.effectiveness

    def get_duration(self):

        return self.duration

    def apply_buff(self):
        """decrements the duration by 1 after the buff has been applied for one round"""

        self.duration -= 1
