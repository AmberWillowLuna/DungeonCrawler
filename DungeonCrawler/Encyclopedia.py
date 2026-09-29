import inspect
import json
import pygame
import enemies  # module with all enemy classes
import Cards    # module with all card classes
import SettingHelp
from Screen import screen
import button

scale = SettingHelp.get_scale(screen)

_enemy_classes = None
_card_classes = None


def _get_enemy_classes():
    """name -> enemy subclass (built once, e.g. "Orc Wizard" -> OrcWizard)."""
    global _enemy_classes
    if _enemy_classes is None:
        _enemy_classes = {}
        for _, cls in inspect.getmembers(enemies, inspect.isclass):
            if issubclass(cls, enemies.enemy) and cls is not enemies.enemy:
                _enemy_classes[cls().name] = cls
    return _enemy_classes


def _get_card_classes():
    """name -> Card subclass (built once, e.g. "Long Sword" -> LongSword)."""
    global _card_classes
    if _card_classes is None:
        _card_classes = {}
        for _, cls in inspect.getmembers(Cards, inspect.isclass):
            if issubclass(cls, Cards.Card) and cls is not Cards.Card:
                try:
                    _card_classes[cls().name] = cls
                except TypeError:
                    pass  # class needs constructor args - skip it
    return _card_classes


def _make_back_button(scale):
    return button.Button(
        x=int(50 * scale),
        y=int(50 * scale),
        width=int(150 * scale),
        height=int(100 * scale),
        text="BACK",
        color=(100, 100, 100),
        hover_color=(150, 150, 150),
    )


def _load_unlocked(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {json_file_path} not found.")
    except json.JSONDecodeError:
        print(f"Error: File {json_file_path} is not a valid JSON.")
    return None


def _layout(cards, screen, start_x, start_y, gap):
    """Place already created card buttons in a wrapping grid."""
    x, y = start_x, start_y
    for c in cards:
        if x + c.rect.width > screen.get_width() - gap and x != start_x:
            x = start_x
            y += c.rect.height + gap
        c.rect.topleft = (x, y)
        x += c.rect.width + gap


def _pedia_loop(screen, cards, draw_desc):
    """
    Shared loop: draws cards, shows draw_desc(card, screen) for the hovered one.
    Returns True when left via BACK (or ESC), False when window was closed.
    """
    scale = SettingHelp.get_scale(screen)
    back_button = _make_back_button(scale)
    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            if back_button.is_clicked(event.pos if hasattr(event, "pos") else mouse_pos, event):
                return True

        screen.fill((0, 0, 0))

        hovered = None
        for c in cards:
            c.is_hovered = c.rect.collidepoint(mouse_pos)
            c.draw(screen)
            if c.is_hovered:
                hovered = c

        back_button.check_hover(mouse_pos)
        back_button.draw(screen)

        # description is drawn LAST so no card can cover it
        if hovered is not None:
            draw_desc(hovered, screen)

        pygame.display.flip()
        clock.tick(60)


def display_unlocked_enemies(screen, back_button_callback=None):
    """
    Display all unlocked enemies (value = 1 in encyclopedia.json) as EntityCards.
    Hovering a card shows enemy name, description and the names of cards in its hand.

    Returns:
        bool: True if exited via BACK button, False if window was closed / file error.
    """
    scale = SettingHelp.get_scale(screen)
    data = _load_unlocked("encyclopedia.json")
    if data is None:
        return False

    classes = _get_enemy_classes()
    cards = []
    for enemy_name, unlocked in data.items():
        if unlocked != 1:
            continue
        cls = classes.get(enemy_name)
        if cls is None:
            print(f"Warning: no enemy class named {enemy_name}")
            continue
        real_enemy = cls()  # real enemy -> real description and hand
        cards.append(button.EntityCards(
            x=0, y=0, name=enemy_name,
            color=(50, 50, 50), hover_color=(80, 80, 80),
            card=real_enemy,
        ))

    gap = int(20 * scale)
    _layout(cards, screen, int(250 * scale), int(50 * scale), gap)
    return _pedia_loop(screen, cards, lambda c, surf: c.drawDesc3(surf, scale))


def display_unlocked_weapons(screen, back_button_callback=None):
    """
    Display all discovered weapons (value = 1 in weapon_pedia.json) as CardButtons.
    Hovering a card shows its stats (weight, type, attack, defs, heal, trick).

    Returns:
        bool: True if exited via BACK button, False if window was closed / file error.
    """
    scale = SettingHelp.get_scale(screen)
    data = _load_unlocked("weapon_pedia.json")
    if data is None:
        return False

    classes = _get_card_classes()
    cards = []
    for weapon_name, unlocked in data.items():
        if unlocked != 1:
            continue
        cls = classes.get(weapon_name)
        if cls is None:
            print(f"Warning: no card class named {weapon_name}")
            continue
        card = cls()
        cards.append(button.CardButton(
            x=0, y=0, name=weapon_name,
            color=(50, 50, 50), hover_color=(80, 80, 80),
            card=card, d=False, card_type=card.card_type,
        ))

    gap = int(20 * scale)
    _layout(cards, screen, int(250 * scale), int(50 * scale), gap)
    return _pedia_loop(screen, cards, lambda c, surf: c.drawDesc4(surf, scale))





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