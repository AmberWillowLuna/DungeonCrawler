
import Cards
import random
import EncounterLoops

import colors
import button
import button
import SettingHelp

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
        scale = SettingHelp.get_scale()
        self.HandButtons = [
            button.CardButton(690*scale, 550*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(910*scale, 550*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1130*scale, 550*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing")   
        ]
    #if trick == 0 it is just a one round battle like three arrows or sth
    def shuffleHand(self):
        curHand=self.hand
        #make random order of cards in hand
        self.hand = random.sample(curHand, len(curHand))
    def take_damage(self, dmg):
        pass

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
import SettingHelp
def trigger(player1, trap,screen):
    #make a one turn battle with the trap - player should have a chance to play cards and then the trap will play its cards
    #if trap.trick == 0 then it is a one turn battle
    scale = SettingHelp.get_scale()
    if trap.trick==0:
        #one round battle
        OkayButton = Button(screen.get_width() // 2 - 50, 400*scale, 300*scale, 150*scale, "Okay", colors.PINK, colors.WHITE)
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()


            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if event.type == pygame.MOUSEBUTTONDOWN:

                    player1.handle_equipment_click(mouse_pos, event)
                    if OkayButton.is_clicked(mouse_pos, event):
                        
                        running = False

            OkayButton.check_hover(mouse_pos)
            # Clear the screen
            screen.fill((0, 0, 0))       
            OkayButton.draw(screen)
            player1.displayDeck(screen)
            player1.displayHand(screen)
            # Update the display
            pygame.display.flip()




