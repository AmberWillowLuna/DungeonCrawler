import json
from player import Player, save_player

def EraseAllData():
    """
    Reset all values in weapon_pedia.json, state.json, and encyclopedia.json to 0.
    Create a new Player object and save it using save_player.
    """
    # Reset weapon_pedia.json
    weapon_pedia_data = {}
    try:
        with open("weapon_pedia.json", "w") as file:
            json.dump(weapon_pedia_data, file, indent=4)
        print("weapon_pedia.json reset to empty.")
    except Exception as e:
        print(f"Error resetting weapon_pedia.json: {e}")

    # Reset state.json
    state_data = {"win": 0}
    try:
        with open("state.json", "w") as file:
            json.dump(state_data, file, indent=4)
        print("state.json reset to {'win': 0}.")
    except Exception as e:
        print(f"Error resetting state.json: {e}")

    # Reset encyclopedia.json
    encyclopedia_data = {}
    try:
        with open("encyclopedia.json", "w") as file:
            json.dump(encyclopedia_data, file, indent=4)
        print("encyclopedia.json reset to empty.")
    except Exception as e:
        print(f"Error resetting encyclopedia.json: {e}")

    # Create a new default player
    new_player = Player("Aurerlius")

    # Save the new player
    save_player(new_player, "player.json")
