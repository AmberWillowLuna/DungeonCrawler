import GameLoop
import SaveAndRead


def ContinueTheGame(screen):
    player1 = SaveAndRead.load_player()
    GameLoop.GameLoop(screen, player1, False)





import json
from Trinkets import RingOfLife, RingOfThief, NecklaceOfRegeneration, EnchantedRingOfLife, BraceletOfThief, NecklaceOfTime, NecklaceOfWisdom
from SaveAndRead import create_trinket_from_name

def LoadTrinkets(file_path="Trinket.json"):
    """
    Load trinkets from a JSON file and return them as a list of objects.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: List of trinket objects.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            trinket_names = data.get("order", [])

        trinkets = []
        for name in trinket_names:
            trinket = create_trinket_from_name(name)
            if trinket:
                trinkets.append(trinket)
            else:
                print(f"Warning: Failed to load trinket '{name}'. Skipping.")

        return trinkets

    except FileNotFoundError:
        print(f"Error: File {file_path} not found. Returning empty list.")
        return []
    except json.JSONDecodeError:
        print(f"Error: File {file_path} is not a valid JSON. Returning empty list.")
        return []
    except Exception as e:
        print(f"Error loading trinkets: {e}")
        return []