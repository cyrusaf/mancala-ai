from MancalaGUI import *
from Player import *

player1 = MancalaPlayer(1, Player.HUMAN)
player2 = MancalaPlayer(2, Player.MINIMAX, 2)
startGame(player1, player2)
