

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
        self.disarmed_rounds = 0
        self.price=5
        self.m=False


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
        #print(f"Name: {self.name}, Type: {self.card_type}, Weight: {self.weight}, Description: {self.desc}, Attack Value: {self.Aval}, Defense Value (Light): {self.Dval}, Defense Value (Heavy): {self.D2val}, Heal Value: {self.Hval}, Trick Value: {self.Tval}")
        pass

    def _owner_hand(self, player, enemy):
        """Returns (index, is_player) for self's slot in whichever hand it's in."""
        for i, hb in enumerate(player.HandButtons):
            if hb.card is self:
                return i, True
        for i, c in enumerate(enemy.hand):
            if c is self:
                return i, False
        return None, None

    def _set_slot(self, player, enemy, is_player, idx, card):
        if is_player:
            player.HandButtons[idx].set_card(card)
        else:
            enemy.hand[idx] = card

    def _fall_off(self, player, enemy):
        """
        Simple fall-off: the card leaves its hand slot, which becomes a
        Nothing() card - full stop, that's the general rule.
        For the player specifically, try to swap the falling card into the
        first empty ('Nothing') slot in the deck, so it's just returned to
        storage rather than destroyed. If the deck has no empty slot to
        receive it, buffer it into player.graveyard instead so it isn't
        lost outright. The enemy has no deck, so its slot just becomes
        Nothing() directly.
        """
        idx, is_player = self._owner_hand(player, enemy)
        if idx is None:
            return

        if is_player:
            for db in player.DeckButtons:
                if db.card.name == "Nothing":
                    db.set_card(self)
                    player.HandButtons[idx].set_card(Nothing())
                    return
            # no empty deck slot available - buffer it in the graveyard
            player.graveyard.append(self)
            player.HandButtons[idx].set_card(Nothing())
        else:
            enemy.hand[idx] = Nothing()

    def _empty_slot(self, player, enemy):
        """Find an empty slot on self's own side. Returns (idx, is_player) or (None, None)."""
        _, is_player = self._owner_hand(player, enemy)
        hand = player.HandButtons if is_player else enemy.hand
        for i, c in enumerate(hand):
            card = c.card if is_player else c
            if card.name == "Nothing":
                return i, is_player
        return None, None

    # ---- the six tricks ----

    def trick_1_falls_off_after_action(self, oc, player, enemy):
        if self.Aval > 0 or oc.Aval > 0:
            self._fall_off(player, enemy)

    def trick_2_disarm(self, oc, player, enemy):
        if oc.name != "Nothing":
            oc.disarmed_rounds = max(oc.disarmed_rounds, 2)
            self.disarmed_rounds = max(self.disarmed_rounds, 2)

    def trick_3_returns_after_two_rounds(self, oc, player, enemy):
        self.pending_return = 2
        self._fall_off(player, enemy)

    def trick_4_breaks_after_second_heavy_hit(self, oc, player, enemy):
        if oc.card_type == "Heavy" and oc.Aval > 0:
            self.heavy_hits += 1
            if self.heavy_hits >= 2:
                self._fall_off(player, enemy)

    def trick_5_falls_off_after_dealing_damage(self, oc, player, enemy):
        if self.Aval > 0:
            defense = oc.get_defense(self.card_type == "Heavy")
            if self.Aval > defense:
                self._fall_off(player, enemy)

    def trick_6_spawn_knife(self, oc, player, enemy):
        idx, is_player = self._empty_slot(player, enemy)
        if idx is not None:
            self._set_slot(player, enemy, is_player, idx, Knife())


TRICKS = {
    1: Card.trick_1_falls_off_after_action,
    2: Card.trick_2_disarm,
    3: Card.trick_3_returns_after_two_rounds,
    4: Card.trick_4_breaks_after_second_heavy_hit,
    5: Card.trick_5_falls_off_after_dealing_damage,
    6: Card.trick_6_spawn_knife,
    7: None,  # Active ability - handled separately
}






'''
Trick list:
0 - no tricks
1 - falls off after defending / attacking
2 - disarms the opposing card for two rounds and itself if the opposing card is not empty
3 - returns to hand after two rounds
4 - breaks after second hit from heavy weapon
5 - falls of after hitting and dealing damage
6 - spawns knives if there is an empty spot 
7 - active ability
8 - only off battle item (healing potion) TO ADD LATER MAYBE
'''

