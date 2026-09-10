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
