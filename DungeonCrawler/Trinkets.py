'''

Trinkets ideas:

Ring of knowledge - u know what trap is ahead v

ring of life - +1 max hp v

enchanted ring of life - + 3 max hp v

necklace of regeneration - +1 hp each room v

The ring of the thief - +2 gold each room v

Bracelet of the thief - +4 gold each room v

necklace of time - can roll again for merchant in rooms

necklace of wisdom - you alwyas know what is in front room



'''
class Trinket:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def apply_effect(self, player):
        '''Apply the effect of the trinket to the player'''
        pass  # To be implemented in subclasses

    def delete_effect(self, player):
        '''Remove the effect of the trinket from the player'''
        pass

class RingOfLife(Trinket):
    def __init__(self):
        super().__init__("Ring of Life", "Increases max HP by 1.")

    def apply_effect(self, player):
        player.maxHp += 1
        player.life_points += 1  # Optionally heal the player as well

    def delete_effect(self, player):
        player.maxHp -= 1
        if player.hp > player.maxHp:
            player.life_points = player.maxHp

class EnchantedRingOfLife(Trinket):
    def __init__(self):
        super().__init__("Enchanted Ring of Life", "Increases max HP by 2.")

    def apply_effect(self, player):
        player.maxHp += 3
        player.life_points += 3  # Optionally heal the player as well

    def delete_effect(self, player):
        player.maxHp -= 3
        if player.hp > player.maxHp:
            player.life_points = player.maxHp

class NecklaceOfRegeneration(Trinket):
    def __init__(self):
        super().__init__("Necklace of Regeneration", "Heals 1 HP each room.")

    def apply_effect(self, player):
        player.regeneration += 1  # Assuming player has a regeneration attribute

    def delete_effect(self, player):
        player.regeneration -= 1

class RingOfKnowledge(Trinket):
    def __init__(self):
        super().__init__("Ring of knowledge", "You learn when trap is not ahead")

    def apply_effect(self, player):
        player.wis = True  # Assuming player has a regeneration attribute

    def delete_effect(self, player):
        player.wis = False

class RingOfThief(Trinket):
    def __init__(self):
        super().__init__("Ring of thief", "You get extra 2 gold per room")

    def apply_effect(self, player):
        player.income +=2

    def delete_effect(self, player):
        player.income -= 2

class BraceletOfThief(Trinket):
    def __init__(self):
        super().__init__("Bracelet of thief", "You get extra 4 gold per room")

    def apply_effect(self, player):
        player.income +=4

    def delete_effect(self, player):
        player.income -= 4

class NecklaceOfTime(Trinket):
    def __init__(self):
        super().__init__("Necklace of time", "You can reroll the merchant drop one time")

    def apply_effect(self, player):
        player.timePerk =True

    def delete_effect(self, player):
        player.timePerk = False

class NecklaceOfWisdom(Trinket):
    def __init__(self):
        super().__init__("Necklace of wisdom", "You alwyas know what is in front room")

    def apply_effect(self, player):
        player.wisdom =True

    def delete_effect(self, player):
        player.wisdom = False


import random

Tier1 = [RingOfLife(), RingOfThief(), RingOfKnowledge(), NecklaceOfRegeneration()]
Tier2 = [EnchantedRingOfLife(), BraceletOfThief(), NecklaceOfTime(), NecklaceOfWisdom()]

# Shuffle and shrink Tier1 to 3 elements
random.shuffle(Tier1)
Tier1 = Tier1[:3]

# Shuffle and shrink Tier2 to 3 elements
random.shuffle(Tier2)
Tier2 = Tier2[:3]

# Combine Tier1 and Tier2 into Trinkets
Trinkets = Tier1 + Tier2