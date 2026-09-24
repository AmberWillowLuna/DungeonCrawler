# EncounterLoops.py

import pygame
import button
import colors
import SettingHelp
import Cards
import Trap
import random

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
        enemy.HandButtons = buttons



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


def _resolve_round(player1, enemy, log):
    """
    Resolves one full clash of player.hand vs enemy.hand, lane by lane
    (slot 0 vs 0, 1 vs 1, 2 vs 2). Uses each card's own attack/heal/trick
    implementation exactly as written in Cards.py - nothing here overrides
    or replaces card behaviour, it just calls it in the right order:
        1) attacks (Aval > 0 cards)
        2) healing (Hval > 0 cards)
        3) tricks (Tval is used as the trick id 1-6, matching the TRICKS
           dict and the numbered list above it in Cards.py)
    Then ticks disarm/return timers. Hand slots emptied by a fall-off stay
    Nothing() for the rest of the battle - there is no refill from the deck
    mid-fight, since the hand is chosen beforehand and locked in for the fight.


    """
    e_hp_before = enemy.hp
    p_hp_before = player1.hp

    for i in range(3):
        p_card = player1.HandButtons[i].card
        e_card = enemy.hand[i]

        #_ensure_trick_state(p_card)
        #_ensure_trick_state(e_card)

        e_hp_before = enemy.hp
        p_hp_before = player1.hp

        # --- attacks ---
        # NOTE: attack(oc, player, target) - "target" is whichever side
        # should take the damage, matching how each card's own attack()
        # method is already written (e.g. LongSword.attack does
        # enemy.take_damage(dmg) on whatever object is passed as the 3rd arg).

        #IF CARD IS DISARMED IT IS IN FIELD (OR GRAVEYARD IF PERMANENTLY DISARMED)

        if p_card.Aval> 0:
            p_card.attack(e_card, player1, enemy)

        if e_card.Aval > 0:
            e_card.attack(p_card, enemy, player1)


        if enemy.hp < e_hp_before:
            log.append(f"{p_card.name} hits {enemy.name} for {e_hp_before - enemy.hp}.")
        if player1.hp < p_hp_before:
            log.append(f"{e_card.name} hits you for {p_hp_before - player1.hp}.")

    #PRZECHODZIMY JESZCZE RAZ ¯EBY SPRAWDZIÆ TRIKI
    for i in range(3):
        p_card = player1.HandButtons[i].card
        e_card = enemy.hand[i]



        # --- healing ---
        #Bandage
        if p_card.Hval > 0:
            if p_card.Tval==7:
                if e_card.Aval==0:
                    p_card.CanHeal=True
                else:
                    p_card.CanHeal=False
        if e_card.Hval > 0:
            if e_card.Tval==7:
                if p_card.Aval==0:
                    e_card.CanHeal=True
                else:
                    e_card.CanHeal=False
        #healing amulet - heals when not attacked
        if p_card.Hval > 0:
            if p_card.Tval==8:
                if e_card.Aval==0:
                    p_card.heal(e_card, player1, enemy)
                    log.append(f"{p_card.name} heals you for {p_card.Hval}.")


        if e_card.Hval > 0:
            if e_card.Tval==8:
                if p_card.Aval==0:
                    e_card.heal(p_card, enemy, player1)
                    log.append(f"{p_card.name} heals enemy for {p_card.Hval}.")



        ################# DISARMING SECTION ###############################
        #check if card is disarmed and getting it to graveyard or field
        if p_card.disarmed_rounds == -1:

            if p_card.m == False:
                player1.graveyard.append(p_card)
            player1.hand[i] = Cards.Nothing()


        if e_card.disarmed_rounds == -1:
            enemy.hand[i] = Cards.Nothing()

        #now check if some card is temporarly disarmed!
        if p_card.disarmed_rounds > 0:
            # put in field 
            player1.field.append(p_card)
            player1.hand[i] = Cards.Nothing()
            player1.hand_sync()

        if e_card.disarmed_rounds > 0:
            # put in field 
            enemy.field.append(e_card) 
            enemy.hand[i] = Cards.Nothing()

        # destruction trick
        if p_card.Tval == 4:
            # count hits and self destroy ( go to graveyard)
            if p_card.durability==0:
                player1.graveyard.append(p_card)
                player1.hand[i] = Cards.Nothing()
                player1.hand_sync()
                #player1.HandButtons[i].set_card(Cards.Nothing())
        #same for enemy cards

        if e_card.Tval == 4:
            if e_card.durability==0:
                enemy.hand[i] = Cards.Nothing()

        ######################################################


    for tcard in player1.field:
        tcard.disarmed_rounds -= 1
        if tcard.disarmed_rounds <= 0:
            for i, slot in enumerate(player1.hand):
                if slot.name == "Nothing":
                    player1.hand[i] = tcard
                    player1.hand_sync()
                    player1.field.remove(tcard)
                    break

    for tcard in enemy.field:
        tcard.disarmed_rounds -= 1
        if tcard.disarmed_rounds <= 0:
            for i, slot in enumerate(enemy.hand):
                if slot.name == "Nothing":
                    enemy.hand[i] = tcard
                    enemy.field.remove(tcard)
                    break




