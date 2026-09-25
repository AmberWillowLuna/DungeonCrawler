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
                          [enemies.LavaLarva(), enemies.LavaGolem(), enemies.Ent(), enemies.Demon(), enemies.Satan()], 
                          [Trap.FireTrap(), Trap.ClubTrap(), Trap.DestroyItem(), Trap.DestroyItem()])


    Dungeons=[D1, D2]
    
    random.shuffle(Dungeons)

    return Dungeons


def LoadDungeon(screen, player):
    '''Load a dungeon from the given data and display it on the screen'''
    scale = SettingHelp.get_scale()  # You can adjust this scale as needed
    Dungeons = []
    if player.curD=="":
        if player.DungeonLevel <6:
            Dungeons.append(DefineEasyDungeon())
            Dungeons.append(DefineMediumDungeon())
            Dungeons.append(DefineHardDungeon())
        elif player.DungeonLevel == 6:
            pass
   
    return Dungeons