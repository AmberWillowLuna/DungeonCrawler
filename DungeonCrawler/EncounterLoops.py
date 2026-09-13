# EncounterLoops.py
import pygame
import button
import colors
import SettingHelp
import Cards

font = pygame.font.SysFont("Arial", 40)
desc_font = pygame.font.SysFont("Arial", 26)


def _build_enemy_display(enemy):
    """Build read-only CardButtons to show the enemy's hand, laid out in a row."""
    scale = SettingHelp.get_scale()
    buttons = []
    start_x = 680 * scale
    spacing = 220 * scale
    y = 240 * scale
    # EncounterLoops.py
import pygame
import button
import colors
import SettingHelp
import Cards

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


def _ensure_trick_state(card):
    """
    Some tricks (2, 3, 4) need to remember state across rounds
    (disarmed_rounds, pending_return, heavy_hits) but Card.__init__ in
    Cards.py doesn't set these up. Rather than editing Cards.py, stamp
    them onto the instance the first time we see it.
    """
    if not hasattr(card, "disarmed_rounds"):
        card.disarmed_rounds = 0
    if not hasattr(card, "heavy_hits"):
        card.heavy_hits = 0
    if not hasattr(card, "pending_return"):
        card.pending_return = 0


def _safe_call(fn, *args, label=""):
    """
    Call a card method defensively. A few cards in Cards.py currently have
    incomplete signatures (e.g. Bandage.heal()/trick(), FishingRod.trick(),
    WizardHat.trick() are all missing their 'self' parameter, and Bow's
    __init__ is missing its Tval argument) - one broken card shouldn't be
    able to crash the whole duel, so failures here are logged and skipped.
    """
    try:
        return fn(*args)
    except TypeError as e:
        print(f"[Battle] Skipped {label} (bad signature): {e}")
        return None
    except Exception as e:
        print(f"[Battle] Error in {label}: {e}")
        return None


