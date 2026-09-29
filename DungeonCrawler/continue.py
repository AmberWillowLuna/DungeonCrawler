from GameLoop import GameLoop
import player
import SaveAndRead


def ContinueTheGame(screen):
    player = SaveAndRead.load_player()
    GameLoop.GameLoop(player)


