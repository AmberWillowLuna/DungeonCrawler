
import random

class dungeon:
    def __init__(self, name, description, enemies, rewards, trinkets, imagname, traps):
        self.name = name
        self.description = description
        self.enemies = enemies  # List of enemy objects
        self.rewards = rewards  # List of reward objects - items to buy in the shop
        self. trinkets = trinkets
        #load background image
        self.background = "assets/"+imagname+".png"
        self.traps = traps
        # each round you choose one of the three ways to go - and you get random enemies and rewards
        self.set=[
            ["L1","L1","L1"],
            ["L1", "P", "T"],
            ["L2","L2","T"],
            ["P","L2","T"],
            ["L2","L2","L1"],
            ["M","M","M"],

            ["P","P","T"],
            ["L2","L3","L1"],
            ["P","L3","L3"],
            ["TR","TR","TR"],

            ["L3","L3","L4"],
            ["T", "L3","L4"], #level 4 enemy should be basicly same level enemy as boss fight but i dunno
            ["M","M","M"], 
            ["L5","L5","L5"],
            ["E", "E", "E"] #escape and heal
            ]


    def get_random_enemy(self, level):
        #the second symbol in the set is the level of the enemy - so if it is L1 then get a random enemy from the enemies list with level 1
        return self.enemies[int(level[1])-1]

    def randomizeSet(self):
        for s in self.set:
            random.shuffle(s)

    def get_random_trap(self):
        # Return a random trap from the dungeon's enemies list that is of type "trap"
        return self.traps[random.randint(0, len(self.traps)-1)]