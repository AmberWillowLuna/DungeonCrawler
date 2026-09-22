
import pygame
import button
import SettingHelp
import Cards

class Player:
    def __init__(self, name):
        self.name = name
        self.deck = [] #eq
        self.hand = [Cards.Nothing(), Cards.Nothing(), Cards.Nothing()] #3 cards in fight
        self.field = [] # cards that will come back
        self.graveyard = [] # cards that are out of fight 
        self.trinkets = []
        self.maxHp = 8
        self.hp = self.maxHp
        self.level = 0

        self.et = "p"
        self.DungeonLevel = 0
        self.AdvLevel = 0
        self.gold = 15
        scale = SettingHelp.get_scale()
        self.font  = pygame.font.SysFont("Arial", int(48 * scale))
        self.gold_text = self.font.render("Gold: "+str(self.gold), True, (255, 255, 255))
        self.kills = 0
        self.curD = ""
        self.maxweight=10
        self.HeartIcon = pygame.image.load("assets/heart.png")
        self.EmptyHeartIcon = pygame.image.load("assets/Eheart.png")
        #prescale icons by the scale factor
        self.HeartIcon = pygame.transform.scale(self.HeartIcon, (60*SettingHelp.get_scale(), 60*SettingHelp.get_scale()))
        self.EmptyHeartIcon = pygame.transform.scale(self.EmptyHeartIcon, (60*SettingHelp.get_scale(), 60*SettingHelp.get_scale()))
        self.regeneration = 0
        self.last_clicked_button = None
        self.wis = False
        self.wisdom = False
        self.timePerk = False
        self.scout = False
        self.income = 0
        self.Trinket_text = self.font.render("Trinkets: ", True, (255, 255, 255))

        self.sync_delay_start = 0
        self.sync_delay_active = False
        self.sync_delay_duration = 2000  #


        #buttons for displaying the deck
        #at the beggining 9 nothing cards and 3 nothing cards in hand!
        scale = SettingHelp.get_scale()
        self.DeckButtons = [
            button.CardButton(40*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(156*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(272*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(388*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(504*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(620*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(736*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(852*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(968*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1084*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1200*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1316*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1432*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1548*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1669*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1790*scale, 950*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing")
        ]


        self.HandButtons = [
            button.CardButton(690*scale, 750*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(910*scale, 750*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing"),
            button.CardButton(1130*scale, 750*scale, "Nothing", (200, 200, 200), (150, 150, 150), Cards.Nothing(), card_type="nothing")            
            ]

    def PickUp(self, trinket):
        self.trinkets.append(trinket)
        self.update_trinket_text()

    def update_trinket_text(self):
        """
        Updates the Trinket_text to display all trinket names in self.trinkets,
        each on a new line.
        """
        if not self.trinkets:
            self.Trinket_text = [self.font.render("Trinkets: None", True, (255, 255, 255))]
            return

        # Start with "Trinkets: " and add each trinket's name on a new line
        text_lines = ["Trinkets:"]
        for trinket in self.trinkets:
            text_lines.append(trinket.name)

        # Render each line separately
        self.Trinket_text = [
            self.font.render(line, True, (255, 255, 255))
            for line in text_lines
        ]

    def displayTrinkets(self, screen):
        scale = SettingHelp.get_scale()

        # Ensure Trinket_text is updated
        self.update_trinket_text()

        # Calculate position (adjust as needed)
        x_pos = 1500 * scale
        y_pos = 20 * scale

        # Blit each line of text onto the screen
        for line in self.Trinket_text:
            screen.blit(line, (x_pos, y_pos))
            y_pos += 45 * scale 

    def displayHp(self, screen):
        scale = SettingHelp.get_scale()
        for i in range(self.maxHp):
            if i < self.hp:
                screen.blit(self.HeartIcon, (40*scale + i*50*scale, 800*scale))
            else:
                screen.blit(self.EmptyHeartIcon, (40*scale + i*50*scale, 800*scale))

        screen.blit(self.gold_text, (200 * scale, 880 * scale))
        self.displayTrinkets(screen)



    def earn(self, val):
        self.gold+=val
        self.gold_text = self.font.render("gold: "+str(self.gold), True, (255, 255, 255))

    def MoveNextRoom(self):
        self.heal(self.regeneration)
        #if you have trinkets earn gold

    def earn_gold(self, amount):
        #make trinket bonuses!
        self.gold += amount
        #print(f"{self.name} earned {amount} gold! Total gold: {self.gold}")

    def ascend(self):

        #game is blocking on 14
        self.level += 1
        print(self.level)
        if self.level==15:
            self.level=0
            self.curD = ""
            self.DungeonLevel += 1
            if self.DungeonLevel==5:
                self.DungeonLevel=0
                self.AdvLevel += 1
                if self.AdvLevel==3:
                    self.AdvLevel=0


        self.gold += self.income
        self.heal(self.regeneration)

                    #game won!


        #print(f"{self.name} has ascended to level {self.level}!")

    def HandToDeck(self):
        for i in range(3):  # Loop from 0 to 2
            if i < len(self.hand):  # Ensure the index is within bounds
                card = self.hand[i]
                card.disarmed_rounds = 0
                #card.disarmed = 0
                if card.m == False:
                    self.addItem(card)
                self.hand[i] = Cards.Nothing()

        ####### FIELD TO DECK AS WELL #########
        for i in range(len(self.field)):
            card = self.field[i]
            card.disarmed_rounds = 0
            #card.disarmed = 0
            if card.m == False:
                    self.addItem(card)
            self.field[i] = Cards.Nothing()
            

        self.sync_hand()
        self.sync_deck()



    def graveyardToDeck(self):
        for g in self.graveyard:
            g.disarmed_rounds = 0
            g.disarmed = 0
            self.addItem(g)

        self.sync_deck()

        self.graveyard.clear()

        self.HandToDeck()

        #print(f"{self.name}'s graveyard has been returned to the deck.")

    def sync_deck(self):
        for i in range(len(self.DeckButtons)):
            self.DeckButtons[i].set_card(Cards.Nothing())

        for i in range(min(len(self.DeckButtons), len(self.deck))):
            self.DeckButtons[i].set_card(self.deck[i])

    def sync_hand(self):
        for i in range(min(len(self.HandButtons), len(self.hand))):
            self.HandButtons[i].set_card(self.hand[i])


    def take_damage(self, amount):
        self.hp -= amount
        #print(f"{self.name} took {amount} damage! Life points: {self.hp}")
        if self.hp <= 0:
            self.hp=0
            #print(f"{self.name} has lost the duel!")

    def fallOff(self, card):
        if card in self.hand:
            # Add the card to self.graveyard
            self.graveyard.append(card)

            # Find the index of the card in self.hand
            index = self.hand.index(card)
            # Remove the card from self.hand
            self.hand[index]= Cards.Nothing()
            self.sync_hand()




    def heal(self, amount):
        self.hp += amount
        if self.hp > self.maxHp:
            self.hp = self.maxHp
        #print(f"{self.name} has healed {amount} points! Life points: {self.hp}")

    def addItem(self, card):
        self.stripDeck()
        if len(self.deck)<=16:
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
        self.displayHp(screen)

        #DRAW HEARTS as hp - empty as lost and full as existing

    def displayHand(self, screen):
        for h in self.HandButtons:
            h.draw(screen)
        self.displayHp(screen)


    def SaveToJson(self):
        #file: player.json
        import json
        player_data = {
            "name": self.name,
            "deck": [card.name for card in self.deck],
            "hand": [card.name for card in self.hand],
            "field": [card.name for card in self.field],
            "graveyard": [card.name for card in self.graveyard],
            "hp": self.hp,
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
                    if btn.card.name == "HealingPotion":
                        btn.card.heal(self)
                        btn.set_card(Cards.Nothing())
                        # Update the corresponding card in self.hand or self.deck
                        self._sync_lists_from_buttons()
                        self.stripDeck()

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
                    self._sync_lists_from_buttons()

                    return

    def handle_equipment_delete(self, mouse_pos, event):
        """Call this once per event in your main loop.
        Works on right-click (mouse button 3).
        If the same button is clicked twice, it replaces it with Cards.Nothing().
        Only works on DeckButtons.
        Highlights the button with a red border on right-click."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right-click
            for btn in self.DeckButtons:
                if btn.is_Rclicked(mouse_pos, event):
                    # Highlight the button with a red border
                    btn.Rselected = True
                    btn.border_color = (255, 0, 0)  # Red border

                    # Check if the same button was already selected
                    if hasattr(self, 'last_clicked_button') and self.last_clicked_button == btn:
                        # Replace the card in the button with Cards.Nothing()
                        btn.set_card(Cards.Nothing())
                        # Update the corresponding card in self.deck
                        clicked_index = self.DeckButtons.index(btn)
                        if clicked_index < len(self.deck):
                            self.deck[clicked_index] = Cards.Nothing()
                        # Reset the last clicked button and border
                        self.last_clicked_button = None
                        btn.Rselected = False
                        btn.border_color = (0, 255, 0)  # Revert to green border
                    else:
                        # Store the clicked button for the next right-click
                        self.last_clicked_button = btn
                    return
            # If no button was clicked, reset the last clicked button and borders
            self.last_clicked_button = None
            for btn in self.DeckButtons:
                btn.Rselected = False
                btn.border_color = (0, 255, 0)  # Revert to green border

            self.stripDeck()


    def deselectAll(self):
        """Deselect all buttons in the deck and hand."""
        for btn in self.DeckButtons + self.HandButtons:
            btn.selected = False

    def handle_hand_click(self, mouse_pos, event, enemy):
        """Call this once per event in your fight loop."""
        all_buttons = self.HandButtons

        for btn in all_buttons:
            if btn.is_clicked(mouse_pos, event):
                # clicking an already-selected button unclicks it
                if btn.selected:
                    btn.selected = False
                    if btn.card.name == "Bandage" and self.hp < 8:
                        clicked_index = self.HandButtons.index(btn)
                        print(clicked_index)
                        # Check if clicked_index is within bounds of self.hand
                        if clicked_index < len(self.hand):
                            if clicked_index < len(enemy.hand):
                                oc = enemy.hand[clicked_index]
                                if oc.Aval <= 0:
                                    DidItHeal = btn.card.heal(None, self, None)
                                    if DidItHeal:
                                        btn.set_card(Cards.Nothing())
                                        self.hand[clicked_index] = Cards.Nothing()
                    return

                already_selected = [b for b in all_buttons if b.selected]

                if not already_selected:
                    btn.selected = True
                    return
                else:
                    other = already_selected
                    self._try_swap(other, btn)
                    other.selected = False
                    btn.selected = False
                    self._sync_lists_from_buttons()
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

    def stripDeck(self):
        # Create a new deck with only cards that are not "Nothing"
        self.deck = [card for card in self.deck if card.name != "Nothing"]
        self.sync_deck()

    def _sync_lists_from_buttons(self):
        """Keep self.deck / self.hand consistent with what the buttons now show."""
        
        self.deck = [b.card for b in self.DeckButtons if b.card.name != "Nothing"]
        self.hand = [b.card for b in self.HandButtons]


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
    player.hp = player_data["hp"]
    player.level = player_data["level"]
    player.DungeonLevel = player_data["DungeonLevel"]
    player.AdvLevel = player_data["AdvLevel"]
    player.gold = player_data["gold"]
    player.kills = player_data["kills"]
    player.curD = player_data["curD"]

    return player
