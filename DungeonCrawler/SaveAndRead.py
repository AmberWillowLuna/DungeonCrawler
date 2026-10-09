import json
import pygame
from Cards import Nothing  # Assuming Cards.Nothing() is defined in Cards.py
import player

def save_player(player,file_path="player.json"):
    """
    Save the player's data to a JSON file.

    Args:
        player (Player): The Player object to save.
        file_path (str): Path to the JSON file.
    """
    # Prepare data for serialization
    player_data = {
        "name": player.name,
        "deck": [card.__class__.__name__ for card in player.deck],  # Save card class names
        "hand": [card.__class__.__name__ for card in player.hand],
        "field": [card.__class__.__name__ for card in player.field],
        "graveyard": [card.__class__.__name__ for card in player.graveyard],
        "trinkets": [trinket.__class__.__name__ for trinket in player.trinkets],
        "maxHp": player.maxHp,
        "hp": player.hp,
        "level": player.level,
        "et": player.et,
        "DungeonLevel": player.DungeonLevel,
        "AdvLevel": player.AdvLevel,
        "gold": player.gold,
        "kills": player.kills,
        "curD": player.curD,
        "maxweight": player.maxweight,
        "regeneration": player.regeneration,
        "last_clicked_button": player.last_clicked_button,
        "wis": player.wis,
        "wisdom": player.wisdom,
        "timePerk": player.timePerk,
        "scout": player.scout,
        "income": player.income,
        "mode": player.mode,
        "sync_delay_start": player.sync_delay_start,
        "sync_delay_active": player.sync_delay_active,
        "sync_delay_duration": player.sync_delay_duration,
    }

    # Save to JSON file
    try:
        with open(file_path, 'w') as file:
            json.dump(player_data, file, indent=4)
        print(f"Player data saved to {file_path}")
    except Exception as e:
        print(f"Error saving player data: {e}")


from LoadHelper import create_card_from_name


def load_player(file_path="player.json"):
    """
    Load a player's data from a JSON file and create a Player object.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        Player: The loaded Player object, or None if loading fails.
    """
    try:
        with open(file_path, 'r') as file:
            player_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File {file_path} is not a valid JSON.")
        return None

    # Create a new Player object
    player1 = player.Player(player_data["name"])

    # Load attributes
    player1.maxHp = player_data["maxHp"]
    player1.hp = player_data["hp"]
    player1.level = player_data["level"]
    player1.et = player_data["et"]
    player1.DungeonLevel = player_data["DungeonLevel"]
    player1.AdvLevel = player_data["AdvLevel"]
    player1.gold = player_data["gold"]
    player1.kills = player_data["kills"]
    player1.curD = player_data["curD"]
    player1.maxweight = player_data["maxweight"]
    player1.regeneration = player_data["regeneration"]
    player1.last_clicked_button = player_data["last_clicked_button"]
    player1.wis = player_data["wis"]
    player1.wisdom = player_data["wisdom"]
    player1.timePerk = player_data["timePerk"]
    player1.scout = player_data["scout"]
    player1.income = player_data["income"]
    player1.mode = player_data["mode"]
    player1.sync_delay_start = player_data["sync_delay_start"]
    player1.sync_delay_active = player_data["sync_delay_active"]
    player1.sync_delay_duration = player_data["sync_delay_duration"]

    # Load cards and trinkets using the new function
    player1.deck = [create_card_from_name(card_name) for card_name in player_data["deck"]]
    player1.hand = [create_card_from_name(card_name) for card_name in player_data["hand"]]
    player1.field = [create_card_from_name(card_name) for card_name in player_data["field"]]
    player1.graveyard = [create_card_from_name(card_name) for card_name in player_data["graveyard"]]
    player1.trinkets = [create_trinket_from_name(card_name) for card_name in player_data["trinkets"]]

    player1.sync_deck()



    return player1

import Trinkets

def create_trinket_from_name(name):
    """
    Create a trinket object based on its name.

    Args:
        name (str): The name of the trinket.

    Returns:
        Trinket: An instance of the trinket class, or None if the trinket is unknown.
    """
    # Mapping of trinket names to their classes
    trinket_classes = {
        "Ring of Life": Trinkets.RingOfLife,
        "RingOfLife": Trinkets.RingOfLife,
        "Ring of Thief": Trinkets.RingOfThief,
        "RingOfThief": Trinkets.RingOfThief,  # Handle potential typo
        "Ring of Wisdom": Trinkets.RingOfKnowledge,
        "RingOfKnowledge": Trinkets.RingOfKnowledge,
        "Regen Ring": Trinkets.NecklaceOfRegeneration,
        "NecklaceOfRegeneration": Trinkets.NecklaceOfRegeneration,
        "Life Gem": Trinkets.EnchantedRingOfLife,
        "EnchantedRingOfLife": Trinkets.EnchantedRingOfLife,
        "Thief's Bracelet": Trinkets.BraceletOfThief,
        "BraceletOfThief": Trinkets.BraceletOfThief,       
        "Magical Clock": Trinkets.NecklaceOfTime,
        "NecklaceOfTime": Trinkets.NecklaceOfTime,
        "Owl Totem": Trinkets.NecklaceOfWisdom,
        "NecklaceOfWisdom": Trinkets.NecklaceOfWisdom,
    }

    # Get the trinket class from the mapping
    trinket_class = trinket_classes.get(name)
    if trinket_class:
        return trinket_class()
    else:
        print(f"Warning: Unknown trinket name '{name}'. Returning None.")
        return None