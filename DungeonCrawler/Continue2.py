from GameLoop import GameLoop
import SaveAndRead


def ContinueTheGame(screen):
    player1 = SaveAndRead.load_player()
    GameLoop(screen, player1)


