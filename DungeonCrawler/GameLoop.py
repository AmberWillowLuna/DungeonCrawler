import pygame
from DungeonLoader import LoadDungeon
import SettingHelp
import button


def GameLoop(screen, player1):
    '''Main game loop for the dungeon crawler'''
    scale = SettingHelp.get_scale()
    clock = pygame.time.Clock()

    #buttons for going in driections if someone want to play only with mouse
    GoLeft = button.Button(200*scale, 500*scale, 300*scale, 200*scale, "Left", (0, 0, 128), (0, 255, 0))
    GoForward = button.Button(800*scale, 150*scale, 300*scale, 200*scale, "Forward", (0, 0, 128), (0, 255, 0))
    GoRight = button.Button(1500*scale, 500*scale, 300*scale, 200*scale, "Right", (0, 0, 128), (0, 255, 0))

    State = "Free"
    #States 
    # Free - free to go
    # Battle - in a battle
    # Trap - in a trap 
    # Merchant - in a merchant
    # Empty room - a few miliseconds to skip
    move=""

    backgroundImg = None


    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        if player1.curD=="":
            dungeons = LoadDungeon(screen, player1)
            player1.curD=dungeons[player1.AdvLevel][player1.DungeonLevel].name
            backgroundImg = pygame.image.load(dungeons[player1.AdvLevel][player1.DungeonLevel].background).convert()
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
                        if GoLeft.is_clicked(mouse_pos, event):
                            move="Left"
                        elif GoForward.is_clicked(mouse_pos, event):
                            move="Forward"
                        elif GoRight.is_clicked(mouse_pos, event):
                            move="Right"

                #if state is free - you can swap two cards 
                # the clicked card - get clicked status
                # when two where clicked - swap them in the hand and set clicked status to false

        ###########################DRAW#########################################
        # Clear the screen
        screen.fill((0, 0, 0))
                        
        if backgroundImg is not None:
            screen.blit(backgroundImg, (0, 0))

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
                    Dir=1
                elif move=="Left":
                    Dir=0
                elif move=="Right":
                    Dir=2
                
                #IMPLEMENT THIS PLAYER MOVE PART
                
                move=""

                #### get the dependency of the dungeon and the player and make a logic to move the player in the dungeon
                sign = dungeons[player1.AdvLevel][player1.DungeonLevel].set[player1.level][Dir]

                # if L1-L4 start a fight, L5 boss fight, T trap, P empty, M merchant, E escape, TR trinket - depending on this make a button that informs what happens and then if it is a fight then start a fight


        player1.displayDeck(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)
