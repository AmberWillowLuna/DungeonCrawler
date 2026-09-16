'''

Trinkets ideas:

Ring of knowledge - u know what trap is ahead

ring of life - +1 max hp

enchanted ring of life - + 2 max hp

necklace of regeneration - +1 hp each room

The ring of the thief - +1 gold each room

Bracelet of the thief - +3 gold each room

necklace of time - can roll again for merchant in rooms

necklace of wisdom - you alwyas know what is in front room

bracelet of gambler - enemy has 20% chance NOT to shuffle hand - very op tbh


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
        player.max_hp += 1
        player.hp += 1  # Optionally heal the player as well

    def delete_effect(self, player):
        player.max_hp -= 1
        if player.hp > player.max_hp:
            player.hp = player.max_hp

class EnchantedRingOfLife(Trinket):
    def __init__(self):
        super().__init__("Enchanted Ring of Life", "Increases max HP by 2.")

    def apply_effect(self, player):
        player.max_hp += 2
        player.hp += 2  # Optionally heal the player as well

    def delete_effect(self, player):
        player.max_hp -= 2
        if player.hp > player.max_hp:
            player.hp = player.max_hp

class NecklaceOfRegeneration(Trinket):
    def __init__(self):
        super().__init__("Necklace of Regeneration", "Heals 1 HP each room.")

    def apply_effect(self, player):
        player.regeneration += 1  # Assuming player has a regeneration attribute

    def delete_effect(self, player):
        player.regeneration -= 1