def Battle(screen, player1, enemy):
    """
    Battle resolution loop.

    Your hand is chosen BEFOREHAND, in BattleLoop's Ready screen - deck/
    equipment swapping is not available here. During the fight itself you
    may only swap two cards WITHIN your hand (reordering which lane they
    sit in), while the enemy's hand is hidden (drawn as card backs).

    - Pressing "Fight" shuffles the enemy's hand, resolves one full round
      (see _resolve_round), and reveals what the enemy actually played.
    - As soon as the player reorders their hand again, the enemy hand is
      hidden again, ready for another blind round.
    - Loops, checking HP after every round, until either side reaches 0.

    Returns "win" or "lose".
    """
    scale = SettingHelp.get_scale()
    clock = pygame.time.Clock()

    FightButton = button.Button(
        800 * scale, 500 * scale, 300 * scale, 100 * scale,
        "Fight", (100, 0, 0), (200, 0, 0)
    )
    WinButton = button.Button(
        800 * scale, 650 * scale, 300 * scale, 100 * scale,
        "Victory!", (100, 125, 0), (10, 155, 155)
    )

    _build_enemy_display(enemy)
    revealed = False
    log = []
    result = None
    end = True

    while end:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit





            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    print(enemy.hand)
                    print(enemy.field)
                    print("####################")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if FightButton.is_clicked(mouse_pos, event):
                    enemy.ShuffleHand()
                    player1.sync_hand()
                    player1.sync_delay_active = False
                    log = []
                    _resolve_round(player1, enemy, log)

                    revealed = True
                   
                    if player1.hp <= 0:
                        result = "lose"
                    elif enemy.hp <= 0:
                        result = "win"

                    player1.sync_delay_start = pygame.time.get_ticks()
                    _build_enemy_display(enemy)
                    player1.sync_delay_active = True


                elif WinButton.is_clicked(mouse_pos, event):
                        end = False
                else:
                    # any click that isn't Fight is the player reordering
                    # their hand - re-hide the enemy so the next Fight is
                    # a blind placement again. Deck/equipment is NOT
                    # touchable here - that's locked in for the fight.

                    player1.handle_hand_click(mouse_pos, event, enemy)
                    revealed = False

        current_time = pygame.time.get_ticks()

        # Check if the delay is active and if it has expired
        if player1.sync_delay_active:
            elapsed_time = current_time - player1.sync_delay_start
            if elapsed_time >= player1.sync_delay_duration:
                player1.sync_hand()
                player1.sync_delay_active = False

        FightButton.check_hover(mouse_pos)
        for eb in enemy.HandButtons:
            eb.check_hover(mouse_pos, screen)

        for hb in player1.DeckButtons:
            hb.check_hover(mouse_pos, screen)

        for hb in player1.HandButtons:
            hb.check_hover(mouse_pos, screen)

        # ---- draw ----
        screen.fill((0, 0, 30))

        _draw_enemy_header(screen, enemy)

        if revealed:
            for eb in enemy.HandButtons:
                eb.draw(screen)
        else:
            for eb in enemy.HandButtons:
                pygame.draw.rect(screen, (60, 60, 60), eb.rect, border_radius=10)
                pygame.draw.rect(screen, colors.GREEN, eb.rect, 2, border_radius=10)

        for j, line in enumerate(log[-8:]):
            surf = desc_font.render(line, True, colors.WHITE)
            screen.blit(surf, (150 * scale, (500 + j * 26) * scale))
        
        if result == None:
            FightButton.draw(screen)
        else:
            WinButton.draw(screen)
        player1.displayHand(screen)

        pygame.display.flip()
        clock.tick(60)

    loot = Cards.Nothing()
    if random.randint(1,enemy.lootChance)==1:
        loot = enemy.lootTable[random.randint(0,2)]
    player1.earn(enemy.prize)

    # ---- end-of-battle screen ----
    end_msg = f"VICTORY! You won: {loot.name}" if result == "win" else "DEFEATED..."
    end_color = colors.GREEN if result == "win" else colors.RED

    player1.graveyardToDeck()
    player1.addItem(loot)

    player1.stripDeck()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

        screen.fill((0, 0, 0))
        msg_surf = font.render(end_msg, True, end_color)
        msg_rect = msg_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(msg_surf, msg_rect)
        pygame.display.flip()
        clock.tick(60)

    return result



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

    PLAYER DOES NOT KNOW WHAT TRAP IS AHEAD OF HIM!!!
    this way the destroy card trap is effective

    """
    scale = SettingHelp.get_scale()
    clock = pygame.time.Clock()
    log = []
    ReadyButton = button.Button(
        800 * scale, 50 * scale, 300 * scale, 100 * scale,
        "Ready", (0, 100, 0), (0, 200, 0)
    )
    running = True
        # Player confirmed -> apply the trap's effect
    Trap.trigger(player1, trap, screen)  # assumes Trap has a .trigger(player) method; adjust to your Trap class
    #after trap is set 

    _build_enemy_display(trap)

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
            _resolve_round(player1, trap, log)
            if event.type == pygame.MOUSEBUTTONDOWN:
                #player1.handle_equipment_click(mouse_pos, event)
                if ReadyButton.is_clicked(mouse_pos, event):
                    running = False

        ReadyButton.check_hover(mouse_pos)

        # ---- draw ----
        screen.fill((30, 0, 0))  # dim red backdrop to signal danger
        for eb in trap.HandButtons:
            eb.draw(screen)


        ReadyButton.draw(screen)
        player1.displayHand(screen)

        pygame.display.flip()
        clock.tick(60)

    player1.graveyardToDeck()




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

    _build_enemy_display(enemy)
    # asset/enemy.name+"png"
    player1.stripDeck()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    print(enemy.hand)
                    print(player1.hand)
                    print("####################")
                    print(enemy.field)
                    print("####################")


            if event.type == pygame.MOUSEBUTTONDOWN:
                player1.handle_equipment_click(mouse_pos, event)
                player1.handle_equipment_delete(mouse_pos, event)
                if ReadyButton.is_clicked(mouse_pos, event):
                    running = False

        ReadyButton.check_hover(mouse_pos)
        for eb in enemy.HandButtons:
            eb.check_hover(mouse_pos, screen)  # purely cosmetic, they aren't clickable for swaps

        for hb in player1.DeckButtons:
            hb.check_hover(mouse_pos, screen)

        for hb in player1.HandButtons:
            hb.check_hover(mouse_pos, screen)
        # ---- draw ----
        screen.fill((0, 0, 30))  # dim blue backdrop for battle

        _draw_enemy_header(screen, enemy)
        for eb in enemy.HandButtons:
            eb.draw(screen)



        ReadyButton.draw(screen)
        player1.displayDeck(screen)
        player1.displayHand(screen)


        pygame.display.flip()
        clock.tick(60)

    # Player confirmed their set -> hand off to actual combat resolution
    Battle(screen, player1, enemy)
    return True


