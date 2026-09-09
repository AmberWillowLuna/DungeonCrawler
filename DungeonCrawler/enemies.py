import Cards

def shuffle(lst):
    import random
    shuffled_lst = lst[:]
    random.shuffle(shuffled_lst)
    return shuffled_lst

class enemy:
    def __init__(self, name, description, hp, hand, DungeonName, level):
        self.name = name
        self.description = description
        self.hp = hp
        self.hand = hand  # List of card objects
        self.DungeonName = DungeonName
        self.level = level


    def ShuffleHand(self):
        curHand=self.hand
        #make random order of cards in hand
        self.hand = shuffle(curHand)

    def take_damage(self, damage):
        self.hp -= damage
        print(f"{self.name} took {damage} damage! Life points: {self.hp}")
        if self.hp < 0:
            self.hp = 0
            # Logic for when the enemy is defeated would go here
            print(f"{self.name} has been defeated!")


class Goblin(enemy):
    def __init__(self):
        super().__init__("Goblin", "A small, green, mischievous creature.", 3, [Cards.Knife(), Cards.LightAxe(), Cards.Nothing()], "Orc's dungeon", 1)

class Orc(enemy):
    def __init__(self):
        super().__init__("Orc", "Grey mischievous creature.", 4, [Cards.Dagger(), Cards.ShoulderPlate(), Cards.LightAxe()], "Orc's dungeon", 2)

class ArmoredOrc(enemy):
    def __init__(self):
        super().__init__("Armored Orc", "A grey orc with a chainmail.", 4, [Cards.LightAxe(), Cards.LightAxe(), Cards.ChainMail()], "Orc's dungeon", 3)

class Ogre(enemy):
    def __init__(self):
        super().__init__("Ogre", "Huge green furry mischievous creature.", 6, [Cards.Club(), Cards.Nothing(), Cards.Nothing()], "Orc's dungeon", 4)

class OrcWizard(enemy):
    def __init__(self):
        super().__init__("Orc Wizard", "A powerful mystical creature.", 3, [Cards.Knife(), Cards.LightAxe(), Cards.Nothing()], "Orc's dungeon", 5)