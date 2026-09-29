import json
import pygame
from Cards import Nothing  # Assuming Cards.Nothing() is defined in Cards.py
import player

def save_player(player, file_path="player.json"):
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
    player = player.player(player_data["name"])

    # Load attributes
    player.maxHp = player_data["maxHp"]
    player.hp = player_data["hp"]
    player.level = player_data["level"]
    player.et = player_data["et"]
    player.DungeonLevel = player_data["DungeonLevel"]
    player.AdvLevel = player_data["AdvLevel"]
    player.gold = player_data["gold"]
    player.kills = player_data["kills"]
    player.curD = player_data["curD"]
    player.maxweight = player_data["maxweight"]
    player.regeneration = player_data["regeneration"]
    player.last_clicked_button = player_data["last_clicked_button"]
    player.wis = player_data["wis"]
    player.wisdom = player_data["wisdom"]
    player.timePerk = player_data["timePerk"]
    player.scout = player_data["scout"]
    player.income = player_data["income"]
    player.mode = player_data["mode"]
    player.sync_delay_start = player_data["sync_delay_start"]
    player.sync_delay_active = player_data["sync_delay_active"]
    player.sync_delay_duration = player_data["sync_delay_duration"]

    # Load cards and trinkets (assuming you have a way to map class names to objects)
    # Example: card_classes = {"Nothing": Nothing, "LightAxe": LightAxe, ...}
    def load_cards(card_names):
        cards = []
        for card_name in card_names:
            if card_name == "Nothing":
                cards.append(Nothing())
            else:
                # Add logic to map card names to their classes
                # Example: cards.append(card_classes[card_name]())
                pass
        return cards

    player.deck = load_cards(player_data["deck"])
    player.hand = load_cards(player_data["hand"])
    player.field = load_cards(player_data["field"])
    player.graveyard = load_cards(player_data["graveyard"])
    player.trinkets = load_cards(player_data["trinkets"])  # Assuming trinkets are also cards

    print(f"Player {player.name} loaded from {file_path}")
    return player
