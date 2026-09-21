import pygame
from DungeonLoader import LoadDungeon
import SettingHelp
import button

#make a button to be used in the empty room to skip the room

def LetsNotStopHere(screen, player1, backgroundImg, State):
    '''Main game loop for the dungeon crawler'''
    scale = SettingHelp.get_scale()
    clock = pygame.time.Clock()

    LesGo = button.Button(700*scale, 150*scale, 800*scale, 300*scale, "You have survived the dungeon!", (0, 0, 128), (0, 255, 0))


    player1.heal(player1.maxHp)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the game not the loop # CHANGE ########################################
                running = False
                

            # Handle player movement
            if event.type == pygame.KEYDOWN:
                State="Free"
                running=False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if LesGo.is_clicked(mouse_pos, event):
                    State="Free"
                    running=False


                #if state is free - you can swap two cards 
                # the clicked card - get clicked status
                # when two where clicked - swap them in the hand and set clicked status to false

        ###########################DRAW#########################################
        # Clear the screen
        screen.fill((0, 0, 0))
                        
        if backgroundImg is not None:
            screen.blit(backgroundImg, (0, 0))

        LesGo.draw(screen)

        player1.displayDeck(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)



