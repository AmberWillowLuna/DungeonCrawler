import SettingHelp
import json
import pygame


def load_background(screen):
    """
    Load the background image based on the 'win' value in state.json.

    Args:
        screen: Pygame surface to get dimensions for scaling.

    Returns:
        pygame.Surface: The loaded and scaled background image.
    """
    # Load scale based on the screen
    scale = SettingHelp.get_scale(screen)

    # Default background path
    background_path = "assets/PBack.png"  # Default path for win=0

    # Try to read 'win' from state.json
    try:
        with open("state.json", "r") as file:
            state_data = json.load(file)
            if state_data.get("win", 0) == 1:
                background_path = "assets/WBack.png"  # Path for win=1
    except FileNotFoundError:
        print("state.json not found. Using default background.")
    except json.JSONDecodeError:
        print("state.json is invalid. Using default background.")
    except Exception as e:
        print(f"Error reading state.json: {e}. Using default background.")

    # Try to load the background image
    try:
        background = pygame.image.load(background_path).convert_alpha()
        background = pygame.transform.scale(
            background,
            (screen.get_width(), screen.get_height())
        )
    except:
        # Fallback: Create a black background if the image is missing
        background = pygame.Surface((screen.get_width(), screen.get_height()))
        background.fill((0, 0, 0))
        print(f"Failed to load background from {background_path}. Using black background.")

    return background