
import re

# attacks
BLUDGEON = 0
FIRE = 1
RADIATION = 2
COLD = 3
SLASH = 4

#{"team": None, "units": 0, "hitpoints": 0, "weaknesses": [], "immunity_from": [], "attackpower": 0, "attacktype": None, "initiative": 0}

class Platoon:
    def __init__(self, dictionary):
        self.dictionary = dictionary 

    def get_effective_power(self):
        return self.dictionary["num_units"] * self.dictionary["attackpower"]

    def apply_damage(self, dmg):
        self.dictionary['num_units'] -= dmg // self.dictionary['hp'] 
    
    def is_dead(self):
        return self.dictionary['num_units'] == 0

    def get_potential_dmg(self, platoon):
    #def get_potential_dmg(self, attacktype, num_units, attackpower):
        if platoon['attacktype'] in self.dictionary['immunity_from']:
            return 0

        isweak = platoon['attacktype'] in self.dictionary['weaknesses']

        return (1+isweak)*platoon['num_units']*platoon['attackpower']

    def __get__(self, e):
        assert e in self.dictionary
        return self.dictionary[e]

def make_group(team, num_units, hp, weaknesses, immunity_from, attackpower, attacktype, initiative):
    ret = dict({"team": team, "units": num_units, "hitpoints": hp, "weaknesses": None, "immunity_from": None, "attackpower": attackpower, "attacktype": None, "initiative": initiative})
    ret["weaknesses"] = list(weaknesses)
    ret["immunity_from"] = list(immunity_from)
    ret["attacktype"] = attacktype

    return ret

immune_bois = [
    make_group("immunesystem", 3321, 6178, [], [BLUDGEON, FIRE], 18, BLUDGEON, 20),
    make_group("immunesystem", 4228, 9720, [BLUDGEON], [], 21, FIRE, 10),
    make_group("immunesystem", 1181, 5833, [BLUDGEON], [SLASH, COLD], 44, COLD, 6),
    make_group("immunesystem", 89, 6501, [SLASH, BLUDGEON], [], 715, FIRE, 1),
    make_group("immunesystem", 660, 5241, [SLASH], [], 75, RADIATION, 11),
    make_group("immunesystem", 3393, 3576, [FIRE], [COLD, RADIATION], 9, FIRE, 3),
    make_group("immunesystem", 2232, 5558, [], [SLASH], 21, FIRE, 7),
    make_group("immunesystem", 4861, 13218, [SLASH, FIRE], [], 20, FIRE, 14),
    make_group("immunesystem", 3102, 7657, [SLASH], [COLD], 24, RADIATION, 17),
    make_group("immunesystem", 8186, 5664, [SLASH], [], 6, BLUDGEON, 9)
        ]

infection_bois = [
    make_group("infection", 931, 32672, [SLASH], [], 67, SLASH, 13),
    make_group("infection", 1328, 40275, [], [FIRE, RADIATION], 54, BLUDGEON, 5),
    make_group("infection", 5620, 43866, [RADIATION, FIRE], [], 12, COLD, 18),
    make_group("infection", 3596, 44288, [], [BLUDGEON, FIRE], 22, SLASH, 8),
    make_group("infection", 85, 15282, [COLD, FIRE], [], 272, FIRE, 15),
    make_group("infection", 129, 49924, [BLUDGEON], [], 681, RADIATION, 4),
    make_group("infection", 5861, 24179, [SLASH], [], 8, COLD, 16),
    make_group("infection", 3132, 5961, [], [RADIATION], 3, SLASH, 19),
    make_group("infection", 1336, 56700, [BLUDGEON, RADIATION], [], 69, RADIATION, 12),
    make_group("infection", 2611, 28641, [], [], 21, FIRE, 2)
    ]


while len(immune_bois) != 0 and len(infection_bois) == 0:
    # select target