def _resolve_round(player, enemy, log):
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
    for i in range(3):
        p_card = player.HandButtons[i].card if i < len(player.HandButtons) else Cards.Nothing()
        e_card = enemy.hand[i] if i < len(enemy.hand) else Cards.Nothing()

        _ensure_trick_state(p_card)
        _ensure_trick_state(e_card)

        p_active = p_card.disarmed_rounds <= 0
        e_active = e_card.disarmed_rounds <= 0

        e_hp_before = enemy.hp
        p_hp_before = player.life_points

        # --- attacks ---
        # NOTE: attack(oc, player, target) - "target" is whichever side
        # should take the damage, matching how each card's own attack()
        # method is already written (e.g. LongSword.attack does
        # enemy.take_damage(dmg) on whatever object is passed as the 3rd arg).
        if p_active and p_card.Aval > 0:
            _safe_call(p_card.attack, e_card, player, enemy, label=f"{p_card.name}.attack")

        if e_active and e_card.Aval > 0:
            _safe_call(e_card.attack, p_card, player, player, label=f"{e_card.name}.attack")

        if enemy.hp < e_hp_before:
            log.append(f"{p_card.name} hits {enemy.name} for {e_hp_before - enemy.hp}.")
        if player.life_points < p_hp_before:
            log.append(f"{e_card.name} hits you for {p_hp_before - player.life_points}.")

        # --- healing ---
        if p_card.Hval > 0:
            healed = _safe_call(p_card.heal, e_card, player, enemy, label=f"{p_card.name}.heal")
            if healed:
                player.life_points += healed
                log.append(f"{p_card.name} heals you for {healed}.")
        if e_card.Hval > 0:
            healed = _safe_call(e_card.heal, p_card, player, enemy, label=f"{e_card.name}.heal")
            if healed:
                enemy.hp += healed
                log.append(f"{e_card.name} heals {enemy.name} for {healed}.")

        # --- tricks (Tval used as the trick id, 1-6) ---
        if p_card.Tval in Cards.TRICKS:
            _safe_call(Cards.TRICKS[p_card.Tval], p_card, e_card, player, enemy,
                       label=f"{p_card.name}.trick_{p_card.Tval}")
        if e_card.Tval in Cards.TRICKS:
            _safe_call(Cards.TRICKS[e_card.Tval], e_card, p_card, player, enemy,
                       label=f"{e_card.name}.trick_{e_card.Tval}")

        if enemy.hp <= 0 or player.life_points <= 0:
            break

    # --- tick disarm timers for everything still in play ---
    for hb in player.HandButtons:
        _ensure_trick_state(hb.card)
        if hb.card.disarmed_rounds > 0:
            hb.card.disarmed_rounds -= 1
    for c in enemy.hand:
        _ensure_trick_state(c)
        if c.disarmed_rounds > 0:
            c.disarmed_rounds -= 1

    # --- bring back any cards whose pending_return has expired ---
    for c in list(player.graveyard):
        if getattr(c, "pending_return", 0) > 0:
            c.pending_return -= 1
            if c.pending_return <= 0:
                for hb in player.HandButtons:
                    if hb.card.name == "Nothing":
                        hb.set_card(c)
                        player.graveyard.remove(c)
                        break
    if hasattr(enemy, "graveyard"):
        for c in list(enemy.graveyard):
            if getattr(c, "pending_return", 0) > 0:
                c.pending_return -= 1
                if c.pending_return <= 0:
                    for i, slot in enumerate(enemy.hand):
                        if slot.name == "Nothing":
                            enemy.hand[i] = c
                            enemy.graveyard.remove(c)
                            break

    # NOTE: hand is NOT refilled from the deck during battle. You choose
    # your hand beforehand (in BattleLoop's Ready screen); if a card falls
    # off mid-fight, that slot just stays Nothing() for the rest of the
    # battle. Equipment swapping only happens outside of Battle().

    player._sync_lists_from_buttons()


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
        800 * scale, 550 * scale, 300 * scale, 100 * scale,
        "Fight", (100, 0, 0), (200, 0, 0)
    )

    enemy_buttons = _build_enemy_display(enemy)
    revealed = False
    log = []
    result = None

    while result is None:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                if FightButton.is_clicked(mouse_pos, event):
                    enemy.ShuffleHand()
                    log = []
                    _resolve_round(player1, enemy, log)
                    enemy_buttons = _build_enemy_display(enemy)
                    revealed = True

                    if enemy.hp <= 0:
                        result = "win"
                    elif player1.life_points <= 0:
                        result = "lose"
                else:
                    # any click that isn't Fight is the player reordering
                    # their hand - re-hide the enemy so the next Fight is
                    # a blind placement again. Deck/equipment is NOT
                    # touchable here - that's locked in for the fight.
                    player1.handle_hand_reorder_click(mouse_pos, event)
                    revealed = False

        FightButton.check_hover(mouse_pos)
        for eb in enemy_buttons:
            eb.check_hover(mouse_pos)

        # ---- draw ----
        screen.fill((0, 0, 30))

        _draw_enemy_header(screen, enemy)

        if revealed:
            for eb in enemy_buttons:
                eb.draw(screen)
        else:
            for eb in enemy_buttons:
                pygame.draw.rect(screen, (60, 60, 60), eb.rect, border_radius=10)
                pygame.draw.rect(screen, colors.GREEN, eb.rect, 2, border_radius=10)

        for j, line in enumerate(log[-8:]):
            surf = desc_font.render(line, True, colors.WHITE)
            screen.blit(surf, (150 * scale, (500 + j * 26) * scale))

        FightButton.draw(screen)
        player1.displayDeck(screen)

        pygame.display.flip()
        clock.tick(60)

    # ---- end-of-battle screen ----
    end_msg = "VICTORY!" if result == "win" else "DEFEATED..."
    end_color = colors.GREEN if result == "win" else colors.RED
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


