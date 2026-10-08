import pygame
import button
import SettingHelp
import Cards

def ChooseSet(screen, player1):
    '''Choose a starting set for the game'''
    scale = SettingHelp.get_scale(screen)

    # Create buttons for the set picker
    set1Button = button.Button(720*scale, 300*scale, 550*scale, 160*scale, "Barbarian", (0, 0, 128), (0, 255, 0))
    set2Button = button.Button(720*scale, 500*scale, 550*scale, 160*scale, "Palladin", (0, 0, 128), (0, 255, 0))
    set3Button = button.Button(720*scale, 700*scale, 550*scale, 160*scale, "Ranger", (0, 0, 128), (0, 255, 0))



    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Check button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if set1Button.is_clicked(mouse_pos, event):
                    player1.addItem(Cards.LightAxe())
                    player1.addItem(Cards.Helmet())
                    running = False
                elif set2Button.is_clicked(mouse_pos, event):
                    player1.addItem(Cards.Sword())
                    running = False
                elif set3Button.is_clicked(mouse_pos, event):
                    player1.addItem(Cards.Bow())
                    player1.addItem(Cards.Arrow())
                    running = False

        # Draw everything
        screen.fill((0, 0, 0))
        set1Button.draw(screen)
        set2Button.draw(screen)
        set3Button.draw(screen)

        pygame.display.flip()

    # add three bandages
    player1.addItem(Cards.Bandage())
