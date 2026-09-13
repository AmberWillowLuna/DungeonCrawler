# EncounterLoops.py
import pygame
import button
import colors
import SettingHelp

font = pygame.font.SysFont("Arial", 40)
desc_font = pygame.font.SysFont("Arial", 26)


def _build_enemy_display(enemy):
    """Build read-only CardButtons to show the enemy's hand, laid out in a row."""
    scale = SettingHelp.get_scale()
    buttons = []
    start_x = 680 * scale
    spacing = 220 * scale
    y = 240 * scale

    for i, card in enumerate(enemy.hand):
        cb = button.CardButton(
            start_x + i * spacing, y,
            card.name, (200, 200, 200), (150, 150, 150),
            card, card_type=card.card_type
        )
        buttons.append(cb)
    return buttons


def _draw_enemy_header(screen, enemy):
    scale = SettingHelp.get_scale()

    icon_x, icon_y = 150 * scale, 10 * scale
    if enemy.icon:
        icon_size = (150 * scale, 150 * scale)
        scaled_icon = pygame.transform.scale(enemy.icon, icon_size)
        screen.blit(scaled_icon, (icon_x, icon_y))
        text_x = icon_x + icon_size[0] + 20 * scale
    else:
        text_x = icon_x

    name_surf = font.render(f"{enemy.name}  (Lv {enemy.level})", True, colors.WHITE)
    screen.blit(name_surf, (text_x, icon_y))

    hp_surf = font.render(f"HP: {enemy.hp}", True, colors.WHITE)
    screen.blit(hp_surf, (text_x, icon_y + 60 * scale))

    desc_surf = desc_font.render(enemy.description, True, colors.WHITE)
    screen.blit(desc_surf, (200 * scale, icon_y + 150 * scale + 20 * scale))

def TrapLoop(screen, player1, trap):
    """
    Encapsulated setup loop for a Trap encounter.
    Lets the player rearrange cards (swap deck/hand) and confirm with Ready.
    Returns once the player presses Ready.
    """
    scale = SettingHelp.get_scale()
    clock = pygame.time.Clock()

    ReadyButton = button.Button(
        800 * scale, 50 * scale, 300 * scale, 100 * scale,
        "Ready", (0, 100, 0), (0, 200, 0)
    )

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                player1.handle_equipment_click(mouse_pos, event)
                if ReadyButton.is_clicked(mouse_pos, event):
                    running = False

        ReadyButton.check_hover(mouse_pos)

        # ---- draw ----
        screen.fill((30, 0, 0))  # dim red backdrop to signal danger

        title_surf = font.render("A trap! Adjust your equipment.", True, colors.WHITE)
        screen.blit(title_surf, (400 * scale, 10 * scale))

        desc_surf = desc_font.render(trap.description, True, colors.WHITE)
        screen.blit(desc_surf, (400 * scale, 60 * scale))

        ReadyButton.draw(screen)
        player1.displayDeck(screen)

        pygame.display.flip()
        clock.tick(60)

    # Player confirmed -> apply the trap's effect
    trap.trigger(player1)  # assumes Trap has a .trigger(player) method; adjust to your Trap class


def BattleLoop(screen, player1, enemy):
    """
    Encapsulated setup loop for a Battle encounter.
    Shows the enemy (name, description, hp, hand) and lets the player
    rearrange cards before confirming with Ready.
    Returns once the player presses Ready (actual combat resolution happens after this).
    """
    scale = SettingHelp.get_scale()
    clock = pygame.time.Clock()

    ReadyButton = button.Button(
        800 * scale, 500 * scale, 300 * scale, 100 * scale,
        "Ready", (0, 100, 0), (0, 200, 0)
    )

    enemy_buttons = _build_enemy_display(enemy)
    # asset/enemy.name+"png"
    


    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                player1.handle_equipment_click(mouse_pos, event)
                if ReadyButton.is_clicked(mouse_pos, event):
                    running = False

        ReadyButton.check_hover(mouse_pos)
        for eb in enemy_buttons:
            eb.check_hover(mouse_pos)  # purely cosmetic, they aren't clickable for swaps

        # ---- draw ----
        screen.fill((0, 0, 30))  # dim blue backdrop for battle

        _draw_enemy_header(screen, enemy)
        for eb in enemy_buttons:
            eb.draw(screen)

        ReadyButton.draw(screen)
        player1.displayDeck(screen)


        pygame.display.flip()
        clock.tick(60)

    # Player confirmed their set -> hand off to actual combat resolution
    Battle(screen, player1, enemy)
    return True


def Battle(screen, player1, enemy):
    # loop with fight instead of ready button
    # after fight you reveal cards of enemy (that are shuffled)
    # all cards with atack are resolved
    #tricks are resolved
    # healing may be resolved but new logic for healing is needed

