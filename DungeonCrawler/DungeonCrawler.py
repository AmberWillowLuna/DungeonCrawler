import pygame
pygame.init()
import colors
import json
import random
import start
from button import Button, CardButton, EntityCards, WeaponCards
#make a loop with buttons

#start a window (only for this module)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
titles="Dungeon Crawler"
font = pygame.font.SysFont("Arial", 40)
small_font = pygame.font.SysFont("Arial", 30)



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




    start_button = Button(240*scale, 100*scale, 160*scale, 40*scale, "Start", colors.NAVY_BLUE, colors.GREEN)
    achievements_button = Button(240*scale, 160*scale, 160*scale, 40*scale, "Achievements", colors.NAVY_BLUE, colors.GREEN)
    options_button = Button(240*scale, 220*scale, 160*scale, 40*scale, "Options", colors.NAVY_BLUE, colors.GREEN)
    exit_button = Button(240*scale, 280*scale, 160*scale, 40*scale, "Exit", colors.NAVY_BLUE, colors.GREEN)

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

                # Add your start game logic here
            elif options_button.is_clicked(mouse_pos, event):
                pass
                # Add your options menu logic here
            elif achievements_button.is_clicked(mouse_pos, event):
                 pass
            elif exit_button.is_clicked(mouse_pos, event):
                running = False

        # Check button hover
        start_button.check_hover(mouse_pos)
        options_button.check_hover(mouse_pos)
        achievements_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)

        # Draw everything
        screen.fill(colors.BLACK)
        title_text = font.render("Dungeon Crawler", True, colors.WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        achievements_button.draw(screen)
        start_button.draw(screen)
        options_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
