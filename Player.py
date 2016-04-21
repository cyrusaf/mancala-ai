# File: Player.py
# Author(s) names AND netid's:
# Date:
# Group work statement: <please type the group work statement
#      given in the pdf here>
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *
import time
import heapq

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4

    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)

    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        start_time = time.time()

        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far

        dt = time.time() - start_time
        print "\n\nMINIMAX took " + str(dt) + " seconds"

        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score

    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        start_time = time.time()

        root_node = Node(Node.MAX, board, 0, None, None)
        best_node = root_node.bestMove(self)

        dt = time.time() - start_time
        print "\n\nAB took " + str(dt) + " seconds"

        #returns the score adn the associated moved
        return (best_node.score, best_node.move)

    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            val, move = self.customMove(board)
            print "chose move", move, "with value", val
            return move
        else:
            print "Unknown player type"
            return -1

    # ===== SELF DEFINED METHODS ===== #
    def oppCups(self, board):
        if self.num == 1:
            return board.P2Cups[::-1]
        elif self.num == 2:
            return board.P1Cups[::-1]

    def ownCups(self, board):
        if self.num == 1:
            return board.P1Cups
        elif self.num == 2:
            return board.P2Cups

    def oppScore(self, board):
        return board.scoreCups[self.opp-1]

    def ownScore(self, board):
        return board.scoreCups[self.num-1]
    # ================================ #


# Note, you should change the name of this player to be your netid
class MancalaPlayer(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board, depth=0):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        #print "Calling score in MancalaPlayer"

        if board.hasWon(self.num):
            return (100 - depth)
        if board.hasWon(self.opp):
            return -100 + depth

        return (self.ownScore(board) - self.oppScore(board))

    def bestMove(self, board):
        max_score = -INFINITY
        best_move = None
        for m in board.legalMoves(self):
            temp_board = deepcopy(board)
            temp_board.makeMove(self, m)

            score = self.score(temp_board)
            if score > max_score:
                max_score = score
                best_move = m

        return (max_score, best_move)

    def customMove(self, board):
        """ Choose the best move.  Returns (score, move) """
        open_list   = []
        closed_list = []

        best_score = -INFINITY
        best_node  = None

        n_operations   = 0

        root_node = Node(None, self, board, None, self.opp)
        open_list.append(root_node)
        heapq.heapify(open_list)

        start_time = time.time()
        print "=== " + str(self.num) + " ==="
        while len(open_list) > 0:
            # Check time
            if n_operations % 5000 == 0:
                dt = time.time() - start_time
                print dt, n_operations
                if dt > 1:
                    break

            # Check if node is best node
            node = heapq.heappop(open_list)
            node.evaluate(open_list)
            closed_list.append(node)

            # Update best_node
            print "Depth: ", node.depth, "; Own turn: ", node.turn==node.player.num, "; Score: ", node.score, "; Best Score: ", best_score
            if node.score > best_score:
                #print "Depth: ", node.depth, "; Own turn: ", node.turn==node.player.num, "; Score: ", node.score, "; Best Score: ", best_score
                best_score = node.score
                best_node  = node

            n_operations += 1

        scores = [best_node.score]
        if len(open_list) == 0:
            return(scores, best_node.move)

        while best_node.parent.parent is not None:
            best_node = best_node.parent
            scores.append(best_node.score)


        return (scores, best_node.move)

class Node():
    MAX = 0
    MIN = 1

    def __init__(self, node_type, board, depth, parent, move):
        self.type   = node_type
        self.board  = deepcopy(board)
        self.depth  = depth
        self.score  = -INFINITY
        self.parent = parent
        self.move   = move

    def minChild(self, player):
        opponent = MancalaPlayer(player.opp, player.type, player.ply)
        min_score = INFINITY
        min_node  = None

        for m in self.board.legalMoves(opponent):
            new_board = deepcopy(self.board)
            move_again = new_board.makeMove(opponent, m)

            node_type = self.type
            if not move_again:
                if node_type == Node.MIN:
                    node_type = Node.MAX
                else:
                    node_type = Node.MIN

            # Create and evaluate child
            child = Node(node_type, new_board, self.depth+1, self, m)
            child.evaluate(player)

            if child.score < min_score:
                min_score = child.score
                min_node  = child

        if min_node is None:
            print "========== ALERT ============"
            print min_score

        return min_node

    def maxChild(self, player):
        max_score = -INFINITY
        max_node  = None

        if len(self.board.legalMoves(player)) == 0:
            print self.board
        for m in self.board.legalMoves(player):
            new_board = deepcopy(self.board)
            move_again = new_board.makeMove(player, m)

            node_type = self.type
            if not move_again:
                if node_type == Node.MIN:
                    node_type = Node.MAX
                else:
                    node_type = Node.MIN

            # Create and evaluate child
            child = Node(node_type, new_board, self.depth+1, self, m)
            child.evaluate(player)

            if child.score > max_score:
                max_score = child.score
                max_node  = child

        if max_node is None:
            print "========== ALERT ============"
            print max_score

        #print "Max node score: ", max_node.score
        return max_node

    def evaluate(self, player):
        max_depth = player.ply

        if self.depth >= max_depth or self.board.gameOver():
            self.score = player.score(self.board)
            return self

        if self.type == Node.MAX:
            max_child = self.maxChild(player)
            #print " "*max_child.depth + "max_child: " + str(max_child.score)
            self.score = max_child.score
            return max_child

        elif self.type == Node.MIN:
            min_child = self.minChild(player)
            #print " "*min_child.depth + "min_child: " + str(min_child.score)
            self.score = min_child.score
            return min_child

    def bestMove(self, player):
        return self.evaluate(player)






# class Node():
#     # NEED TO EVALUATE OPPONENT BEST MOVE AND ONLY ADD SELF
#     def __init__(self, parent, player, board, move, turn):
#         self.player = player
#         self.board  = deepcopy(board)
#         self.parent = parent
#         self.turn   = turn
#
#         self.depth  = 0
#         self.move   = move
#         if parent is not None:
#             self.depth  = parent.depth + 1
#
#         if self.turn == self.player.num:
#             self.score = player.score(self.board, self.depth)
#         else:
#             player = MancalaPlayer(player.opp, player.type, player.ply)
#             self.score = player.score(self.board, self.depth)
#
#     def __cmp__(self, other):
#         return cmp(self.score, other.score)
#
#     def evaluate(self, open_list):
#         # If depth > max_depth, return early
#         max_depth = 20
#         if self.depth >= max_depth and (self.depth + self.player.num) % 2 == 0:
#             return
#
#         player = self.player
#         # Loop through all possible moves and add them to the open list
#         # if (player.num - 1) % 2 == 0:
#         #     player = MancalaPlayer(self.player.num, self.player.type, self.player.ply)
#
#         for m in self.board.legalMoves(player):
#             new_board = deepcopy(self.board)
#             move_again = new_board.makeMove(player, m)
#
#             turn = self.turn
#             if not move_again:
#                 if turn == 1:
#                     turn = 2
#                 else:
#                     turn = 1
#
#             # Create child node from new board
#             node = Node(self, self.player, new_board, m, turn)
#             #print "Node: ", node.player.num, node.score
#
#             # Add child node to open_list
#             heapq.heappush(open_list, node)
