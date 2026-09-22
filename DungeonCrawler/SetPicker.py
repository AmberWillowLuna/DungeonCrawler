import pygame
import button
import SettingHelp
import Cards

def ChooseSet(screen, player1):
    '''Choose a starting set for the game'''
    scale = SettingHelp.get_scale()

    # Create buttons for the set picker
    set1Button = button.Button(720*scale, 300*scale, 550*scale, 160*scale, "SwordMan", (0, 0, 128), (0, 255, 0))
    set2Button = button.Button(720*scale, 500*scale, 550*scale, 160*scale, "King of Halbard", (0, 0, 128), (0, 255, 0))
    set3Button = button.Button(720*scale, 700*scale, 550*scale, 160*scale, "Spearman", (0, 0, 128), (0, 255, 0))

    # Main loop for the set picker
    #set 1 - longsword
    # set 2 - halbard and crown
    # set 3 - spear and light axe



    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Check button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if set1Button.is_clicked(mouse_pos, event):
                    player1.addItem(Cards.Sword())
                    player1.addItem(Cards.HealingPotion())
                    running = False
                elif set2Button.is_clicked(mouse_pos, event):
                    player1.addItem(Cards.SwordOfDarkness())
                    running = False
                elif set3Button.is_clicked(mouse_pos, event):
                    player1.addItem(Cards.Spear())
                    player1.addItem(Cards.Boomerang())
                    running = False

        # Draw everything
        screen.fill((0, 0, 0))
        set1Button.draw(screen)
        set2Button.draw(screen)
        set3Button.draw(screen)

        pygame.display.flip()

    # add three bandages
    player1.addItem(Cards.Bandage())
