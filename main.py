from MancalaGUI import *
from Player import *

player1 = MancalaPlayer(1, Player.MINIMAX, 6)
player2 = MancalaPlayer(2, Player.ABPRUNE, 6)
startGame(player1, player2)
