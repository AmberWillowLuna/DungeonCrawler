import pygame
import SettingHelp
import button
import SetPicker

def start(screen):
    '''Start the game loop
    -show battle tutorial 
    -make the choice to load game and start new game
    -when new game u get to choose a starting deck 

    '''
    scale = SettingHelp.get_scale()

    # Create buttons for the start menu

    newGameButton = button.Button(720*scale, 300*scale, 480*scale, 160*scale, "New Game", (0, 0, 128), (0, 255, 0))
    continueButton = button.Button(720*scale, 500*scale, 480*scale, 160*scale, "Continue", (0, 0, 128), (0, 255, 0))


    running=True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check button clicks
            if newGameButton.is_clicked(mouse_pos, event):
                SetPicker.ChooseSet(screen)
                # Add your new game logic here
            elif continueButton.is_clicked(mouse_pos, event):
                print("Continue button clicked")
                # Add your continue game logic here

        #display elements
        # Draw everything
        screen.fill((0, 0, 0))
        newGameButton.draw(screen)
        continueButton.draw(screen)
        pygame.display.flip()

          


