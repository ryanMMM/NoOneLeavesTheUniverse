# stores attributes of all weapons in the game
weapon_attribute_dictionary = {

    "starter_weapon":
        {
            "name": "Wooden Stick",
            "description": "just a wooden stick",
            "default_damage": 25,
            "weapon_type": "starter",
            "cost": 0
        },
    "stapler_rifle":
        {
            "name": "Staple Rifle",
            "description": "A deadly bolt action staple gun (effective against office hostiles)",
            "default_damage": 75,
            "weapon_type": "stapler",
            "cost": 100
        },
    "fire_breather":
        {
            "name": "Fire Breather",
            "description": "A dragon, glue, some plastic! (effective against ice hostiles)",
            "default_damage": 50,
            "weapon_type": "fire",
            "cost": 50
        },
    "cursed_trident":
        {
            "name": "Cursed Trident",
            "description": "Hand-crafted from tormented souls of the underworld (effective against hallowed hostiles)",
            "default_damage": 100,
            "weapon_type": "unholy",
            "cost": 200
        },
    "progenitor_steel_blade":
        {
            "name": "Progenitor's Blade",
            "description": "A steel blade forged by the progenitors of the UNIVERSE (effective against goblin enemies)",
            "default_damage": 125,
            "weapon_type": "steel",
            "cost": 250
        },
    "universe_blade":
        {
            "name": "Blade of the UNIVERSE",
            "description": "This blade holds the soul of the UNIVERSE",
            "default_damage": 300,
            "weapon_type": "",
            "cost": 500
        }
}

# stores attributes of all attacks in the game with reference to the weapon they belong to
attack_attribute_dictionary = {

    "starter_weapon":
        [
            {
                "name": "Poke",
                "multiplier": 1.2,
                "variance": 0.4,
                "buff": ""
            },
            {
                "name": "Poison Ivy",
                "multiplier": 0.8,
                "variance": 0.2,
                "buff": "poison_1"
            }
        ],
    "stapler_rifle":
        [
            {
                "name": "High Velocity Staple Shot (high damage)",
                "multiplier": 1.2,
                "variance": 0.4,
                "buff": ""
            },
            {
                "name": "Poisonous Staple Shot (poison)",
                "multiplier": 1,
                "variance": 0.2,
                "buff": "poison_1"
            },
        ],
    "fire_breather":
        [
            {
                "name": "Dragon's Scorch (high damage)",
                "multiplier": 1.4,
                "variance": 0.4,
                "buff": ""
            },
            {
                "name": "Cursed Flame (poison)",
                "multiplier": 0.8,
                "variance": 0.1,
                "buff": "poison_2"
            }
        ],
    "cursed_trident":
        [
            {
                "name": "Piercing strike (high damage)",
                "multiplier": 1.5,
                "variance": 0.6,
                "buff": ""
            },
            {
                "name": "Unholy Slash (break defense)",
                "multiplier": 0.6,
                "variance": 0,
                "buff": "block_defense"
            }
        ],
    "progenitor_steel_blade":
        [
            {
                "name": "PAIN (high damage)",
                "multiplier": 1.2,
                "variance": 0.3,
                "buff": ""
            },
            {
                "name": "PARASITE (break defense)",
                "multiplier": 0.8,
                "variance": 0.2,
                "buff": "break_defense"
            },
            {
                "name": "LOVE (heal your enemy)",
                "multiplier": -0.2,
                "variance": 0,
                "buff": ""
            }
        ],
    "universe_blade":
        [
            {
                "name": "6Nba#R#*",
                "multiplier": 1.5,
                "variance": 0.3,
                "buff": ""
            },
            {
                "name": "#*$U)@$)@",
                "multiplier": 1,
                "variance": 0.4,
                "buff": "break_defense"
            },
            {
                "name": "QWERTYUIOP",
                "multiplier": 0.9,
                "variance": 0.5,
                "buff": "poison_3"
            }
        ],
}

