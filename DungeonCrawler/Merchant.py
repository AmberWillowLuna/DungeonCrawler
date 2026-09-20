import pygame
import SettingHelp
import button
import Shop

def MerchantLoop(screen, player1):
    """
    Encapsulated loop for a merchant shop.
    Displays 2 weapons, 1 armor, 1 healing item, and 1 potion.
    When a player buys an item, it is replaced with a new random item.
    Returns once the player clicks the "Proceed" button.
    """
    scale = SettingHelp.get_scale()
    clock = pygame.time.Clock()

    # Load background image
    try:
        background = pygame.image.load("assets/M"+player1.curD+".png")
        background = pygame.transform.scale(
            background,
            (screen.get_width(), screen.get_height())
        )
    except:
        background = None
        print(f"Warning: Background image not found. Using solid color instead. {player1.curD}")

    # Create a Shop instance for the current dungeon
    shop = Shop.Shop(player1.curD)
    shop_items = shop.generate_items()  # Generate initial items

    # Button to proceed from the merchant screen
    ProceedButton = button.Button(
        1000 * scale, 800 * scale, 500 * scale, 200 * scale,
        "Proceed", (0, 100, 0), (0, 200, 0)
    )

    # Create buttons for each shop item
    item_buttons = []
    for i, item in enumerate(shop_items):
        button_x = 200 * scale
        button_y = (200 + i * 120) * scale  # Stack items vertically with spacing
        item_button = button.Button(
            button_x,
            button_y,
            600 * scale,
            100 * scale,
            f"{item['item'].name} - {item['price']} gold",
            (70, 70, 70),
            (100, 100, 100)
        )
        item_buttons.append((item_button, item['item'], item['type'], item['price']))

    # On-screen notification text
    notification_text = ""
    notification_timer = 0

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any item button is clicked
                player1.handle_equipment_click(mouse_pos, event)
                player1.handle_equipment_delete(mouse_pos, event)
                for item_button, item, item_type, price in item_buttons:
                    if item_button.is_clicked(mouse_pos, event):
                        # Handle item purchase logic here
                        if player1.gold >= price:
                            player1.gold -= price
                            # Add the item to player's inventory or deck
                            player1.addItem(item)
                            notification_text = f"Purchased: {item.name}"
                            notification_timer = 120  # Show for 2 seconds (60 FPS)

                            # Replace the item with a new random one
                            new_item = shop.replace_item(item_type, player1)
                            if new_item:
                                item_button.setText(f"{new_item.name} - {new_item.price} gold")
                                # Update the item in the list
                                for i, (btn, itm, typ, prc) in enumerate(item_buttons):
                                    if btn == item_button:
                                        item_buttons[i] = (btn, new_item, item_type, new_item.price)
                                        break
                        else:
                            notification_text = "Not enough gold!"
                            notification_timer = 120  # Show for 2 seconds (60 FPS)

                # Check if the proceed button is clicked
                if ProceedButton.is_clicked(mouse_pos, event):
                    running = False

        # Update hover states
        ProceedButton.check_hover(mouse_pos)
        for item_button, _, _, _ in item_buttons:
            item_button.check_hover(mouse_pos)

        # ---- Draw ----
        # Draw background
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 30))  # Dark blue backdrop

        # Draw shop title
        font = pygame.font.SysFont("Arial", int(72 * scale))
        title_text = font.render("Merchant Shop", True, (255, 255, 255))
        screen.blit(title_text, (600 * scale, 50 * scale))

        # Draw item buttons
        for item_button, _, _, _ in item_buttons:
            item_button.draw(screen)

        # Draw player's gold
        gold_font = pygame.font.SysFont("Arial", int(36 * scale))
        gold_text = gold_font.render(f"Gold: {player1.gold}", True, (255, 215, 0))
        screen.blit(gold_text, (50 * scale, 50 * scale))

        # Draw notification text if active
        if notification_timer > 0:
            notification_font = pygame.font.SysFont("Arial", int(36 * scale))
            notification_render = notification_font.render(notification_text, True, (255, 255, 255))
            notification_rect = notification_render.get_rect(center=(screen.get_width() // 2, 550 * scale))
            screen.blit(notification_render, notification_rect)
            notification_timer -= 1

        # Draw proceed button
        ProceedButton.draw(screen)

        player1.displayDeck(screen)

        pygame.display.flip()
        clock.tick(60)

    return True

