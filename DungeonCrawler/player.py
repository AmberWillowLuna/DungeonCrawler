import pygame
import button
import SettingHelp
import Cards

class Player:
    def __init__(self, name):
        self.name = name
        self.deck = [] #eq
        self.hand = [] #3 cards in fight
        self.field = [] # cards that will come back
        self.graveyard = [] # cards that are out of fight 
        self.life_points = 5
        self.level = 0
        self.DungeonLevel = 0
        self.AdvLevel = 0
        self.gold = 0
        self.kills = 0
        self.curD = ""
        self.maxweight=10



        #buttons for displaying the deck
        #at the beggining 9 nothing cards and 3 nothing cards in hand!
        scale = SettingHelp.get_scale()
        self.DeckButtons = [
            button.CardButton(40*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(260*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(470*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(690*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(910*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1130*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1350*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1570*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1790*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            ]
        self.HandButtons = [
            button.CardButton(690*scale, 750*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(910*scale, 750*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1130*scale, 750*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing")            
            ]



    def take_damage(self, amount):
        self.life_points -= amount
        #print(f"{self.name} took {amount} damage! Life points: {self.life_points}")
        if self.life_points <= 0:
            self.life_points=0
            #print(f"{self.name} has lost the duel!")

    def fallOff(self, card):
        if card in self.hand:
            self.hand.remove(card)
            self.graveyard.append(card)
            #print(f"{card} has fallen off the hand and is lost for the fight.")

    def addItem(self, card):
        if len(self.deck)<9:
            self.deck.append(card)
            #put in the first nothing card button the card
            for i in range(len(self.DeckButtons)):
                if self.DeckButtons[i].card.name=="Nothing":
                    self.DeckButtons[i] = button.CardButton(self.DeckButtons[i].rect.x, self.DeckButtons[i].rect.y, card.name, (200, 200, 200), (150, 150, 150), card, card_type=card.card_type)
                    break
        #print(f"{card} has been added to {self.name}'s deck.")

    def PlayCards(self, order):
        new_hand = []
        for o in order:
            if o == "a":
                new_hand.append(self.hand[0])
            elif o == "s":
                new_hand.append(self.hand[1])
            elif o == "d":
                new_hand.append(self.hand[2])
        self.hand = new_hand


    def displayDeck(self, screen):
        for d in self.DeckButtons:
            d.draw(screen)
        for h in self.HandButtons:
            h.draw(screen)

        #DRAW HEARTS as hp - empty as lost and full as existing


    def SaveToJson(self):
        #file: player.json
        import json
        player_data = {
            "name": self.name,
            "deck": [card.name for card in self.deck],
            "hand": [card.name for card in self.hand],
            "field": [card.name for card in self.field],
            "graveyard": [card.name for card in self.graveyard],
            "life_points": self.life_points,
            "level": self.level,
            "DungeonLevel": self.DungeonLevel,
            "AdvLevel": self.AdvLevel,
            "gold": self.gold,
            "kills": self.kills,
            "curD": self.curD
        }

        with open('player.json', 'w') as f:
            json.dump(player_data, f, indent=4)

    def handle_equipment_click(self, mouse_pos, event):
        """Call this once per event in your main loop."""
        all_buttons = self.DeckButtons + self.HandButtons

        for btn in all_buttons:
            if btn.is_clicked(mouse_pos, event):
                # clicking an already-selected button unclicks it
                if btn.selected:
                    btn.selected = False
                    return

                already_selected = [b for b in all_buttons if b.selected]

                if not already_selected:
                    btn.selected = True
                    return
                else:
                    other = already_selected[0]
                    self._try_swap(other, btn)
                    other.selected = False
                    btn.selected = False
                    return

    def _try_swap(self, btn1, btn2):
        """Attempt to swap the cards held by two buttons, enforcing hand rules."""
        card1 = btn1.card
        card2 = btn2.card

        in_hand_1 = btn1 in self.HandButtons
        in_hand_2 = btn2 in self.HandButtons

        # If either button lives in the hand, check what the hand would look like after the swap
        if in_hand_1 or in_hand_2:
            hypothetical_hand = [b.card for b in self.HandButtons]
            if in_hand_1:
                hypothetical_hand[self.HandButtons.index(btn1)] = card2
            if in_hand_2:
                hypothetical_hand[self.HandButtons.index(btn2)] = card1

            if not self._hand_is_valid(hypothetical_hand):
                #print("Swap rejected: hand would exceed weight or heavy-card limit.")
                return False

        # Passed checks (or doesn't touch the hand at all) -> perform swap
        btn1.set_card(card2)
        btn2.set_card(card1)

        self._sync_lists_from_buttons()
        return True

    def _hand_is_valid(self, hand_cards):
        total_weight = sum(c.weight for c in hand_cards if c.name != "Nothing")
        heavy_count = sum(1 for c in hand_cards if c.card_type == "heavy")
        return total_weight <= self.maxweight and heavy_count <= 1

    def handle_hand_reorder_click(self, mouse_pos, event):
        """
        For use DURING a fight: only lets you swap two cards within the
        hand itself. Deck (equipment) buttons are ignored here on purpose -
        swapping equipment in/out of the hand is only allowed outside of
        battle (via handle_equipment_click, e.g. in TrapLoop or the free
        Ready screen).
        """
        for btn in self.HandButtons:
            if btn.is_clicked(mouse_pos, event):
                if btn.selected:
                    btn.selected = False
                    return
                already = [b for b in self.HandButtons if b.selected]
                if not already:
                    btn.selected = True
                else:
                    other = already[0]
                    c1, c2 = other.card, btn.card
                    other.set_card(c2)
                    btn.set_card(c1)
                    other.selected = False
                    btn.selected = False
                return

    def _sync_lists_from_buttons(self):
        """Keep self.deck / self.hand consistent with what the buttons now show."""
        self.deck = [b.card for b in self.DeckButtons if b.card.name != "Nothing"]
        self.hand = [b.card for b in self.HandButtons if b.card.name != "Nothing"]


def LoadPlayerFromJson():
    import json
    with open('player.json', 'r') as f:
        player_data = json.load(f)

    player = Player(player_data["name"])
    # Assuming you have a way to convert card names back to card objects
    player.deck = [Cards.get_card_by_name(name) for name in player_data["deck"]]
    player.hand = [Cards.get_card_by_name(name) for name in player_data["hand"]]
    player.field = [Cards.get_card_by_name(name) for name in player_data["field"]]
    player.graveyard = [Cards.get_card_by_name(name) for name in player_data["graveyard"]]
    player.life_points = player_data["life_points"]
    player.level = player_data["level"]
    player.DungeonLevel = player_data["DungeonLevel"]
    player.AdvLevel = player_data["AdvLevel"]
    player.gold = player_data["gold"]
    player.kills = player_data["kills"]
    player.curD = player_data["curD"]

    return player