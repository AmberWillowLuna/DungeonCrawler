import pygame
from DungeonLoader import LoadDungeon
import SettingHelp
import button
import EncounterLoops
import Empty
import copy
import Merchant
import GetTrinkets
import Escape

def GameLoop(screen, player1):
    '''Main game loop for the dungeon crawler'''
    scale = SettingHelp.get_scale()
    clock = pygame.time.Clock()

    #buttons for going in driections if someone want to play only with mouse
    GoLeft = button.Button(200*scale, 500*scale, 300*scale, 200*scale, "Left", (0, 0, 128), (0, 255, 0))
    GoForward = button.Button(800*scale, 150*scale, 300*scale, 200*scale, "Forward", (0, 0, 128), (0, 255, 0))
    GoRight = button.Button(1500*scale, 500*scale, 300*scale, 200*scale, "Right", (0, 0, 128), (0, 255, 0))


    dungeons = LoadDungeon(screen, player1)

    State = "Free"
    #States 
    # Free - free to go
    # Battle - in a battle
    # Trap - in a trap 
    # Merchant - in a merchant
    # Empty - a few miliseconds to skip cuz the room was empty
    move=""

    backgroundImg = None

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        if player1.curD=="":

            player1.curD=dungeons[player1.AdvLevel][player1.DungeonLevel].name
            backgroundImg = pygame.image.load(dungeons[player1.AdvLevel][player1.DungeonLevel].background).convert()
            backgroundImg = pygame.transform.scale(backgroundImg, (1920*scale, 1080*scale))
            '''
            dungeons - array of an arrays of dungeons so dungeons[0] is an array of EASY dungeons and dungeons[0][0] is first dungeon
            '''

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the game not the loop # CHANGE ########################################
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
                player1.handle_equipment_delete(mouse_pos, event)

            player1.handle_equipment_click(mouse_pos, event)
                
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

                #CAPSULATE EVERY STATE!!!!!!!!!! IN A DIFFERENT FILES!

                if sign == "P":
                    State="Empty"
                    Empty.LetsNotStopHere(screen, player1, backgroundImg, State)
                    player1.ascend()
                    State="Free"

                    #capsulate the fact that room is empty
                elif sign == "T":
                    # TO IMPLEMENT
                    State = "Trap"
                    trap = dungeons[player1.AdvLevel][player1.DungeonLevel].get_random_trap()
                    EncounterLoops.TrapLoop(screen, player1, trap)
                    State = "Free"

                elif sign in ("L1", "L2", "L3", "L4", "L5"):
                    State = "Battle"
                    enemy = copy.copy(dungeons[player1.AdvLevel][player1.DungeonLevel].get_random_enemy(sign))
                    enemy.ShuffleHand()
                    won = EncounterLoops.BattleLoop(screen, player1, enemy)
                    player1.ascend()
                    #get graveyard back to deck                 
                    player1.graveyardToDeck()
                    player1.stripDeck()

                    # TODO: actual turn-based combat resolution goes here, using
                    # player1.hand vs enemy.hand — BattleLoop only handles setup/Ready.
                    State = "Free"
                    #when it is trap player should have time to choose his set before trap setts off - so
                    #example traps - destroy a random card in hand / deal light / heavy damage / reduce eq until the end of dungeon / reduce max hp till the end 
                    # for damage - you can have a lot of traps dealing dmg like a spike trap (light axe damage) or a heavy trap (halbard damage) 
                    # also an arrow trap with 3 arrows or 2 arrows - generally traps should be in a dungeon class as Traps [] and u should get a random one
                elif sign == "TR":
                    State = "Trinket"
                    

                    GetTrinkets.GetTrinket(screen, player1)

                    player1.ascend()
                    State = "Free"

                elif sign == "M":
                    State = "Merchant"
                    Merchant.MerchantLoop(screen, player1)
                    player1.ascend()
                    player1.earn(0) #to update gold amount on screen


                    player1.stripDeck()
                    State = "Free"
                    #start a fight with a random enemy from the dungeon class
                    #ALSO YOU GET TO CHOOSE YOUR SET BEFORE THE FIGHT STARTS - so you can choose a set of 3 cards from your deck to fight with

                elif sign == "E":
                    State="Escape"
                    Escape.LetsNotStopHere(screen, player1, backgroundImg, State)
                    player1.ascend()

                    #LOAD NEW DUNGEON!
                    backgroundImg = pygame.image.load(dungeons[player1.AdvLevel][player1.DungeonLevel].background).convert()


                    State="Free"
                # if L1-L4 start a fight, L5 boss fight, T trap, P empty, M merchant, E escape, TR trinket - depending on this make a button that informs what happens and then if it is a fight then start a fight




        player1.displayDeck(screen)
        for hb in player1.DeckButtons:
            hb.check_hover2(mouse_pos, screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)
