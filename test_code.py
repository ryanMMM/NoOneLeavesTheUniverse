from constant_objects import *


print(weapon_object_dictionary['stapler_rifle'].display_details())
print(attack_object_dictionary['cursed_trident'][0].display_details())
print(armour_object_dictionary['ice']['helmet'].display_details())
print(armour_object_dictionary['ice']['chestplate'].display_details())
print(armour_object_dictionary['ice']['boots'].display_details())
print(boss_object_dictionary['giant_boss'].display_battle_stats())
print(hostile_object_dictionary['grass_lands'][0].display_battle_stats())
print(buff_object_dictionary['poison_1'].display_details())
print(potion_object_dictionary['strong_regeneration_potion'].display_details())


"""from weapon import Weapon

my_weapon = Weapon()

for i in range(5):

    my_weapon.reforge()
    print(my_weapon.get_details())
"""
