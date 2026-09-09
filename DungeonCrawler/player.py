
class Player:
    def __init__(self, name):
        self.name = name
        self.deck = [] #eq
        self.hand = [] #3 cards in fight
        self.field = [] # cards that will come back
        self.graveyard = [] # cards that are out of fight 
        self.life_points = 5
        self.gold=100


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
