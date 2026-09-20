
import pygame
import SettingHelp
import button
from Trinkets import Trinkets  # Import the list of trinkets


def GetTrinket(screen, player1):
    """
    Display a trinket receive screen with the trinket's name and description.
    The player can choose to take the trinket, which will apply its effects.
    """
    scale = SettingHelp.get_scale()
    clock = pygame.time.Clock()

    # Load the trinket based on player's AdvLevel and DungeonLevel
    trinket_index = player1.AdvLevel * 2 + player1.DungeonLevel
    trinket = Trinkets[trinket_index]

    # Button to take the trinket
    TakeButton = button.Button(
        800 * scale, 500 * scale, 300 * scale, 100 * scale,
        "Take", (0, 100, 0), (0, 200, 0)
    )

    # Button to skip the trinket
    SkipButton = button.Button(
        800 * scale, 650 * scale, 300 * scale, 100 * scale,
        "Skip", (100, 0, 0), (200, 0, 0)
    )

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                if TakeButton.is_clicked(mouse_pos, event):
                    # Apply the trinket's effects
                    trinket.apply(player1)
                    running = False

                if SkipButton.is_clicked(mouse_pos, event):
                    running = False

        # Update hover states
        TakeButton.check_hover(mouse_pos)
        SkipButton.check_hover(mouse_pos)

        # ---- Draw ----
        screen.fill((0, 0, 30))  # Dark blue backdrop

        # Draw title
        font = pygame.font.SysFont("Arial", int(48 * scale))
        title_text = font.render("You Found a Trinket!", True, (255, 255, 255))
        screen.blit(title_text, (600 * scale, 100 * scale))

        # Draw trinket name
        name_font = pygame.font.SysFont("Arial", int(36 * scale))
        name_text = name_font.render(trinket.name, True, (255, 215, 0))
        screen.blit(name_text, (600 * scale, 200 * scale))

        # Draw trinket description
        desc_font = pygame.font.SysFont("Arial", int(24 * scale))
        desc_lines = wrap_text(trinket.description, 500 * scale, desc_font)
        for i, line in enumerate(desc_lines):
            desc_text = desc_font.render(line, True, (255, 255, 255))
            screen.blit(desc_text, (300 * scale, 300 * scale + i * 40 * scale))

        # Draw the trinket's button (optional, for visual representation)
        trinket_button = button.Button(
            600 * scale, 400 * scale, 200 * scale, 200 * scale,
            trinket.name, (100, 100, 100), (150, 150, 150)
        )
        trinket_button.draw(screen)

        # Draw player's deck
        player1.displayDeck(screen)

        # Draw buttons
        TakeButton.draw(screen)
        SkipButton.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return True

# Helper function to wrap text
def wrap_text(text, max_width, font):
    words = text.split(' ')
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_width = font.size(word)  # Extract the width from the tuple
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width + font.size(' ')  # Add space width
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width + font.size(' ')  # Reset width

    if current_line:
        lines.append(' '.join(current_line))

    return lines