# stores attributes of all armour pieces in the game with respect to the armour class they belong to
armour_attribute_dictionary = {

    "ice":
        {
            "helmet":
                {
                    "name": "Frozen Mask",
                    "defense": 10,
                    "armour_set": "ice",
                    "cost": 30

                },
            "chestplate":
                {
                    "name": "Frozen Chestplate",
                    "defense": 15,
                    "armour_set": "ice",
                    "cost": 50

                },
            "boots":
                {
                    "name": "Frozen Mask",
                    "defense": 5,
                    "armour_set": "ice",
                    "cost": 20
                }
        },
    "goblin":
        {
            "helmet":
                {
                    "name": "Goblin Helm",
                    "defense": 20,
                    "armour_set": "goblin",
                    "cost": 70

                },
            "chestplate":
                {
                    "name": "Goblin Chainmail",
                    "defense": 25,
                    "armour_set": "goblin",
                    "cost": 130

                },
            "boots":
                {
                    "name": "Goblin Shoes",
                    "defense": 10,
                    "armour_set": "goblin",
                    "cost": 50
                }
        },
    "hallowed":
        {
            "helmet":
                {
                    "name": "Hallowed Horns",
                    "defense": 15,
                    "armour_set": "hallowed",
                    "cost": 60

                },
            "chestplate":
                {
                    "name": "Hallowed Robe",
                    "defense": 20,
                    "armour_set": "hallowed",
                    "cost": 120

                },
            "boots":
                {
                    "name": "Hallowed Sandals",
                    "defense": 5,
                    "armour_set": "hallowed",
                    "cost": 40
                }
        },
    "office_armour":
        {
            "helmet":
                {
                    "name": "Office Hat",
                    "defense": 15,
                    "armour_set": "office",
                    "cost": 30

                },
            "chestplate":
                {
                    "name": "Office Suit",
                    "defense": 20,
                    "armour_set": "office",
                    "cost": 100

                },
            "boots":
                {
                    "name": "Office Shoes",
                    "defense": 5,
                    "armour_set": "office",
                    "cost": 20
                }
        },
    "universe_armour":
        {
            "helmet":
                {
                    "name": "UNIVERSE Hat",
                    "defense": 25,
                    "armour_set": "universe",
                    "cost": 200

                },
            "chestplate":
                {
                    "name": "UNIVERSE Shirt",
                    "defense": 30,
                    "armour_set": "universe",
                    "cost": 300

                },
            "boots":
                {
                    "name": "UNIVERSE Boots",
                    "defense": 15,
                    "armour_set": "universe",
                    "cost": 100
                }
        },
}

# stores the attributes of all the boss hostiles in the game
boss_attribute_dictionary = {

    "giant_boss":
        {
            "name": "The Chained Ice Giant",
            "species": "ice",
            "health": 500,
            "heal_amount": 50,
            "damage": 20,
            "defense": 10,
            "coins": 1000,
            "difficulty_multiplier": 1,
            "weakness": "fire"
        },
    "grave_boss":
        {
            "name": "The Void",
            "species": "standard",
            "health": 3000,
            "heal_amount": 0,
            "damage": 50,
            "defense": 0,
            "coins": 3000,
            "difficulty_multiplier": 1,
            "weakness": ""
        },
    "janice_boss":
        {
            "name": "Janice from the HR Department",
            "species": "office_demon",
            "health": 750,
            "heal_amount": 50,
            "damage": 40,
            "defense": 5,
            "coins": 2000,
            "difficulty_multiplier": 1,
            "weakness": "stapler"
        },
    "queen_boss":
        {
            "name": "Leah, the Hallowed Queen",
            "species": "hallowed",
            "health": 1500,
            "heal_amount": 50,
            "damage": 30,
            "defense": 5,
            "coins": 2000,
            "difficulty_multiplier": 1,
            "weakness": "unholy"
        },
    "barry_goblin_boss":
        {
            "name": "Barry Goblin the Lucky",
            "species": "goblin",
            "health": 1500,
            "heal_amount": 50,
            "damage": 60,
            "defense": 5,
            "coins": 2000,
            "difficulty_multiplier": 1,
            "weakness": "steel"
        }
}

