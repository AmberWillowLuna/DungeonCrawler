#functions to get scale and window size
import pygame
import json
def get_scale():
    # Get the current display info
    display_info = pygame.display.Info()
    width, height = display_info.current_w, display_info.current_h

    # Calculate scale based on a reference resolution (e.g., 1920x1080)
    reference_width = 1920
    reference_height = 1080
    scale_x = width / reference_width
    scale_y = height / reference_height

    # Return the smaller scale to maintain aspect ratio
    return min(scale_x, scale_y)

def get_window_size():
    # Get the current display info
    display_info = pygame.display.Info()
    width, height = display_info.current_w, display_info.current_h
    return width, height

def getFromFile():
    # Read the settings from the json file and return them as a dictionary
     pass



    #except FileNotFoundError:
        # If the file doesn't exist, return default settings
      #  return {"Resolution": "1920x1080", "State": "Windowed"}