import pygame
from DungeonLoader import LoadDungeon, SaveDungeonOrder, LoadDungeonsFromFile
import SettingHelp
import button
import EncounterLoops
import Empty
import copy
import Merchant
import GetTrinkets
import Escape
import SaveAndRead
import Continue2
import Trinkets

def GameLoop(screen, player1, w=True):
    '''Main game loop for the dungeon crawler'''
    scale = SettingHelp.get_scale(screen)
    clock = pygame.time.Clock()

    Outcome = None

    #buttons for going in driections if someone want to play only with mouse
    GoLeft = button.Button(200*scale, 500*scale, 300*scale, 200*scale, "Left", (0, 0, 128), (0, 255, 0))
    GoForward = button.Button(800*scale, 150*scale, 300*scale, 200*scale, "Forward", (0, 0, 128), (0, 255, 0))
    GoRight = button.Button(1500*scale, 500*scale, 300*scale, 200*scale, "Right", (0, 0, 128), (0, 255, 0))
    SaveAndExit = button.Button(800*scale, 750*scale, 500*scale, 150*scale, "Save and Exit", (0, 0, 128), (0, 255, 0))

    font = pygame.font.SysFont("Arial", int(64*scale))
    TrinketsToFind = None
    backgroundImg = None
    dungeons=None
    if w:
        dungeons = LoadDungeon(screen, player1)
        SaveDungeonOrder(dungeons)
        TrinketsToFind = Trinkets.Tier1+ Trinkets.Tier2
        Trinkets.SaveTrinketOrder(TrinketsToFind)
    else:
        dungeons = LoadDungeonsFromFile()
        backgroundImg = pygame.image.load(dungeons[player1.AdvLevel][player1.DungeonLevel].background).convert()
        backgroundImg = pygame.transform.scale(backgroundImg, (1920*scale, 1080*scale))
        TrinketsToFind = Continue2.LoadTrinkets()
    State = "Free"
    #States 
    # Free - free to go
    # Battle - in a battle
    # Trap - in a trap 
    # Merchant - in a merchant
    # Empty - a few miliseconds to skip cuz the room was empty
    move=""


    #the front room alwyas known:








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
                    elif event.key == pygame.K_x:
                        move="Out"

                

            if event.type == pygame.MOUSEBUTTONDOWN:
                if State=="Free":
                        if GoLeft.is_clicked(mouse_pos, event):
                            move="Left"
                        elif GoForward.is_clicked(mouse_pos, event):
                            move="Forward"
                        elif GoRight.is_clicked(mouse_pos, event):
                            move="Right"
                        elif SaveAndExit.is_clicked(mouse_pos, event):
                            move="Out"

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
            SaveAndExit.draw(screen)

            # Determine the room description based on the first letter of player1.curD
            if player1.wisdom:
                sign0 = dungeons[player1.AdvLevel][player1.DungeonLevel].set[player1.level][1]
                first_letter = sign0[0]
                if first_letter == "L":
                    room_description = "Enemy"
                elif sign0 == "T":
                    room_description = "Trap"
                elif sign0 == "TR":
                    room_description = "Trinket"
                elif first_letter == "P":
                    room_description = "Empty"
                elif first_letter == "M":
                    room_description = "Merchant"
                elif first_letter == "E":
                    room_description = "Exit"
                else:
                    room_description = "Unknown"

                text_surface = font.render(f"Room: {room_description}", True, (255, 255, 255))
                screen.blit(text_surface, (600*scale, 50*scale))


            if player1.wis:
                sign1 = dungeons[player1.AdvLevel][player1.DungeonLevel].set[player1.level][0]
                sign2 = dungeons[player1.AdvLevel][player1.DungeonLevel].set[player1.level][2]
                text_surface = font.render(f"Trap !", True, (255, 255, 255))

                if sign1 == "T":
                    text_surface = font.render(f"Trap !", True, (255, 255, 255))
                    screen.blit(text_surface, (200*scale, 400*scale))

                if sign2 == "T":
                    text_surface = font.render(f"Trap !", True, (255, 255, 255))
                    screen.blit(text_surface, (1500*scale, 400*scale))

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
                elif move=="Out":
                    Dir=-1
                    SaveAndRead.save_player(player1)
                    running = False

                
                #IMPLEMENT THIS PLAYER MOVE PART
                
                move=""

                #### get the dependency of the dungeon and the player and make a logic to move the player in the dungeon
                if Dir!=-1:
                    sign = dungeons[player1.AdvLevel][player1.DungeonLevel].set[player1.level][Dir]
                else:
                    sign = " "
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
                    won = EncounterLoops.TrapLoop(screen, player1, trap)
                    player1.ascend()
                    #get graveyard back to deck                 
                    player1.graveyardToDeck()
                    player1.stripDeck()
                    State = "Free"
                    if won == "lose":
                        running = False

                elif sign in ("L1", "L2", "L3", "L4", "L5"):
                    State = "Battle"
                    enemy = copy.copy(dungeons[player1.AdvLevel][player1.DungeonLevel].get_random_enemy(sign))
                    enemy.ShuffleHand()
                    enemy.ArmAll()
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
                    if won == "lose":
                        running = False
                        Outcome = False

                    if player1.AdvLevel>5:
                        running = False
                        Outcome == True

                elif sign == "TR":
                    State = "Trinket"
                    trinket_index = player1.AdvLevel * 2 + player1.DungeonLevel
                    trinket = TrinketsToFind[trinket_index]
                    GetTrinkets.GetTrinket(screen, player1, trinket)

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

    #implementation of loss or win
    if Outcome:
        pass #it is implemented elsewhere
    elif Outcome is not None:
        game_over_screen(screen)



from player import Player
import SaveAndRead

def game_over_screen(screen):
    """
    Display a GAME OVER screen, create a new player, save it, and wait for any input to exit.

    Args:
        screen: Pygame surface to draw on.
    """
    # Load scale based on the screen
    scale = SettingHelp.get_scale(screen)

    # Create a new player with default stats
    new_player = Player("Aurelius")
    SaveAndRead.save_player(new_player, "player.json")

    # Load the game over background image (replace with your own image path)
    try:
        game_over_bg = pygame.image.load("assets/game_over_bg.png").convert_alpha()
        game_over_bg = pygame.transform.scale(
            game_over_bg,
            (screen.get_width(), screen.get_height())
        )
    except:
        # Fallback: Create a black background if the image is missing
        game_over_bg = pygame.Surface((screen.get_width(), screen.get_height()))
        game_over_bg.fill((0, 0, 0))

    # Font for the game over message
    font = pygame.font.SysFont("Arial", int(72 * scale))

    # Render the game over message
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    text_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Font for the continue message
    small_font = pygame.font.SysFont("Arial", int(36 * scale))

    # Render the continue message
    continue_text = small_font.render("Click or press any key to continue", True, (255, 255, 255))
    continue_rect = continue_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    # Main loop for the game over screen
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                running = False

        # Draw the game over screen
        screen.blit(game_over_bg, (0, 0))
        screen.blit(game_over_text, text_rect)
        screen.blit(continue_text, continue_rect)

        # Update the display
        pygame.display.flip()

    return new_player