def _ensure_trick_state(card):
    """
    Some tricks (2, 3, 4) need to remember state across rounds
    (disarmed_rounds, pending_return, heavy_hits) but Card.__init__ in
    Cards.py doesn't set these up. Rather than editing Cards.py, stamp
    them onto the instance the first time we see it.
    """
    if not hasattr(card, "disarmed_rounds"):
        card.disarmed_rounds = 0
    if not hasattr(card, "heavy_hits"):
        card.heavy_hits = 0
    if not hasattr(card, "pending_return"):
        card.pending_return = 0


def _safe_call(fn, *args, label=""):
    """
    Call a card method defensively. A few cards in Cards.py currently have
    incomplete signatures (e.g. Bandage.heal()/trick(), FishingRod.trick(),
    WizardHat.trick() are all missing their 'self' parameter, and Bow's
    __init__ is missing its Tval argument) - one broken card shouldn't be
    able to crash the whole duel, so failures here are logged and skipped.
    """
    try:
        return fn(*args)
    except TypeError as e:
        print(f"[Battle] Skipped {label} (bad signature): {e}")
        return None
    except Exception as e:
        print(f"[Battle] Error in {label}: {e}")
        return None


def _resolve_round(player, enemy, log):
    """
    Resolves one full clash of player.hand vs enemy.hand, lane by lane
    (slot 0 vs 0, 1 vs 1, 2 vs 2). Uses each card's own attack/heal/trick
    implementation exactly as written in Cards.py - nothing here overrides
    or replaces card behaviour, it just calls it in the right order:
        1) attacks (Aval > 0 cards)
        2) healing (Hval > 0 cards)
        3) tricks (Tval is used as the trick id 1-6, matching the TRICKS
           dict and the numbered list above it in Cards.py)
    Then ticks disarm/return timers and refills empty player hand slots
    from the deck.
    """
    for i in range(3):
        p_card = player.HandButtons[i].card if i < len(player.HandButtons) else Cards.Nothing()
        e_card = enemy.hand[i] if i < len(enemy.hand) else Cards.Nothing()

        _ensure_trick_state(p_card)
        _ensure_trick_state(e_card)

        p_active = p_card.disarmed_rounds <= 0
        e_active = e_card.disarmed_rounds <= 0

        e_hp_before = enemy.hp
        p_hp_before = player.life_points

        # --- attacks ---
        # NOTE: attack(oc, player, target) - "target" is whichever side
        # should take the damage, matching how each card's own attack()
        # method is already written (e.g. LongSword.attack does
        # enemy.take_damage(dmg) on whatever object is passed as the 3rd arg).
        if p_active and p_card.Aval > 0:
            _safe_call(p_card.attack, e_card, player, enemy, label=f"{p_card.name}.attack")

        if e_active and e_card.Aval > 0:
            _safe_call(e_card.attack, p_card, player, player, label=f"{e_card.name}.attack")

        if enemy.hp < e_hp_before:
            log.append(f"{p_card.name} hits {enemy.name} for {e_hp_before - enemy.hp}.")
        if player.life_points < p_hp_before:
            log.append(f"{e_card.name} hits you for {p_hp_before - player.life_points}.")

        # --- healing ---
        if p_card.Hval > 0:
            healed = _safe_call(p_card.heal, e_card, player, enemy, label=f"{p_card.name}.heal")
            if healed:
                player.life_points += healed
                log.append(f"{p_card.name} heals you for {healed}.")
        if e_card.Hval > 0:
            healed = _safe_call(e_card.heal, p_card, player, enemy, label=f"{e_card.name}.heal")
            if healed:
                enemy.hp += healed
                log.append(f"{e_card.name} heals {enemy.name} for {healed}.")

        # --- tricks (Tval used as the trick id, 1-6) ---
        if p_card.Tval in Cards.TRICKS:
            _safe_call(Cards.TRICKS[p_card.Tval], p_card, e_card, player, enemy,
                       label=f"{p_card.name}.trick_{p_card.Tval}")
        if e_card.Tval in Cards.TRICKS:
            _safe_call(Cards.TRICKS[e_card.Tval], e_card, p_card, player, enemy,
                       label=f"{e_card.name}.trick_{e_card.Tval}")

        if enemy.hp <= 0 or player.life_points <= 0:
            break

    # --- tick disarm timers for everything still in play ---
    for hb in player.HandButtons:
        _ensure_trick_state(hb.card)
        if hb.card.disarmed_rounds > 0:
            hb.card.disarmed_rounds -= 1
    for c in enemy.hand:
        _ensure_trick_state(c)
        if c.disarmed_rounds > 0:
            c.disarmed_rounds -= 1

    # --- bring back any cards whose pending_return has expired ---
    for c in list(player.graveyard):
        if getattr(c, "pending_return", 0) > 0:
            c.pending_return -= 1
            if c.pending_return <= 0:
                for hb in player.HandButtons:
                    if hb.card.name == "Nothing":
                        hb.set_card(c)
                        player.graveyard.remove(c)
                        break
    if hasattr(enemy, "graveyard"):
        for c in list(enemy.graveyard):
            if getattr(c, "pending_return", 0) > 0:
                c.pending_return -= 1
                if c.pending_return <= 0:
                    for i, slot in enumerate(enemy.hand):
                        if slot.name == "Nothing":
                            enemy.hand[i] = c
                            enemy.graveyard.remove(c)
                            break

    # --- refill any empty player hand slots straight from the deck ---
    for hb in player.HandButtons:
        if hb.card.name == "Nothing":
            for db in player.DeckButtons:
                if db.card.name != "Nothing":
                    hb.set_card(db.card)
                    db.set_card(Cards.Nothing())
                    break

    player._sync_lists_from_buttons()


