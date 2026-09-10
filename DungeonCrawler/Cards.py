

from re import L


def halved(oc):
        if oc.name != "Bow":
            return oc.Aval
        return oc.Aval//2

# oc - opposing card !

class Card:
    def __init__(self, name, card_type, weight, desc, Aval, Dval, D2val, Hval, Tval):
        self.name = name
        self.card_type = card_type
        self.weight = weight
        self.desc = desc
        self.Aval = Aval
        self.Dval = Dval #light
        self.D2val = D2val #heavy
        self.Hval = Hval
        self.Tval = Tval


        #cards can be heavy or light
        #Tval describes the trick value of the card - when is it triggered maybe?
    def attack(self,  oc, player, enemy):
        # triggers every round
        pass
    def defend(self,  oc, player, enemy):
        # triggers when attacked
        return oc.Aval
    def heal(self,  oc, player, enemy):
        # if not attacked - may be triggered by player
        pass
    def trick(self,  oc, player, enemy):
        # triggers when a special condition is met - may be triggered by player
        pass
    def disp(self):
        print(f"Name: {self.name}, Type: {self.card_type}, Weight: {self.weight}, Description: {self.desc}, Attack Value: {self.Aval}, Defense Value (Light): {self.Dval}, Defense Value (Heavy): {self.D2val}, Heal Value: {self.Hval}, Trick Value: {self.Tval}")


'''
Trick list:
0 - no tricks
1 - falls off after defending / attacking
2 - disarms the opposing card for two rounds and itself if the opposing card is not empty
3 - returns to hand after two rounds
4 - breaks after second hit from heavy weapon
5 - falls of after hitting and dealing damage
6 - spawns knives if there is an empty spot 
'''

class LongSword(Card):
    def __init__(self):
        super().__init__("Long Sword", "Heavy", 5, "'H': 5, ATK: 2, DEF: L1, H0.5", 2, 1, 0.5, 0, 0)
    def attack(self, oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)
    def defend(self,  oc, player, enemy):
        if oc.card_type=="light":
            return 0
        else:
            return  halved(oc)


class Shield(Card):
    def __init__(self):
        super().__init__("Shield", "Light", 5, "'L': 5, DEF: 1", 0, 1, 1, 0, 0)
    def defend(self, oc, player, enemy):
        return halved(oc)

class Halbard(Card):
    def __init__(self):
        super().__init__("Halbard", "Heavy", 4, "'H': 4, ATK: 2, DEF: L1, H0", 2, 1, 0, 0, 0)
    def attack(self,  oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)
    def defend(self, oc, player, enemy):
        if oc.card_type=="light":
            return 0
        else:
            return oc.Aval


class LightAxe(Card):
    def __init__(self):
        super().__init__("Light Axe", "Light", 3, "'L': 3, ATK: 1", 1, 0, 0, 0, 0)
    def attack(self,  oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)

class Bow(Card):
    def __init__(self):
        super().__init__("Bow", "Heavy", 6, "'H': 6, ATK: 2 (-1 arrow for 2 rounds) - even if halved!, DEF: L1, H0.5", 2, 0, 0, 0,)
    def attack(self, oc, player, enemy):
        #if an arrow is in player eq then return 2
        #then throw out arrow out of eq for one round!
        #player : Eq - all equipement (max 12 items for example)
        # player. hand  - 3 cards in fight
        # player. off hand - cards that are in hand but where disarmed for example
        # player. off hand timer - timer to get back to hand
        for q in player.Hand:
            if q.name=="Arrow":
                player.Hand.remove(q)
                #Eq.append(Nothing())
                dmg = oc.defend(self, player, enemy)
                oc.take_damage(dmg)
            else:
                return 0
                

    def defend(self, oc, player, enemy):
        if oc.card_type=="light":
            return 0
        else:
            return  halved(oc)


class Arrow(Card):
    def __init__(self):
        super().__init__("Arrow", "Light", 2, "'L': 2, DEF: 0, L: recoile 1dmg atk, TRK: returns to hand after two rounds", 0, -1, 0, 0,3)
    def defend(self, oc, player, enemy):
        #find a way for recoil dmg - i dunno maybe put a player class for this function
        if oc.card_type=="light":
            self.trick(self, player, enemy) # 
        return oc.Aval # negative will mean 1 recoil dmg? - risky but it is a way to do it
    def trick(self, oc, player, enemy):
                #tu cos ten
        pass

class Crown(Card):
    def __init__(self):
        super().__init__("Crown", "Light", 2, "DEF: 1, TRK: falls off after defending the dmg", 0,1,1,0,1) #or falls of and gets back to player eq
    def defend(self, oc, player, enemy):
        self.trick(self, player, enemy)
        return 0
    def trick(self, oc, player, enemy):
        #breaks player.falls()
        pass

