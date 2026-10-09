# Dungeon Crawler

A point-and-click dungeon crawler where **cards are your weapons**. Walk through six dungeons, collect gold and trinkets, and fight enemies by arranging a three-card hand under a strict weight limit.

Built with Python and [pygame](https://www.pygame.org/).

<!-- Add a screenshot or GIF here, e.g. ![Battle screen](docs/battle.png) -->

## Table of contents

- [Features](#features)
- [How to play](#how-to-play)
- [Combat](#combat)
- [Dungeons](#dungeons)
- [Cards](#cards)
- [Trinkets](#trinkets)
- [Controls](#controls)
- [Getting started](#getting-started)
- [Saving and progress](#saving-and-progress)
- [Project structure](#project-structure)

## Features

- **Card-based combat.** Every weapon, shield and healing item is a card with its own weight, damage type and special effect.
- **Weight-limited loadout.** Your hand holds 3 cards with a combined weight of at most **10**, and at most **one** of them can be **Heavy**.
- **Six dungeons in three tiers**, each with five enemy types and its own traps, merchant stock and background art.
- **Random room choices.** At every step you pick left, forward or right, and each path leads to an enemy, trap, merchant, trinket or empty room.
- **Merchants, traps and trinkets** to keep each run varied.
- **Three starting classes** (Barbarian, Paladin, Ranger).
- **Encyclopedia and weapon pedia** that fill in as you meet enemies and collect cards.
- **Save and continue**, with mouse-only or keyboard-only controls.
- **Configurable display** (640x360, 1280x720 or 1920x1080; windowed or fullscreen).

## How to play

**Goal:** clear all 6 dungeons to win.

1. Choose **Start**, then **New Game**, and pick a starting set:

   | Class | Starting cards |
   |-------|----------------|
   | Barbarian | Light Axe, Helmet |
   | Paladin | Sword |
   | Ranger | Bow, Arrow |

   Every class also starts with a Bandage.

2. Each dungeon has **15 rooms**. In every room you choose one of three paths (left, forward, right). The room types are:

   | Room | What happens |
   |------|--------------|
   | Enemy (Lv 1 to 5) | A fight. Level 5 is the dungeon boss. |
   | Trap | A one-round fight against trap cards. You never see which trap is ahead, so choose your hand carefully. |
   | Merchant | Spend gold on weapons, armor, healing items and potions. |
   | Trinket | Take or skip a permanent bonus item (one per dungeon). |
   | Empty | Nothing happens. |
   | Exit | Fully heals you and leads to the next dungeon. |

3. Every room you pass earns you gold (if you carry income trinkets) and regenerates HP (if you carry a regeneration trinket).
4. If your HP reaches 0, the run is over and your save is reset. Beat the final dungeon and you see the ending screen.

Within one row of three paths the room types are fixed, but which direction leads where is shuffled, so you can't memorise the doors.

## Combat

You fight with a **hand of 3 cards**, and the enemy has 3 cards too. Cards are matched **lane by lane** (left vs left, middle vs middle, right vs right).

### Choosing your hand

Before each fight you arrange your hand from your deck (16 slots). The hand is valid only if:

- the **total weight is 10 or less**, and
- **no more than one card is Heavy**.

Invalid swaps are rejected. Once the fight starts your hand is locked in, and you can only reorder the three cards between rounds.

### Rounds

1. Press **Fight**. The enemy's hand is shuffled and hidden until the round resolves.
2. All three lanes resolve: attacks, then healing, then card tricks.
3. Reorder your hand if you want, then fight again. The enemy hand is hidden again after each reorder.
4. The fight ends when you or the enemy reach 0 HP.

### Light and Heavy

Every card is either **Light** or **Heavy**, and defensive cards treat the two differently. For example, a Helmet stops Light hits but not Heavy ones, a Spell Shield stops Heavy hits but not Light ones, and a Shield stops both. Hover over a card to see its details.

### Falling off, disarming and destroyed cards

- Some cards **fall off** after use (Knife, Fire, Spear, Poisonous Gas, Dagger and others).
- Others can be **disarmed** by an opposing card (for example Fishing Rod) and come back a few rounds later.
- Cards that fall off during a fight **return to your deck after the fight**.
- A **Destroy Item trap** can remove a card from your hand for good, so be careful what you bring.

### Rewards

- **Gold:** enemies pay out by level (Lv 1 = 3, Lv 2 = 5, Lv 3 = 8, Lv 4 = 13, Lv 5 = 21).
- **Loot:** an enemy usually has a 1-in-2 chance of dropping one of the cards from its own hand.

## Dungeons

There are three tiers with two dungeons each. The order of the two dungeons within a tier is randomised every run.

| Tier | Dungeons | Enemies (Lv 1 to 5, boss last) |
|------|----------|-------------------------------|
| Easy | **Orc's dungeon** | Goblin, Orc, Armored Orc, Ogre, Orc Wizard |
| | **Misty's dungeon** | Slime, Dark Creature, Skeleton, Ghoul, Misty Ghost |
| Medium | **Library dungeon** | Librarian, Demonic Eye, Three-Eyed Beast, Trophy Hunter, Arcane Guardian |
| | **Forest dungeon** | Gremlin, Fungis, Ent, Tree of Life, Forest Spirit |
| Hard | **Darkness dungeon** | Shadow, Darkness Ghoul, Dark Knight, Darkness Sorcerer, Lich |
| | **Hell dungeon** | Lava Larva, Lava Golem, Fiery Spirit, Demon, Satan |

### Layout of a dungeon

Each dungeon follows the same 15-room structure:

- Rooms 1 to 5: Level 1 and 2 enemies, an empty room and traps
- Room 6: **Merchant**
- Rooms 7 to 9: Level 2 and 3 enemies, empty rooms and traps
- Room 10: **Trinket**
- Rooms 11 and 12: Level 3 and 4 enemies and a trap
- Room 13: **Merchant**
- Room 14: **Boss** (Level 5)
- Room 15: **Exit** (full heal)

### Merchants

Each merchant offers 2 weapons, 1 armor, 1 healing item and 1 potion, drawn from a stock that depends on the current dungeon. Prices go up as you progress deeper into the game.

## Cards

There are 35+ cards. Highlights, grouped by role:

| Role | Cards |
|------|-------|
| Heavy weapons | Sword, Long Sword, Halberd, Club, Spear (one use), Magic Eye, Fiery Sword, Devil Horns, Sword of Darkness |
| Light weapons | Light Axe, Machete, Dagger, Knife, Boomerang, Trident, Ritual Knife (heals on hit), Poisonous Gas (unblockable) |
| Ranged | Bow (needs an Arrow in your hand), Arrow |
| Armor and defense | Helmet, Shoulder Plate, Chain Mail, Shield, Spell Shield, Spell Book, Crown, Gas Bubble |
| Spawners and utility | Magic Hat and Knife Pack (spawn a Knife in an empty slot), Fireball (spawns Fire), Fishing Rod (disarms the opposing card), Magic Mirror (copies the opposing card) |
| Healing | Bandage, Healing Amulet, Healing Potion |

- **Bandage** heals 2 HP when the opposing card isn't attacking.
- **Healing Potion** heals 5 HP and can only be used outside of fights. It is too heavy to ever fit into a hand.
- Some cards are discovered only in specific dungeons. Check the **Weapons** page in the main menu to see what you have found.

## Trinkets

One trinket is waiting in each dungeon, and you can take it or skip it. The first three dungeons offer three random picks from the first group, and the last three offer three random picks from the second group.

| Group | Trinket | Effect |
|-------|---------|--------|
| 1 | Ring of Life | +1 max HP |
| 1 | Ring of Thief | +2 gold per room |
| 1 | Ring of Wisdom | Warns you when a side path is a trap |
| 1 | Regen Ring | +1 HP per room |
| 2 | Life Gem | +3 max HP |
| 2 | Thief's Bracelet | +4 gold per room |
| 2 | Magical Clock | Reroll a merchant's stock once per visit |
| 2 | Owl Totem | Always shows what is in the room ahead |

## Controls

The game can be played with the mouse alone, the keyboard alone, or a mix of both.

### Moving through the dungeon

| Action | Mouse | Keyboard |
|--------|-------|----------|
| Go left / forward / right | Click the on-screen button | `A` / `W` / `D` |
| Save and exit | Click **Save and Exit** | `X` |

### Managing cards

| Action | Mouse | Keyboard |
|--------|-------|----------|
| Swap two cards (deck or hand) | Click one card, then another | `Q` / `E` to move the cursor, `Space` to select and swap |
| Use a Healing Potion (outside fights) | Click it twice | Select it, then `Space` |
| Delete a card from your deck | Right-click it twice | `Backspace` twice |
| Inspect a card | Hover over it | Move the cursor onto it |

### In battle

| Action | Mouse | Keyboard |
|--------|-------|----------|
| Fight a round | Click **Fight** | `Space` |
| Use a Bandage | Double-click it | `H` |
| Confirm Ready / continue | Click the button | `2` |

## Getting started

### Requirements

- Python 3
- [pygame](https://pypi.org/project/pygame/)

### Install and run

```bash
git clone https://github.com/AmberWillowLuna/DungeonCrawler.git
cd DungeonCrawler/DungeonCrawler

pip install pygame
python DungeonCrawler.py
```

> **Important:** run the game from inside the inner `DungeonCrawler/` folder. Assets and save files are loaded with relative paths, so starting it from anywhere else will fail to find them.

### Display settings

The default is a 1920x1080 window. Open **Options** in the main menu to switch between 640x360, 1280x720 and 1920x1080, and between windowed and fullscreen. The choice is stored in `settings.json`.

### Building an executable (optional)

A PyInstaller spec is included:

```bash
pip install pyinstaller
pyinstaller DungeonCrawler.spec
```

The project can also be opened in Visual Studio through `DungeonCrawler.sln`.

## Saving and progress

- **Save and Exit** stores your deck, hand, HP, gold, dungeon progress and trinkets. **Continue** resumes exactly where you left off, including the dungeon order and which trinkets are still to be found.
- The game also auto-saves after every room.
- **Dying resets your run.** Discovered enemies and weapons stay unlocked.
- The main menu background changes after you have beaten the game once.
- To wipe everything (saved run, encyclopedia, weapon pedia and win state), run `EraseAllData.py` from the inner project folder.

| File | Purpose |
|------|---------|
| `player.json` | Current run |
| `dungeons.json` | Dungeon order for the current run |
| `Trinket.json` | Trinket order for the current run |
| `encyclopedia.json`, `weapon_pedia.json` | Unlocked enemies and cards |
| `state.json` | Whether you have won the game |
| `settings.json` | Resolution and window mode |

## Project structure

```
DungeonCrawler/
├── DungeonCrawler.sln
└── DungeonCrawler/
    ├── DungeonCrawler.py   # Entry point and main menu
    ├── start.py            # New game / Continue
    ├── SetPicker.py        # Starting class selection
    ├── GameLoop.py         # Dungeon navigation and room dispatch
    ├── EncounterLoops.py   # Battle and trap loops, round resolution
    ├── Cards.py            # All cards and their effects
    ├── enemies.py          # Enemy definitions
    ├── Trap.py             # Trap definitions
    ├── dungeons.py         # Dungeon class and 15-room layout
    ├── DungeonLoader.py    # Dungeon definitions and save/load of order
    ├── Merchant.py, Shop.py          # Merchant screen and stock
    ├── Trinkets.py, GetTrinkets.py   # Trinkets and pickup screen
    ├── Empty.py, Escape.py           # Empty and exit rooms
    ├── player.py           # Player, deck/hand rules, weight limit
    ├── SaveAndRead.py, Continue2.py, LoadHelper.py  # Saving and loading
    ├── Encyclopedia.py     # Enemy and weapon encyclopedia
    ├── Options.py, SettingHelp.py, Screen.py        # Settings and scaling
    ├── button.py, colors.py, Background.py          # UI helpers
    ├── EraseAllData.py     # Reset all saved data
    ├── *.json              # Saves, settings and unlock data
    └── assets/             # Card, enemy and dungeon art
```

## Tech

- Python 3
- pygame