def Battle(screen, player1, enemy):
    """
    Battle resolution loop.

    - The player can freely rearrange their hand/deck (handle_equipment_click)
      while the enemy's hand is hidden (drawn as card backs).
    - Pressing "Fight" shuffles the enemy's hand, resolves one full round
      (see _resolve_round), and reveals what the enemy actually played.
    - As soon as the player touches their own hand/deck again, the enemy
      hand is hidden again, ready for another blind round.
    - Loops, checking HP after every round, until either side reaches 0.

    Returns "win" or "lose".
    """
    scale = SettingHelp.get_scale()
    clock = pygame.time.Clock()

    FightButton = button.Button(
        800 * scale, 550 * scale, 300 * scale, 100 * scale,
        "Fight", (100, 0, 0), (200, 0, 0)
    )

    enemy_buttons = _build_enemy_display(enemy)
    revealed = False
    log = []
    result = None

    while result is None:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                if FightButton.is_clicked(mouse_pos, event):
                    enemy.ShuffleHand()
                    log = []
                    _resolve_round(player1, enemy, log)
                    enemy_buttons = _build_enemy_display(enemy)
                    revealed = True

                    if enemy.hp <= 0:
                        result = "win"
                    elif player1.life_points <= 0:
                        result = "lose"
                else:
                    # any click that isn't Fight is the player managing
                    # their hand/deck - re-hide the enemy so the next
                    # Fight is a blind placement again
                    player1.handle_equipment_click(mouse_pos, event)
                    revealed = False

        FightButton.check_hover(mouse_pos)
        for eb in enemy_buttons:
            eb.check_hover(mouse_pos)

        # ---- draw ----
        screen.fill((0, 0, 30))

        _draw_enemy_header(screen, enemy)

        if revealed:
            for eb in enemy_buttons:
                eb.draw(screen)
        else:
            for eb in enemy_buttons:
                pygame.draw.rect(screen, (60, 60, 60), eb.rect, border_radius=10)
                pygame.draw.rect(screen, colors.GREEN, eb.rect, 2, border_radius=10)

        for j, line in enumerate(log[-8:]):
            surf = desc_font.render(line, True, colors.WHITE)
            screen.blit(surf, (150 * scale, (500 + j * 26) * scale))

        FightButton.draw(screen)
        player1.displayDeck(screen)

        pygame.display.flip()
        clock.tick(60)

    # ---- end-of-battle screen ----
    end_msg = "VICTORY!" if result == "win" else "DEFEATED..."
    end_color = colors.GREEN if result == "win" else colors.RED
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