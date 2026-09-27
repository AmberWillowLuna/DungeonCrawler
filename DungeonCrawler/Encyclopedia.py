import json
from tkinter import BUTT
import pygame
from enemies import enemy  # Assuming you have an enemy class
import Cards  # Assuming you have a Cards module
import os
import SettingHelp
from Screen import screen
import button  # Import your button module

scale = SettingHelp.get_scale(screen)

def display_unlocked_enemies(screen, back_button_callback=None):
    """
    Display all unlocked enemies (value = 1 in JSON) as EntityCards with a BACK button.
    Runs in a while loop until the BACK button is pressed or the window is closed.

    Args:
        screen: Pygame surface to draw on.
        back_button_callback (function): Callback function for the BACK button.

    Returns:
        bool: True if exited via BACK button, False if window was closed.
    """
    # Load scale based on the screen
    scale = SettingHelp.get_scale(screen)
    json_file_path = "encyclopedia.json"

    try:
        with open(json_file_path, 'r') as file:
            enemies_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File {json_file_path} not found.")
        return False
    except json.JSONDecodeError:
        print(f"Error: File {json_file_path} is not a valid JSON.")
        return False

    # Load the back button image (replace with your own image path)
    try:
        back_button_img = pygame.image.load("assets/back_button.png").convert_alpha()
        back_button_img = pygame.transform.scale(
            back_button_img,
            (int(100 * scale), int(50 * scale))
        )
    except:
        # Fallback: Create a simple rectangle if the image is missing
        back_button_img = None

    back_button = button.Button(
            x=int(50 * scale),
            y=int(50 * scale),
            width=int(100 * scale),
            height=int(50 * scale),
            text="BACK",
            color=(100, 100, 100),
            hover_color=(150, 150, 150),
        )

    # Positioning variables (scaled)
    start_x = int(200 * scale)  # Start after the BACK button
    start_y = int(150 * scale)
    spacing_x = int(300 * scale)  # Horizontal spacing between enemies
    spacing_y = int(350 * scale)  # Vertical spacing between rows
    card_width = int(468 // 2 * scale)  # Width of the entity card
    card_height = int(458 // 2 * scale)  # Height of the entity card

    # Main loop for displaying enemies
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if back_button and back_button.rect.collidepoint(event.pos):
                        back_button.execute_action()
                        return True  # Exited via BACK button

        # Clear the screen
        screen.fill((0, 0, 0))  # Fill with black or your preferred background color

        # Draw all unlocked enemies
        current_x = start_x
        current_y = start_y

        for enemy_name, unlocked in enemies_data.items():
            if unlocked == 1:
                # Create a temporary enemy object to access its icon and name
                temp_enemy = enemy(
                    name=enemy_name,
                    description="",  # Not used here
                    hp=0,  # Not used here
                    hand=[],  # Not used here
                    DungeonName="",  # Not used here
                    level=0  # Not used here
                )

                # Create an EntityCard for the enemy
                enemy_card = button.EntityCards(
                    x=current_x,
                    y=current_y,
                    name=enemy_name,
                    color=(50, 50, 50),
                    hover_color=(80, 80, 80),
                    card=temp_enemy
                )

                # Draw the enemy card
                enemy_card.draw(surface=screen)

                # Move to the next position
                current_x += spacing_x
                if current_x > screen.get_width() - card_width:
                    current_x = start_x
                    current_y += spacing_y

        # Draw the BACK button

        back_button.draw(screen)

        # Update the display
        pygame.display.flip()

    # Return False if the loop was interrupted (e.g., window closed)
    return False





def read_enemies_map(json_file_path):
    """
    Read the entire JSON file and return it as a map (dictionary).

    Args:
        json_file_path (str): Path to the JSON file containing enemy data.

    Returns:
        dict: A dictionary where keys are enemy names and values are 0 or 1.
    """
    try:
        with open(json_file_path, 'r') as file:
            enemies_data = json.load(file)
        return enemies_data
    except FileNotFoundError:
        print(f"Error: File {json_file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: File {json_file_path} is not a valid JSON.")
        return {}



def unlock_enemy(enemy_name, json_file_path):
    """
    Set the value of the specified enemy to 1 in the JSON file and return the updated map.

    Args:
        enemy_name (str): Name of the enemy to unlock.
        json_file_path (str): Path to the JSON file containing enemy data.

    Returns:
        dict: The updated map (dictionary) after unlocking the enemy.
    """
    try:
        with open(json_file_path, 'r') as file:
            enemies_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File {json_file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: File {json_file_path} is not a valid JSON.")
        return {}

    # Unlock the enemy if it exists
    if enemy_name in enemies_data:
        enemies_data[enemy_name] = 1
    else:
        print(f"Error: Enemy {enemy_name} not found in the JSON file.")
        return enemies_data

    # Save the updated data back to the file
    try:
        with open(json_file_path, 'w') as file:
            json.dump(enemies_data, file, indent=2)
    except Exception as e:
        print(f"Error: Could not save the updated data to {json_file_path}. Error: {e}")
        return enemies_data

    return enemies_data

