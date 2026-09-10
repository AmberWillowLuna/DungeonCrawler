
import random

class dungeon:
    def __init__(self, name, description, enemies, rewards, trinkets, imagname):
        self.name = name
        self.description = description
        self.enemies = enemies  # List of enemy objects
        self.rewards = rewards  # List of reward objects - items to buy in the shop
        self. trinkets = trinkets
        #load background image
        self.background = "assets/"+imagname+".png"
        # each round you choose one of the three ways to go - and you get random enemies and rewards
        self.set=[
            ["L1","L1","L1"],
            ["L1", "P", "T"],
            ["L1","L2","T"],
            ["P","L2","T"],
            ["L2","L2","L1"],
            ["M","M","M"],

            ["P","P","T"],
            ["L2","L3","L1"],
            ["P","L3","L2"],
            ["TR","TR","TR"],

            ["L3","L3","L2"],
            ["T", "L3","L4"], #level 4 enemy should be basicly same level enemy as boss fight but i dunno
            ["M","M","M"], 
            ["B","B","B"],
            ["E", "E", "E"] #escape and heal
            ]

    def randomizeSet(self):
        for s in self.set:
            random.shuffle(s)