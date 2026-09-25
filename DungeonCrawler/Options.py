import SettingHelp
import json
import button
import colors
import pygame

def Options(screen):

    # --------------------------------
    # Options menu
    # --------------------------------
    clock = pygame.time.Clock()
    scale = SettingHelp.get_scale()
    font = pygame.font.SysFont("Arial", 36)

    resolutions = [
        "640x360",
        "1280x720",
        "1920x1080"
    ]

    screen_states = [
        "Windowed",
        "Fullscreen"
    ]

    # --------------------------------
    # Load settings
    # --------------------------------

    try:
        with open("settings.json", "r", encoding="utf-8") as file:
            settings = json.load(file)

        current_resolution = settings.get("Resolution", "1920x1080")
        current_state = settings.get("State", "Windowed")

    except (FileNotFoundError, json.JSONDecodeError):
        current_resolution = "1920x1080"
        current_state = "Windowed"

    # Make sure settings are valid
    if current_resolution not in resolutions:
        current_resolution = "1920x1080"

    if current_state not in screen_states:
        current_state = "Windowed"

    # --------------------------------
    # Create buttons
    # --------------------------------

    SaveAndExit = button.Button(
        800 * scale,
        520 * scale,
        520 * scale,
        120 * scale,
        "Save and Exit",
        colors.NAVY_BLUE,
        colors.GREEN
    )

    back_button = button.Button(
        800 * scale,
        680 * scale,
        520 * scale,
        120 * scale,
        "Back",
        colors.NAVY_BLUE,
        colors.GREEN
    )

    res_button = button.Button(
        800 * scale,
        360 * scale,
        520 * scale,
        120 * scale,
        f"Resolution: {current_resolution}",
        colors.NAVY_BLUE,
        colors.GREEN
    )

    screen_button = button.Button(
        800 * scale,
        200 * scale,
        520 * scale,
        120 * scale,
        f"Screen: {current_state}",
        colors.NAVY_BLUE,
        colors.GREEN
    )

    running = True

    # --------------------------------
    # Main options loop
    # --------------------------------

    while running:

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                return screen

            # --------------------------------
            # Back
            # --------------------------------

            if back_button.is_clicked(mouse_pos, event):
                running = False

            # --------------------------------
            # Resolution
            # --------------------------------

            elif res_button.is_clicked(mouse_pos, event):

                current_index = resolutions.index(current_resolution)

                current_index = (current_index + 1) % len(resolutions)

                current_resolution = resolutions[current_index]

                res_button.text = f"Resolution: {current_resolution}"

            # --------------------------------
            # Screen mode
            # --------------------------------

            elif screen_button.is_clicked(mouse_pos, event):

                current_index = screen_states.index(current_state)

                current_index = (current_index + 1) % len(screen_states)

                current_state = screen_states[current_index]

                screen_button.text = f"Screen: {current_state}"

            # --------------------------------
            # Save and Exit
            # --------------------------------

            elif SaveAndExit.is_clicked(mouse_pos, event):

                # Save settings to JSON
                settings = {
                    "Resolution": current_resolution,
                    "State": current_state
                }

                with open("settings.json", "w", encoding="utf-8") as file:
                    json.dump(settings, file, indent=4)

                # --------------------------------
                # Convert resolution to integers
                # --------------------------------

                new_width, new_height = map(
                    int,
                    current_resolution.split("x")
                )

                # --------------------------------
                # Set display mode
                # --------------------------------

                if current_state == "Fullscreen":
                    screen = pygame.display.set_mode(
                        (new_width, new_height),
                        pygame.FULLSCREEN
                    )
                else:
                    screen = pygame.display.set_mode(
                        (new_width, new_height)
                    )

                # --------------------------------
                # Update dimensions
                # --------------------------------

                SCREEN_WIDTH = new_width
                SCREEN_HEIGHT = new_height

                # Exit options menu
                running = False

        # --------------------------------
        # Draw menu
        # --------------------------------

        screen.fill(colors.BLACK)

        title_text = font.render(
            "Options",
            True,
            colors.LIGHT_BLUE
        )

        screen.blit(
            title_text,
            (SettingHelp.get_window_size()[0] // 2, 50)
        )

        res_button.draw(screen)
        screen_button.draw(screen)
        back_button.draw(screen)
        SaveAndExit.draw(screen)

        pygame.display.flip()

        clock.tick(60)

    # Return the possibly changed screen
    return screen