class HealingAmulet(Card):
    def __init__(self):
        super().__init__("Healing Amulet", "Light", 2, "DEF: 1, TRK: falls off after being attakced",0,0,0,1,1) #or falls of and gets back to player eq
    def defend(self, oc, player, enemy):
        self.trick(self, player, enemy)
    def heal(self, oc, player, enemy):
        return 1
    def trick(self, oc, player, enemy):
        #tu cos ten player.fall
        pass

class Bandage(Card):
    def __init__(self):
        super().__init__("Bandage", "Light", 3, "HEAL: 2 TRK: falls after being used",0,0,0,2,1) #or falls of and gets back to player eq
    def heal():
        return 2
    def trick():
        #tu cos ten zniszczyc player.falls
        pass

class FishingRod(Card):
    def __init__(self):
        super().__init__("Fishing rod", "Light", 3, "TRK: disarms oc and itself if oc is not empty",0,0,0,0,2) #or falls of and gets back to player eq

    def attack(self, oc, player, enemy):
        if oc.name!="Nothing":
            self.trick(self, player, enemy)
    def trick():
        #tu cos ten oc.disarm, player.fall off 
        pass

class Helmet(Card):
    def __init__(self):
        super().__init__("Helmet", "Light", 3, "DEF: L1, H0", 0,1,0,0,0) 
    def defend(self, oc, player, enemy):
        if oc.card_type=="light":
            return 0
        else:
            return oc.Aval

class ShoulderPlate(Card):
    def __init__(self):
        super().__init__("Shoulder Plate", "Light", 1, "DEF: L1, H0 TRK: falls off after defending",0,1,0,0,1) 
    def defend(self, oc, player, enemy):
        if oc.card_type=="light":
            self.trick(self, oc, player, enemy)
            return 0
        else:
            return oc.Aval
    def trick(self, oc, player, enemy):
        #tu cos ten player.falls()
        pass

class ChainMail(Card):
    def __init__(self):
        super().__init__("Chain Mail", "Light", 4, "DEF: L1, H0.5",0,1,0.5,0,4) 
    def defend(self, oc, player, enemy):
        if oc.card_type=="light":
            return 0
        else:
            return oc.Aval

class Spear(Card):
    def __init__(self):
        super().__init__("Spear", "Heavy", 3, "ATK: 3, DEF: L0, H0",3,0,0,0,0) 
    def attack(self, oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)
        #here also trick trigger

class Dagger(Card):
    def __init__(self):
        super().__init__("Dagger", "Light", 2, "ATK: 1, DEF: L0, H0",2,0,0,0,5) 
    def attack(self, oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        oc.take_damage(dmg)
        #here also disarm trigger
    def trick(self, oc, player, enemy):
        #tu cos ten oc.disarm, player.fall off 
        pass

class Knife(Card):
    def __init__(self):
        super().__init__("Knife", "Light", 1, "ATK: 1, DEF: L0, H0",1,0,0,0,2) 
    def attack(self, oc, player, enemy):
        self.trick(self, player, enemy)
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)
    def trick(self, oc, player, enemy):
        #tu cos ten oc.disarm, player.fall off 
        pass

class WizardHat(Card):
    def __init__(self):
        super().__init__("Wizard Hat", "Heavy", 3, "ATK: 0, DEF: L0, H0",0,1,0.5,0,6) 
    def defend(self, oc, player, enemy):
        if oc.card_type=="light":
            return 0
        else:
            return oc.Aval
    def trick(self, oc, player, enemy):
        #tu cos ten ze spawnem knifeów
        pass
    
class Club(Card):
    def __init__(self):
        super().__init__("Club", "Heavy", 6, "ATK: 3, DEF: L0, H0",3,0,0,0,0) 
    def attack(self, oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)
        #here also trick trigger




# TRAP CARDS #################################################################
'''class Spike(Card):
    def __init__(self):
        super().__init__("Spike", "Light", 10, "ATK: 1, DEF: L0, H0",1,0,0,0,0) 
    def attack(self, oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)
        #THIS IS A TRAP CARD ###################'''


# to add:
#magic mirror - reflecs stats of opposing cards - very rare item
#magic wand - rotates card for one round after reveal before resolution - then falls off, very rare item
#crown of thorns - takes 1dmg from player when opposing attacks (so def) but if enemy hits it it takes 4 dmg of light dmg recoil - very rare item
#machet and basic sword - to be added - basic items
#firery sword - rare item

#additional things - trinkets will be added in another file

class Nothing(Card):
    def __init__(self):
        super().__init__("Nothing", "Light", 0, "DEF: 0", 0,0,0,0,0) 
