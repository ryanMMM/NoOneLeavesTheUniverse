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
        details += ":\nDuration: " + str(self.duration)

    def get_effect(self):

        return self.effect

    def get_effectiveness(self):

        return self.effectiveness

    def get_duration(self):

        return self.duration


class DirectedBuff:

    def __init__(self, buff=Buff()):

        self.buff = buff
        self.duration_counter = self.buff.get_duration() + 1

    def apply_buff(self):
        """every round in a fight the duration of a buff is checked by this method, when it reaches 0, the buff stops"""

        self.duration_counter -= 1
        return self.duration_counter



