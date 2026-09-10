import pygame
from DungeonLoader import LoadDungeon
import SettingHelp
import button

def GameLoop(screen, player1):
    '''Main game loop for the dungeon crawler'''
    scale = SettingHelp.get_scale()
    clock = pygame.time.Clock()

    #buttons for going in driections if someone want to play only with mouse
    GoLeft = button.Button(100*scale, 500*scale, 100*scale, 100*scale, "Left", (0, 0, 128), (0, 255, 0))
    GoForward = button.Button(300*scale, 300*scale, 100*scale, 100*scale, "Forward", (0, 0, 128), (0, 255, 0))
    GoRight = button.Button(500*scale, 500*scale, 100*scale, 100*scale, "Right", (0, 0, 128), (0, 255, 0))

    State = "Free"
    #States 
    # Free - free to go
    # Battle - in a battle
    # Trap - in a trap 
    # Merchant - in a merchant
    # Empty room - a few miliseconds to skip
    move=""



    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        if player1.curD=="":
            dungeons = LoadDungeon(screen, player1)
            '''
            dungeons - array of an arrays of dungeons so dungeons[0] is an array of EASY dungeons and dungeons[0][0] is first dungeon
            '''

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle player movement
            if event.type == pygame.KEYDOWN:
                #here make a logic to move player in the dungeon BUT ONLY IF YOU ARE NOT IN FIGHT
                if State=="Free":
                    if event.key == pygame.K_w:
                        move="Forward"
                    elif event.key == pygame.K_a:
                        move="Left"
                    elif event.key == pygame.K_d:
                        move="Right"
                

            if event.type == pygame.MOUSEBUTTONDOWN:
                if State=="Free":
                        if GoLeft.is_clicked(mouse_pos):
                            move="Left"
                        elif GoForward.is_clicked(mouse_pos):
                            move="Forward"
                        elif GoRight.is_clicked(mouse_pos):
                            move="Right"

        ###########################DRAW#########################################
        # Clear the screen
        screen.fill((0, 0, 0))

        if State=="Free":
            # Draw movement buttons
            GoLeft.draw(screen)
            GoForward.draw(screen)
            GoRight.draw(screen)


            #MOVEMENT
            if move!="":
                # Here you would implement the logic to move the player in the dungeon
                #print(f"Player moves {move}")
                if move=="Forward":
                    player1.currentDungeon.move_forward()
                elif move=="Left":
                    player1.currentDungeon.move_left()
                elif move=="Right":
                    player1.currentDungeon.move_right()
                
                #IMPLEMENT THIS PLAYER MOVE PART
                
                move=""
                




        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)
