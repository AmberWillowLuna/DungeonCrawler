
import Cards
import random
import EncounterLoops

import colors
from button import Button

class Trap:
    def __init__(self, name, description, hand, DungeonName,  trick):
        self.name = name
        self.hand = hand # List of card objects
        self.trick = trick
        self.field = []
        self.hp = 0
        self.maxhp = 0
        self.description = description
        self.DungeonName = DungeonName
        self.type="trap"
    #if trick == 0 it is just a one round battle like three arrows or sth
    def shuffleHand(self):
        curHand=self.hand
        #make random order of cards in hand
        self.hand = random.sample(curHand, len(curHand))

''' 
trick lists:
1 - destroy item
'''


class ArrowTrap(Trap):
    def __init__(self):
        super().__init__("Arrow Trap", "A trap that shoots arrows at the player.", [Cards.Arrow(), Cards.Arrow(), Cards.Arrow()], "Orc's dungeon", 0)
        self.shuffleHand()

class KnifeTrap(Trap):
    def __init__(self):
        super().__init__("Knife Trap", "A trap that throws knife at the player.", [Cards.Knife(), Cards.Nothing(), Cards.Nothing()], "Orc's dungeon", 0)
        self.shuffleHand()

class HalbardTrap(Trap):
    def __init__(self):
        super().__init__("Halbard Trap", "A trap that swings a halbard at the player.", [Cards.Halbard(), Cards.Nothing(), Cards.Nothing()], "Orc's dungeon", 0)
        self.shuffleHand()

class DestroyItem(Trap):
    def __init__(self):
        super().__init__("Destroy Item Trap", "A trap that destroys one of the player's items.", [Cards.Nothing(), Cards.Nothing(), Cards.Nothing()], "Orc's dungeon", 1)
        Index= random.randint(0, 2)
        
    def trick(self, player1):
        player1.hand[self.Index]= Cards.Nothing()









import pygame
def trigger(player1, trap,screen):
    #make a one turn battle with the trap - player should have a chance to play cards and then the trap will play its cards
    #if trap.trick == 0 then it is a one turn battle
    if trap.trick==0:
        #one round battle
        OkayButton = Button(screen.get_width() // 2 - 50, screen.get_height() - 100, 100, 50, "Okay", colors.GRAY, colors.WHITE)
        running = True
        while running:




            # Clear the screen
            screen.fill((0, 0, 0))
            
            # Draw the trap's hand and the player's hand
            #EncounterLoops.draw_hands(screen, player1.hand, trap.hand)
            #resolve round i guess!
            EncounterLoops._resolve_round(player1, trap)


            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if OkayButton.is_clicked(pygame.mouse.get_pos(), event):
                    running = False
            
            # Update the display
            pygame.display.flip()




