import Cards


card_classes = {
        "Nothing": Cards.Nothing,
        "LongSword": Cards.LongSword,
        "Shield": Cards.Shield,
        "Halberd": Cards.Halberd,
        "LightAxe": Cards.LightAxe,
        "Bow": Cards.Bow,
        "Arrow": Cards.Arrow,
        "Crown": Cards.Crown,
        "HealingAmulet": Cards.HealingAmulet,
        "Bandage": Cards.Bandage,
        "FishingRod": Cards.FishingRod,
        "Helmet": Cards.Helmet,
        "ShoulderPlate": Cards.ShoulderPlate,
        "ChainMail": Cards.ChainMail,
        "Spear": Cards.Spear,
        "Dagger": Cards.Dagger,
        "Knife": Cards.Knife,
        "MagicHat": Cards.MagicHat,
        "Club": Cards.Club,
        "HealingPotion": Cards.HealingPotion,
        "Sword": Cards.Sword,
        "Machete": Cards.Machete,
        "Boomerang": Cards.Boomerang,
        "MagicMirror": Cards.MagicMirror,
        "SpellBook": Cards.SpellBook,
        "SpellShield": Cards.SpellShield,
        "MagicEye": Cards.MagicEye,
        "RitualKnife": Cards.RitualKnife,
        "KnifePack": Cards.KnifePack,
        "PoisonousGas": Cards.PoisonousGas,
        "GasBubble": Cards.GasBubble,
        "Fire": Cards.Fire,
        "Fireball": Cards.Fireball,
        "FierySword": Cards.FierySword,
        "DevilHorns": Cards.DevilHorns,
        "Trident": Cards.Trident,
        "SwordOfDarkness": Cards.SwordOfDarkness,
    }

def create_card_from_name(card_name):
    """
    Create a card object based on its name.

    Args:
        card_name (str): The name of the card.

    Returns:
        Card: An instance of the card class, or a Nothing card if the card is unknown.
    """
    # Mapping of card names to their classes


    # Get the card class from the mapping
    card_class = card_classes.get(card_name)

    if card_class:
        return card_class()
    else:
        print(f"Warning: Unknown card name '{card_name}'. Returning Nothing card.")
        return Cards.Nothing()