class LongSword(Card):
    def __init__(self):
        super().__init__("Long Sword", "Heavy", 5, "'H': 5, ATK: 2, DEF: L1, H0.5", 2, 1, 0.5, 0, 0)
    def attack(self, oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)
    def defend(self,  oc, player, enemy):
        if oc.card_type=="Light":
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
        if oc.card_type=="Light":
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
        super().__init__("Bow", "Heavy", 6, "'H': 6, ATK: 2 (-1 arrow for 2 rounds) - even if halved!, DEF: L1, H0.5", 2, 0, 0, 0,0)
    def attack(self, oc, player, enemy):
        #if an arrow is in player eq then return 2

        #FIX THIS ###############################
        for i, card in enumerate(player.hand):
            if card.name=="Arrow":
                player.hand[i].disarmed_rounds = 2
                #Eq.append(Nothing())
                dmg = oc.defend(self, player, enemy)
                enemy.take_damage(dmg)
                return ####################################################### NAPRAW!

        return
                

    def defend(self, oc, player, enemy):
        if oc.card_type=="Light":
            return 0
        else:
            return  halved(oc)


class Arrow(Card):
    def __init__(self):
        super().__init__("Arrow", "Light", 2, "'L': 2, DEF: 0, L: recoile 1dmg atk, TRK: returns to hand after two rounds", 0, -1, 0, 0,3)
    def defend(self, oc, player, enemy):
        #find a way for recoil dmg - i dunno maybe put a player class for this function
        if oc.card_type=="Light":
            self.trick(oc, player, enemy) # 
        return oc.Aval # negative will mean 1 recoil dmg? - risky but it is a way to do it
    def trick(self, oc, player, enemy):
        dmg = 1
        if oc.Dval==0 and oc.Aval>0:
            enemy.take_damage(dmg)

class Crown(Card):
    def __init__(self):
        super().__init__("Crown", "Light", 2, "DEF: 1, TRK: falls off after defending the dmg", 0,1,1,0,1) #or falls of and gets back to player eq
    def defend(self, oc, player, enemy):
        self.trick(self, player, enemy)
        return 0
    def trick(self, oc, player, enemy):
        self.disarmed_rounds=-1 # -1 means it will be removed FOREVER from hand being hit

class HealingAmulet(Card):
    def __init__(self):
        super().__init__("Healing Amulet", "Light", 2, "DEF: 1, TRK: falls off after being attakced",0,0,0,1,9) #or falls of and gets back to player eq
    def defend(self, oc, player, enemy):
        self.trick(oc, player, enemy)
    def heal(self, oc, player, enemy):
        player.heal(1)
    def trick(self, oc, player, enemy):
        self.disarmed_rounds=-1 # -1 means it will be removed FOREVER from hand being hit

class Bandage(Card):
    def __init__(self):
        super().__init__("Bandage", "Light", 3, "HEAL: 2 TRK: falls after being used",0,0,0,2,1) #or falls of and gets back to player eq
        self.CanHeal=False
    def heal(self, oc, player, enemy):
        if oc==None:
            player.heal(self.Hval)
            self.trick(oc, player, enemy)
            return True
        return False
    def trick(self, oc, player, enemy):
        player.fallOff(self)

class FishingRod(Card):
    def __init__(self):
        super().__init__("Fishing rod", "Light", 3, "TRK: disarms oc and itself if oc is not empty",0,0,0,0,2) #or falls of and gets back to player eq

    def attack(self, oc, player, enemy):
        if oc.name!="Nothing":
            self.trick(oc, player, enemy)
    def trick(oc, player, enemy):
        oc.disarmed_rounds=3

class Helmet(Card):
    def __init__(self):
        super().__init__("Helmet", "Light", 3, "DEF: L1, H0", 0,1,0,0,0) 
    def defend(self, oc, player, enemy):
        if oc.card_type=="Light":
            return 0
        else:
            return oc.Aval

class ShoulderPlate(Card):
    def __init__(self):
        super().__init__("Shoulder Plate", "Light", 1, "DEF: L1, H0 TRK: falls off after defending",0,1,0,0,1) 
    def defend(self, oc, player, enemy):
        if oc.card_type=="Light":
            self.trick(oc, player, enemy)
            return 0
        else:
            return oc.Aval
    def trick(self, oc, player, enemy):
        self.disarmed_rounds=-1

class ChainMail(Card):
    def __init__(self):
        super().__init__("Chain Mail", "Light", 4, "DEF: L1, H0.5",0,1,0.5,0,4) 
        self.durability=2
    def defend(self, oc, player, enemy):

        if oc.card_type=="Light":
            return 0
        else:
            self.durability-=1
            if self.durability==0:
                self.disarmed_rounds=-1

            return oc.Aval

class Spear(Card):
    def __init__(self):
        super().__init__("Spear", "Heavy", 3, "ATK: 3, DEF: L0, H0",3,0,0,0,0) 
    def attack(self, oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)
        #here also trick trigger
        self.trick(oc, player, enemy)
    def trick(self, oc, player, enemy):
        self.disarmed_rounds=-1

