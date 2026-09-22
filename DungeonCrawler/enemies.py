import Cards
import os
from random import shuffle
import pygame
import button
import SettingHelp


def shuffle(lst):
    import random
    shuffled_lst = lst[:]
    random.shuffle(shuffled_lst)
    return shuffled_lst

def Fibbonaci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return Fibbonaci(n - 1) + Fibbonaci(n - 2)

class enemy:
    def __init__(self, name, description, hp, hand, DungeonName, level):
        self.name = name
        self.description = description
        self.hp = hp
        self.maxhp = hp
        self.et = "e"
        self.hand = hand  # List of card objects
        scale = SettingHelp.get_scale()
        self.lootTable = hand
        self.field = []
        self.DungeonName = DungeonName
        self.level = level
        self.prize = Fibbonaci(level+3)
        self.icon = self._load_icon()
        self.type="enemy"
        self.lootChance=2
        self.HandButtons = [
            button.CardButton(690*scale, 550*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(910*scale, 550*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1130*scale, 550*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing")   
            ]

    def _load_icon(self, size=None):
        """Load assets/{name}.png as the enemy's display icon."""
        image_path = os.path.join("assets", f"{self.name}.png")
        if os.path.exists(image_path):
            img = pygame.image.load(image_path).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            return img
        else:
            print(f"Warning: Enemy icon not found at {image_path}")
            return None

    def ShuffleHand(self):
        curHand=self.hand
        #make random order of cards in hand
        self.hand = shuffle(curHand)

    def heal(self, amount):
        self.hp += amount
        if self.hp>self.maxhp:
            self.hp = self.maxhp

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def sync_hand(self):
        for i in range(min(len(self.HandButtons), len(self.hand))):
            self.HandButtons[i].set_card(self.hand[i])

    def _build_enemy_display(self):
        """Build read-only CardButtons to show the enemy's hand, laid out in a row."""
        scale = SettingHelp.get_scale()
        buttons = []
        start_x = 680 * scale
        spacing = 220 * scale
        y = 240 * scale

        for i, card in enumerate(self.hand):
            cb = button.CardButton(
                start_x + i * spacing, y,
                card.name, (200, 200, 200), (150, 150, 150),
                card, card_type=card.card_type
            )
            buttons.append(cb)
        return buttons


class Goblin(enemy):
    def __init__(self):
        super().__init__("Goblin", "A small, green, mischievous creature.", 3, [Cards.Knife(), Cards.LightAxe(), Cards.Nothing()], "Orc's dungeon", 1)

class Orc(enemy):
    def __init__(self):
        super().__init__("Orc", "Grey mischievous creature.", 4, [Cards.Dagger(), Cards.ShoulderPlate(), Cards.LightAxe()], "Orc's dungeon", 2)

class ArmoredOrc(enemy):
    def __init__(self):
        super().__init__("Armored Orc", "A grey orc with a chainmail.", 4, [Cards.Sword(), Cards.LightAxe(), Cards.ChainMail()], "Orc's dungeon", 3)

class Ogre(enemy):
    def __init__(self):
        super().__init__("Ogre", "Huge green furry mischievous creature.", 6, [Cards.Club(), Cards.Nothing(), Cards.Nothing()], "Orc's dungeon", 4)
        self.lootTable = [Cards.Club(), Cards.Club(), Cards.Nothing()]
        self.lootChance = 1


class OrcWizard(enemy):
    def __init__(self):
        super().__init__("Orc Wizard", "A powerful mystical creature.", 5, [Cards.Spear(), Cards.ChainMail(), Cards.MagicHat()], "Orc's dungeon", 5)
        self.lootTable = [Cards.MagicHat(), Cards.MagicHat(), Cards.MagicHat()]
        self.lootChance = 1

class Slime(enemy):
        def __init__(self):
            super().__init__("slime", "A goo that seems to be agresive", 3, [Cards.Dagger(), Cards.Arrow(), Cards.Nothing()], "Misty dungeon", 1)

class Skeleton(enemy):
        def __init__(self):
            super().__init__("Skeleton", "Archer that looks like death", 4, [Cards.Bow(), Cards.Arrow(), Cards.Nothing()], "Misty dungeon", 2)

class DarkCreature(enemy):
        def __init__(self):
            super().__init__("DarkCreature", "Gives nightmares if you look too much at him", 5, [Cards.Halbard(), Cards.ShoulderPlate(), Cards.ChainMail()], "Misty dungeon", 3)

class Ghoul(enemy):
        def __init__(self):
            super().__init__("Ghoul", "Very dangerous spirit", 5, [Cards.Spear(), Cards.LightAxe(), Cards.Shield()], "Misty dungeon", 4)

class MistyGhost(enemy):
        def __init__(self):
            super().__init__("MistyGhost", "Agressive spirit of this dungeon", 7, [Cards.HealingAmulet(), Cards.Crown(), Cards.LongSword()], "Misty dungeon", 5)



class Librarian(enemy):
        def __init__(self):
            super().__init__("librarian", 
                             "Seems like a smart dude with books", 
                             5, 
                             [Cards.SpellBook(), Cards.Boomerang(), Cards.SpellShield()], 
                             "Library dungeon", 
                             1)

class DemonicEye(enemy):
        def __init__(self):
            super().__init__("Demonic eye", 
                             "Lewitating evil eye", 
                             6, 
                             [Cards.MagicEye(), Cards.SpellShield(), Cards.ShoulderPlate()], 
                             "Library dungeon", 
                             2)

class ThreeEyedBeast(enemy):
        def __init__(self):
            super().__init__("Three eyed beast", 
                             "Powerfull combination of beast and cyclop", 
                             7, 
                             [Cards.SpellBook(), Cards.Halbard(), Cards.Nothing()], 
                             "Library dungeon", 
                             3)


class TrophyHunter(enemy):
        def __init__(self):
            super().__init__("Trophy hunter", 
                             "Try-hard, willing to do a lot for gold", 
                             7, 
                             [Cards.SpellBook(), Cards.LongSword(), Cards.Boomerang()], 
                             "Library dungeon", 
                             4)
            self.lootTable = [Cards.SpellBook(), Cards.SpellBook(), Cards.Nothing()]
            self.lootChance = 1

class ArcaneGuardian(enemy):
        def __init__(self):
            super().__init__("Arcane guardian", 
                             "Increadibly powerful cultist like person", 
                             8, 
                             [Cards.SpellBook(), Cards.RitualKnife(), Cards.HealingAmulet()], 
                             "Library dungeon", 
                             5)
            self.lootTable = [Cards.RitualKnife(), Cards.RitualKnife(), Cards.RitualKnife()]
            self.lootChance = 1


class Gremlin(enemy):
        def __init__(self):
            super().__init__("Gremlin", 
                             "Small but grevious creature", 
                             4, 
                             [Cards.Nothing(), Cards.KnifePack(), Cards.Knife()], 
                             "Forest dungeon", 
                             1)

class Fungis(enemy):
        def __init__(self):
            super().__init__("Fungis", 
                             "Humanoid fungus", 
                             6, 
                             [Cards.Sword(), Cards.FishingRod(), Cards.PoisonousGas()], 
                             "Forest dungeon", 
                             2)

class Ent(enemy):
        def __init__(self):
            super().__init__("Ent", 
                             "Humanoid tree", 
                             9, 
                             [Cards.Sword(), Cards.Shield(), Cards.PoisonousGas()], 
                             "Forest dungeon", 
                             3)

class TreeOfLife(enemy):
        def __init__(self):
            super().__init__("Tree of life", 
                             "Huge tree pulsating with magic", 
                             12, 
                             [Cards.FishingRod(), Cards.GasBubble(), Cards.Spear()], 
                             "Forest dungeon", 
                             4)
            self.lootTable = [Cards.GasBubble(), Cards.GasBubble(), Cards.Nothing()]
            self.lootChance = 1


class ForestSpirit(enemy):
        def __init__(self):
            super().__init__("Forest Spirit", 
                             "Born from nature to rule the forest", 
                             10, 
                             [Cards.RitualKnife(), Cards.MagicMirror(), Cards.RitualKnife()], 
                             "Forest dungeon", 
                             4)
            self.lootTable = [Cards.MagicMirror(), Cards.MagicMirror(), Cards.MagicMirror()]
            self.lootChance = 1
