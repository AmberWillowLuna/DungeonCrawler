import pygame
pygame.init()
import colors
import json
import random
from Screen import screen
import start
from button import Button, CardButton, EntityCards, WeaponCards
import Options
import SettingHelp
import Encyclopedia
import Background
#make a loop with buttons

#start a window (only for this module)




scale = SettingHelp.get_scale(screen)
titles="Dungeon Crawler"
font = pygame.font.SysFont("Arial", int(64*scale))
small_font = pygame.font.SysFont("Arial", int(45*scale))



def main():

    #get the state from settings file
    # Get the state from settings file
    with open("settings.json", "r", encoding="utf-8") as file:
        settings = json.load(file)

    STATE = settings["State"]
    Resolution = settings["Resolution"]

    new_width, new_height = map(int, Resolution.split("x"))
    SCREEN_WIDTH = new_width
    SCREEN_HEIGHT = new_height

    if STATE == "Fullscreen":
        screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.FULLSCREEN
        )
    else:
        screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
        )

    scale = 1.0*SCREEN_WIDTH/640


    background = Background.load_background(screen)

    start_button = Button(240*scale, 100*scale, 160*scale, 40*scale, "Start", colors.NAVY_BLUE, colors.GREEN)
    Encyclopedia_button = Button(240*scale, 150*scale, 160*scale, 40*scale, "Encyclopedia", colors.NAVY_BLUE, colors.GREEN)
    Weapons_button = Button(240*scale, 200*scale, 160*scale, 40*scale, "Weapons", colors.NAVY_BLUE, colors.GREEN)
    options_button = Button(240*scale, 250*scale, 160*scale, 40*scale, "Options", colors.NAVY_BLUE, colors.GREEN)
    exit_button = Button(240*scale, 300*scale, 160*scale, 40*scale, "Exit", colors.NAVY_BLUE, colors.GREEN)

    clock = pygame.time.Clock()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Check button clicks
            if start_button.is_clicked(mouse_pos, event):
                start.start(screen)
            elif options_button.is_clicked(mouse_pos, event):
                Options.Options(screen)
            elif Encyclopedia_button.is_clicked(mouse_pos, event):
                Encyclopedia.display_unlocked_enemies(screen)
            elif Weapons_button.is_clicked(mouse_pos, event):
                Encyclopedia.display_unlocked_weapons(screen)
            elif exit_button.is_clicked(mouse_pos, event):
                running = False

        # Check button hover
        start_button.check_hover(mouse_pos)
        options_button.check_hover(mouse_pos)
        Encyclopedia_button.check_hover(mouse_pos)
        Weapons_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)

        # Draw everything
        screen.fill(colors.BLACK)
        screen.blit(background, (0, 0))
        title_text = font.render("Dungeon Crawler", True, colors.WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        Encyclopedia_button.draw(screen)
        Weapons_button.draw(screen)
        start_button.draw(screen)
        options_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()




