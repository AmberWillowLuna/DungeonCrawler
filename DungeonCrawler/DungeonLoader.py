import pygame
import SettingHelp
import enemies
import player
import dungeons
import Cards
import random
import Trap

def DefineEasyDungeon():
    # Define a low level dungeon
    D1 = dungeons.dungeon("Orc's dungeon", "Dungeon with some green and grey creatures", [enemies.Goblin(), enemies.Orc(), enemies.ArmoredOrc(), enemies.Ogre(), enemies.OrcWizard()], [Trap.KnifeTrap(), Trap.ArrowTrap()])
    D2 = dungeons.dungeon("Misty's dungeon", "Dungeon with some slimes and undead creatures", [enemies.Slime(), enemies.DarkCreature(), enemies.Skeleton(), enemies.Ghoul(), enemies.MistyGhost()], [Trap.KnifeTrap(), Trap.ArrowTrap()])


    Dungeons=[D1, D2]
    
    random.shuffle(Dungeons)


    return Dungeons


def DefineMediumDungeon():
    # Define a mid level dungeon
    D1 = dungeons.dungeon("Library dungeon", "Dungeon with books and magic with undead and magical creatures", 
                          [enemies.Librarian(), enemies.DemonicEye(), enemies.ThreeEyedBeast(), enemies.TrophyHunter(), enemies.ArcaneGuardian()], 
                          [Trap.FireTrap(), Trap.HalbardTrap(), Trap.ArrowTrap(), Trap.DestroyItem()])
    D2 = dungeons.dungeon("Forest dungeon", "Dungeon with full of fungi, ents and gremlins", 
                          [enemies.Gremlin(), enemies.Fungis(), enemies.Ent(), enemies.TreeOfLife(), enemies.ForestSpirit()], 
                          [Trap.GasTrap(), Trap.GasBubbleTrap(), Trap.ClubTrap(), Trap.DestroyItem()])


    Dungeons=[D1, D2]
    
    random.shuffle(Dungeons)

    return Dungeons

def DefineHardDungeon():
    # Define a hard level dungeon
    D1 = dungeons.dungeon("Darkness dungeon", "Dungeon with books and magic with undead and magical creatures", 
                          [enemies.Shadow(), enemies.DarknessGhoul(), enemies.DarkKnight(), enemies.DarknessSorcerer(), enemies.Lich()], 
                          [Trap.ClubTrap(), Trap.GasBubbleTrap(), Trap.GasTrap(), Trap.DestroyItem()])
    D2 = dungeons.dungeon("Hell dungeon", "Dungeon with full of fungi, ents and gremlins", 
                          [enemies.LavaLarva(), enemies.LavaGolem(), enemies.FirerySpirit(), enemies.Demon(), enemies.Satan()], 
                          [Trap.FireTrap(), Trap.ClubTrap(), Trap.DestroyItem(), Trap.DestroyItem()])


    Dungeons=[D1, D2]
    
    random.shuffle(Dungeons)

    return Dungeons


def LoadDungeon(screen, player):
    '''Load a dungeon from the given data and display it on the screen'''
    scale = SettingHelp.get_scale(screen)  # You can adjust this scale as needed
    Dungeons = []
    if player.curD=="":
        if player.DungeonLevel <6:
            Dungeons.append(DefineEasyDungeon())
            Dungeons.append(DefineMediumDungeon())
            Dungeons.append(DefineHardDungeon())
        elif player.DungeonLevel == 6:
            # when u win manage here
            pass
   
    return Dungeons

import json

def SaveDungeonOrder(dungeons, file_path="dungeons.json"):
    """
    Save the order of dungeon names to a JSON file.

    Args:
        dungeons (list): List of dungeon lists (e.g., [[D1, D2], [D3, D4], [D5, D6]]).
        file_path (str): Path to the JSON file.
    """
    dungeon_order = []

    for dungeon_list in dungeons:
        dungeon_names = [d.name for d in dungeon_list]
        dungeon_order.append(dungeon_names)

    try:
        with open(file_path, 'w') as file:
            json.dump({"order": dungeon_order}, file, indent=4)
        print(f"Dungeon order saved to {file_path}")
    except Exception as e:
        print(f"Error saving dungeon order: {e}")



def LoadDungeonsFromFile(file_path="dungeons.json"):
    """
    Load dungeons from a JSON file and return them in a similar structure to LoadDungeon.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: List of dungeon lists (e.g., [[D1, D2], [D3, D4], [D5, D6]]).
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            dungeon_order = data.get("order", [])

        loaded_dungeons = []

        for dungeon_names in dungeon_order:
            dungeon_list = []
            for name in dungeon_names:
                # Define dungeons based on their names
                if name == "Orc's dungeon":
                    d = dungeons.dungeon(
                        name,
                        "Dungeon with some green and grey creatures",
                        [enemies.Goblin(), enemies.Orc(), enemies.ArmoredOrc(), enemies.Ogre(), enemies.OrcWizard()],
                        [Trap.KnifeTrap(), Trap.ArrowTrap()]
                    )
                elif name == "Misty's dungeon":
                    d = dungeons.dungeon(
                        name,
                        "Dungeon with some slimes and undead creatures",
                        [enemies.Slime(), enemies.DarkCreature(), enemies.Skeleton(), enemies.Ghoul(), enemies.MistyGhost()],
                        [Trap.KnifeTrap(), Trap.ArrowTrap()]
                    )
                elif name == "Library dungeon":
                    d = dungeons.dungeon(
                        name,
                        "Dungeon with books and magic with undead and magical creatures",
                        [enemies.Librarian(), enemies.DemonicEye(), enemies.ThreeEyedBeast(), enemies.TrophyHunter(), enemies.ArcaneGuardian()],
                        [Trap.FireTrap(), Trap.HalbardTrap(), Trap.ArrowTrap(), Trap.DestroyItem()]
                    )
                elif name == "Forest dungeon":
                    d = dungeons.dungeon(
                        name,
                        "Dungeon with full of fungi, ents and gremlins",
                        [enemies.Gremlin(), enemies.Fungis(), enemies.Ent(), enemies.TreeOfLife(), enemies.ForestSpirit()],
                        [Trap.GasTrap(), Trap.GasBubbleTrap(), Trap.ClubTrap(), Trap.DestroyItem()]
                    )
                elif name == "Darkness dungeon":
                    d = dungeons.dungeon(
                        name,
                        "Dungeon with books and magic with undead and magical creatures",
                        [enemies.Shadow(), enemies.DarknessGhoul(), enemies.DarkKnight(), enemies.DarknessSorcerer(), enemies.Lich()],
                        [Trap.ClubTrap(), Trap.GasBubbleTrap(), Trap.GasTrap(), Trap.DestroyItem()]
                    )
                elif name == "Hell dungeon":
                    d = dungeons.dungeon(
                        name,
                        "Dungeon with full of fungi, ents and gremlins",
                        [enemies.LavaLarva(), enemies.LavaGolem(), enemies.FirerySpirit(), enemies.Demon(), enemies.Satan()],
                        [Trap.FireTrap(), Trap.ClubTrap(), Trap.DestroyItem(), Trap.DestroyItem()]
                    )
                else:
                    print(f"Unknown dungeon name: {name}")
                    continue

                dungeon_list.append(d)

            loaded_dungeons.append(dungeon_list)

        return loaded_dungeons

    except FileNotFoundError:
        print(f"File {file_path} not found. Returning empty list.")
        return []
    except json.JSONDecodeError:
        print(f"File {file_path} is invalid. Returning empty list.")
        return []
    except Exception as e:
        print(f"Error loading dungeons: {e}")
        return []