import pygame
import SettingHelp
import enemies
import player
import dungeons
import Cards
import random

def DefineEasyDungeon(player):
    # Define a low level dungeon
    D1 = dungeons.dungeon("Orc's dungeon", "Dungeon with some green and grey creatures", [enemies.Goblin(), enemies.Orc(), enemies.ArmoredOrc(), enemies.OrcWizard(), enemies.Ogre()], [Cards.Bandage(), Cards.Bandage(), Cards.Bandage(), Cards.Shield(), Cards.ChainMail(), Cards.Dagger(), Cards.Knife(), Cards.Knife()], ["Ring of life", "Lucky coin", "Regeneration necklace"], "orcdungeon")

    Dungeons=[D1]
    
    random.shuffle(Dungeons)

    return Dungeons


def DefineEasyMediumDungeon():
    # Define a lower medium level dungeon
    pass

def DefineMediumDungeon():
    # Define a medium level dungeon
    pass

def DefineMediumHardDungeon():
    # Define a medium to hard level dungeon
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