class Dagger(Card):
    def __init__(self):
        super().__init__("Dagger", "Light", 2, "ATK: 1, DEF: L0, H0",2,0,0,0,5) 
    def attack(self, oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)
        if oc.Dval==0:
            self.trick(oc, player, enemy)
        #here also disarm trigger
    def trick(self, oc, player, enemy):
        self.disarmed_rounds=-1

class Knife(Card):
    def __init__(self):
        super().__init__("Knife", "Light", 1, "ATK: 1, DEF: L0, H0, TRK: falls off after atack",1,0,0,0,5) 
    def attack(self, oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        self.trick(oc, player, enemy)
        enemy.take_damage(dmg)
    def trick(self, oc, player, enemy):
        self.disarmed_rounds=-1 # -1 means it will be removed FOREVER from hand after attack
        pass

class MagicHat(Card):
    def __init__(self):
        super().__init__("Magic Hat", "Heavy", 3, "ATK: 0, DEF: L1, H0",0.1,1,0.5,0,6) 

    def attack(self, oc, player, enemy):
        self.trick(oc, player, enemy)

    def defend(self, oc, player, enemy):
        if oc.card_type=="Light":
            return 0
        else:
            return oc.Aval
    def trick(self, oc, player, enemy):

        for i, card in enumerate(player.hand):
            if card.name == "Nothing":
                # Replace the first Nothing() card with Knife()
                player.hand[i] = Knife()
                player.hand[i].m=True   # Assuming Cards.Knife() creates a Knife card
                player.sync_hand()  # Synchronize the hand after the change
                return  # Exit the function after the first replacement

    
class Club(Card):
    def __init__(self):
        super().__init__("Club", "Heavy", 7, "ATK: 3, DEF: L0, H0",3,0,0,0,0) 
    def attack(self, oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)
        #here also trick trigger

class HealingPotion(Card):
    def __init__(self):
        super().__init__("HealingPotion", "Heavy", 25, "HEAL: 5",0,0,0,5,0) 
    def heal(self, player):
        player.heal(self.Hval)


class Sword(Card):
    def __init__(self):
        super().__init__("Sword", "Heavy", 3, "'H': 5, ATK: 1, DEF: L1, H0", 1, 1, 0, 0, 0)
    def attack(self, oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)
    def defend(self,  oc, player, enemy):
        if oc.card_type=="light":
            return 0
        else:
            return  halved(oc)

class Boomerang(Card):
    def __init__(self):
        super().__init__("Light Axe", "Light", 2, "'L': 3, ATK: 1", 1, 0, 0, 0, 0)
    def attack(self,  oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)
        self.trick()

    def defend(self,  oc, player, enemy):
        if oc.card_type=="Light":
            return 0
        else:
            return  oc.Aval

    def trick(self,  oc, player, enemy):
        self.disarmed_rounds=2

class MagicMirror(Card):
    def __init__(self):
        super().__init__("Magic mirror", "Light", 4, "Simulater opposing card, ??", 0, 0, 0, 0, 8)
    def attack(self,  oc, player, enemy):
        dmg = oc.defend(oc, player, enemy) # tu jest w argumentach oc zamiast self i essa
        enemy.take_damage(dmg)


#we will be adding them simultaniously with enemies and dungeons
#but first I need to fix traps and knife falling off

# to add:
#magic mirror - reflecs stats of opposing cards - very rare item v
#healing potion - heal 5hp but cannot be used in fight
# spell book - if heavy dmg then blok and recoil 1 heavy dmg (item is light) (does not block light dmg)
# spell shield - blocks heavy dmg BUT NOT LIGHT
#
# magic eye - 3 dmg and if you hit it it has -1dmg when in defence (i dunno wether light or heavy tho maybe heavy)
#ritual knife - light axe but recover 1hp when oc is nothing
# knife pack - magic hat but when hit it falls off
# 
# poisonous gas - 1 dmg light bypassing everything
# gas buuble - recoil all things that attacks you
# magic mirror - stats same as oc
# fire - knife but heavy dmg (item is i dunno i would say heavy for fun)
#fireball - shield but spawns fire like magic hat
# rogi - 2 heavy dmg and shield
#trójząb - 3 light dmg
#sword of darkness - heavy item with 8 weightness but it a firery sword with shield defence with ritual dagger effect and 

# TRAP CARDS #################################################################
'''class Spike(Card):
    def __init__(self):
        super().__init__("Spike", "Light", 10, "ATK: 1, DEF: L0, H0",1,0,0,0,0) 
    def attack(self, oc, player, enemy):
        dmg = oc.defend(self, player, enemy)
        enemy.take_damage(dmg)
        #THIS IS A TRAP CARD ###################'''




#additional things - trinkets will be added in another file

class Nothing(Card):
    def __init__(self):
        super().__init__("Nothing", "Light", 0, "DEF: 0", 0,0,0,0,0)