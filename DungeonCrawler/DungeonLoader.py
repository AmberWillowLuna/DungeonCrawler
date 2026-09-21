import pygame
import SettingHelp
import enemies
import player
import dungeons
import Cards
import random
import Trap

def DefineEasyDungeon(player):
    # Define a low level dungeon
    D1 = dungeons.dungeon("Orc's dungeon", "Dungeon with some green and grey creatures", [enemies.Goblin(), enemies.Orc(), enemies.ArmoredOrc(), enemies.Ogre(), enemies.OrcWizard()], [Trap.KnifeTrap(), Trap.ArrowTrap()])
    D2 = dungeons.dungeon("Misty's dungeon", "Dungeon with some slimes and undead creatures", [enemies.Slime(), enemies.Skeleton(), enemies.DarkCreature(), enemies.Ghoul(), enemies.MistyGhost()], [Trap.KnifeTrap(), Trap.ArrowTrap()])


    Dungeons=[D1, D2]
    
    random.shuffle(Dungeons)

    return Dungeons


def DefineMediumDungeon():
    # Define a medium level dungeon
    pass

def DefineHardDungeon():
    # Define a hard level dungeon
    pass


def LoadDungeon(screen, player):
    '''Load a dungeon from the given data and display it on the screen'''
    scale = SettingHelp.get_scale()  # You can adjust this scale as needed
    Dungeons = []
    if player.curD=="":
        if player.DungeonLevel <6:
            Dungeons.append(DefineEasyDungeon(player))
        elif player.DungeonLevel == 6:
            pass
   
    return Dungeons