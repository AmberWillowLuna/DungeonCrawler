import random
import Cards

class Shop:
    def __init__(self, curD):
        self.curD = curD
        self.weapons = []
        self.armors = []
        self.healing = []
        self.potions = []

        if curD == "Orc's dungeon":
            self.weapons = [
                Cards.LongSword(),
                Cards.Halbard(),
                Cards.LightAxe(),
                Cards.Dagger(),
                Cards.Knife(),
                Cards.Bow(),
                Cards.Boomerang()
            ]
            self.armors = [
                Cards.ChainMail(),
                Cards.Shield(),
                Cards.Helmet(),
                Cards.ShoulderPlate(),
                Cards.Crown()
            ]
            self.healing = [Cards.Bandage()]
            self.potions = [Cards.HealingPotion()]

    def generate_items(self):
        """Generate a list of items for the shop."""
        shop_items = []

        # Add 2 random weapons
        for _ in range(2):
            if self.weapons:
                weapon = random.choice(self.weapons)
                shop_items.append({"item": weapon, "price": weapon.price, "type": "weapon"})

        # Add 1 random armor
        if self.armors:
            armor = random.choice(self.armors)
            shop_items.append({"item": armor, "price": armor.price, "type": "armor"})

        # Add 1 random healing item
        if self.healing:
            healing = random.choice(self.healing)
            shop_items.append({"item": healing, "price": healing.price, "type": "healing"})

        # Add 1 random potion
        if self.potions:
            potion = random.choice(self.potions)
            shop_items.append({"item": potion, "price": potion.price, "type": "potion"})

        return shop_items

    def replace_item(self, item_type, player1):
        """Replace an item of the given type with a new random item."""
        if item_type == "weapon" and self.weapons:
            new_item = random.choice(self.weapons)
            return new_item
        elif item_type == "armor" and self.armors:
            new_item = random.choice(self.armors)
            return new_item
        elif item_type == "healing" and self.healing:
            new_item = random.choice(self.healing)
            return new_item
        elif item_type == "potion" and self.potions:
            new_item = random.choice(self.potions)
            return new_item
        return None