# stores the attributes of all the random encounter hostiles in the game with reference to the biome they live in
hostile_attribute_dictionary = {

    "grass_lands":
        [
            {
                "name": "warrior",
                "species": "standard",
                "health": 90,
                "heal_amount": 20,
                "damage": 10,
                "defense": 0,
                "coins": 100,
                "difficulty_multiplier": 1,
                "weakness": ""
            },
            {
                "name": "bandit",
                "species": "standard",
                "health": 80,
                "heal_amount": 20,
                "damage": 15,
                "defense": 0,
                "coins": 120,
                "difficulty_multiplier": 1,
                "weakness": ""
            }
        ],
    "offices":
        [
            {
                "name": "accountant",
                "species": "office_demon",
                "health": 150,
                "heal_amount": 30,
                "damage": 10,
                "defense": 10,
                "coins": 100,
                "difficulty_multiplier": 1,
                "weakness": "stapler"
            },
            {
                "name": "intern",
                "species": "office_demon",
                "health": 120,
                "heal_amount": 20,
                "damage": 15,
                "defense": 5,
                "coins": 120,
                "difficulty_multiplier": 1,
                "weakness": "stapler"
            }
        ],
    "lava_lake":
        [
            {
                "name": "imp",
                "species": "magma_creature",
                "health": 150,
                "heal_amount": 30,
                "damage": 10,
                "defense": 10,
                "coins": 100,
                "difficulty_multiplier": 1,
                "weakness": "aqua"
            },
            {
                "name": "demon",
                "species": "magma_creature",
                "health": 120,
                "heal_amount": 20,
                "damage": 20,
                "defense": 0,
                "coins": 120,
                "difficulty_multiplier": 1,
                "weakness": "aqua"
            }
        ],
    "tundra":
        [
            {
                "name": "reaper",
                "species": "ice",
                "health": 150,
                "heal_amount": 20,
                "damage": 10,
                "defense": 10,
                "coins": 100,
                "difficulty_multiplier": 1,
                "weakness": "fire"
            },
            {
                "name": "polar bear",
                "species": "ice",
                "health": 120,
                "heal_amount": 30,
                "damage": 15,
                "defense": 10,
                "coins": 120,
                "difficulty_multiplier": 1,
                "weakness": "fire"
            }
        ],
    "goblin_forest":
        [
            {
                "name": "gremlin",
                "species": "goblin",
                "health": 150,
                "heal_amount": 20,
                "damage": 10,
                "defense": 10,
                "coins": 100,
                "difficulty_multiplier": 1,
                "weakness": "steel"
            },
            {
                "name": "thief",
                "species": "goblin",
                "health": 120,
                "heal_amount": 30,
                "damage": 15,
                "defense": 10,
                "coins": 120,
                "difficulty_multiplier": 1,
                "weakness": "steel"
            }
        ],
    "sycamore_forest":
        [
            {
                "name": "fairy",
                "species": "hallowed",
                "health": 150,
                "heal_amount": 20,
                "damage": 10,
                "defense": 10,
                "coins": 100,
                "difficulty_multiplier": 1,
                "weakness": "unholy"
            },
            {
                "name": "pegasus",
                "species": "hallowed",
                "health": 120,
                "heal_amount": 30,
                "damage": 15,
                "defense": 10,
                "coins": 120,
                "difficulty_multiplier": 1,
                "weakness": "unholy"
            }
        ]
}

# stores all the changes that each condition will apply to a weapon
condition_dictionary = {

    "puny":
        {
            "damage_multiplier": 0.8,
            "critical_chance": 40,
            "critical_multiplier": 1.2
        },
    "sturdy":
        {
            "damage_multiplier": 1,
            "critical_chance": 30,
            "critical_multiplier": 1.4
        },
    "hardened":
        {
            "damage_multiplier": 1.2,
            "critical_chance": 20,
            "critical_multiplier": 1.6
        },
    "draconic":
        {
            "damage_multiplier": 1.4,
            "critical_chance": 10,
            "critical_multiplier": 1.8
        }
}

# stores the attributes of all the buffs
buff_attribute_dictionary = {

    "poison_1":
        {
            "name": "Weak Poison",
            "effect": "poison",
            "effectiveness": 20,
            "duration": 3
        },
    "poison_2":
        {
            "name": "Mild Poison",
            "effect": "poison",
            "effectiveness": 40,
            "duration": 3
        },
    "poison_3":
        {
            "name": "Weak Poison",
            "effect": "poison",
            "effectiveness": 60,
            "duration": 3
        },
    "block_healing":
        {
            "name": "Heal Blocker",
            "effect": "block_healing",
            "effectiveness": 1,
            "duration": 3
        },
    "block_defense":
        {
            "name": "Defense Blocker",
            "effect": "block_defense",
            "effectiveness": 1,
            "duration": 3
        },
    "regeneration_1":
        {
            "name": "Weak Regeneration",
            "effect": "regeneration",
            "effectiveness": 20,
            "duration": 3
        },
    "regeneration_2":
        {
            "name": "Mild Regeneration",
            "effect": "regeneration",
            "effectiveness": 40,
            "duration": 3
        },
    "regeneration_3":
        {
            "name": "Strong Regeneration",
            "effect": "regeneration",
            "effectiveness": 60,
            "duration": 3
        }
}

# stores the attributes of all the potions
potion_attribute_dictionary = {

    "weak_regeneration_potion":
        {
            "name": "Weak Regeneration Potion",
            "description": "Tasty and healthy potion to enjoy on a nice summer day",
            "buff": "regeneration_1",
            "cost": 20
        },
    "mild_regeneration_potion":
        {
            "name": "Mild Regeneration Potion",
            "description": "Tasty and healthy potion to enjoy on a nice summer day",
            "buff": "regeneration_2",
            "cost": 40
        },
    "strong_regeneration_potion":
        {
            "name": "Strong Regeneration Potion",
            "description": "Tasty and healthy potion to enjoy on a nice summer day",
            "buff": "regeneration_3",
            "cost": 60
        }
}

# stores the contents of all the chests in the game
chest_contents_dictionary = {

    "chest_1":
        {
            "weapon": "progenitors_steel_blade",
            "potion": "strong_regeneration_potion",
            "collectible": ""
        },
    "chest_2":
        {
            "weapon": "universe_blade",
            "potion": "strong_regeneration_potion",
            "collectible": ""
        }
}

# stores the player attribute multipliers in each level of player upgrades
upgrade_progression_dictionary = {

    "health":
        [
            1.25,
            1.5,
            1.75,
            2
        ],
    "charge":
        [
            1,
            2,
            3
        ],
    "attack_amplification":
        [
            1,
            1.5,
            2
        ]
}

# stores the costs of each player attribute upgrade
upgrade_cost_dictionary = {

    "health": 50,
    "charge": 30,
    "attack_amplification": 40,
}

# stores the dialogue of each shopkeeper with reference to how they react to repuation levels
shop_dialogue = {
    
    "forgery":
        {
            "high_reputation":
                [
                    "Please come again if you ever need anything!",
                    "Thanks for dropping by!"
                ],
            "low_reputation":
                [
                    "Please don't come back",
                    "Go forge your weapons somewhere else next time"
                ]
        },
    "potion_shop":
        {
            "high_reputation":
                [
                    "We've got the best potions in the UNIVERSE, tell your friends!",
                    "Please come back soon, I love your coins"
                ],
            "low_reputation":
                [
                    "You stink up the place, please wear some perfume upon your next visit",
                    "If it wasn't for your money, I'd tell you to leave"
                ]
        }
}


landmark_collectible_attribute_dictionary = {
    "progenitor_statue":
        {
            "name": "The Progenitor's Statue",
            "description": "The remains of the old idols, buried away centuries ago",
            "value": 200
        },
    "goblin_amulet":
        {
            "name": "The Goblin Amulet",
            "description": "a mysterious amulet forged by an ancient civilization of goblins",
            "value": 300
        },
    "queen_bracelet":
        {
            "name": "The Hallowed Queen's Bracelet",
            "description": "A bracelet gifted to the queen of the hallowed by the progenitors",
            "value": 500
        },
    "universe_stone":
        {
            "name": "The UNIVERSE Stone",
            "description": "A fragment of another UNIVERSE that collided with your abode",
            "value": 800
        },
    "jakub_brain":
        {
            "name": "Jakub's Brain",
            "description": "Just a brain",
            "value": 100
        },
    "dodo_wacom_pad":
        {
            "name": "Dodo's Wacom Pad",
            "description": "Filled with Dodo's blood, sweat, and tears",
            "value": 100
        },
    "omar":
        {
            "name": "Omar",
            "description": "Omar's dead cold corpse",
            "value": 50
        },
}



treasure_collectible_attribute_dictionary = {
    "platinum_coin":
        {
            "name": "Platinum Coin",
            "description": "An ancient yet valuable currency",
            "value": 120
        },
    "gold_coin":
        {
            "name": "Gold Coin",
            "description": "A currency from another UNIVERSE",
            "value": 100
        },
    "arman_laptop":
        {
            "name": "Arman's Laptop",
            "description": "Filled with unread PDFs on computational linguistics",
            "value": 50
        },
    "old_shoe":
        {
            "name": "An old shoe",
            "description": "smells off",
            "value": 10
        }
}
