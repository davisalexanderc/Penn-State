import random
import chess
import math
import numpy as np
from collections import defaultdict
from chess_env import ChessEnv

class Node:
    def __init__(self, board, num_searches=1000, C=1.4, parent=None, action_taken=None):
        self.board = board
        self.num_searches = num_searches
        self.C = C
        self.parent = parent
        self.action_taken = action_taken
        
        self.children = []
        self.expandable_moves = list(board.legal_moves)
        
        self.visit_count = 0
        self.value_sum = 0
        
    def is_fully_expanded(self):
        """
        Check if the node is fully expanded.
        
        """
        return len(self.expandable_moves) == 0 and len(self.children) > 0
    
    def select(self):
        """
        Select the best child node based on the UCB1 formula.
        
        """

        best_child = None
        best_ucb = -np.inf
        
        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb
        
        return best_child
    
    def get_ucb(self, child):
        """
        Get the UCB1 value for a child node.
        
        """
        q_value = (child.value_sum / child.visit_count)
        return q_value + self.C * math.sqrt(math.log(self.visit_count) / child.visit_count)
    
    def expand(self):
        """
        Expand the node by adding a child node.
        
        """
        action = random.choice(self.expandable_moves)
        self.expandable_moves.remove(action)
        
        child_board = self.board.copy()
        child_board.push(action)
        
        child = Node(child_board, self.num_searches, self.C, self, action)
        self.children.append(child)
        return child
    
    def simulate(self):
        """
        Simulate a game from the current node.
        
        """
        value, is_terminal = ChessEnv().get_value_and_terminated(self.board, self.action_taken)
        
        if is_terminal:
            return value
        
        rollout_board = self.board.copy()
        rollout_player = chess.WHITE
        
        while True:
            valid_moves = list(rollout_board.legal_moves)
            action = random.choice(valid_moves)
            rollout_board.push(action)
            value, is_terminal = ChessEnv().get_value_and_terminated(rollout_board, action)
            if is_terminal:
                return value
            
            rollout_player = ChessEnv().get_opponent(rollout_player)
            
    def backpropagate(self, value):
        """
        Backpropagate the value of a simulation.
        
        args:
        value (float): The value of the simulation.

        """
        self.value_sum += value
        self.visit_count += 1
        
        value = -value
        if self.parent is not None:
            self.parent.backpropagate(value)
            

class MCTS:
    """
    A class for the Monte Carlo Tree Search model.
    
    """
    def __init__(self, board, num_searches=1000, C=1.4):
        self.board = board
        self.num_searches = num_searches
        self.C = C
        
    def search(self):
        """
        Perform the MCTS search.
        
        """
        # define root
        root = Node(self.board, self.num_searches, self.C)
        
        for _ in range(self.num_searches):
            node = root
            
            # selection
            while node.is_fully_expanded():
                node = node.select()
            
            value, is_terminal = ChessEnv().get_value_and_terminated(node.board, node.action_taken)
            
            if not is_terminal:
                node = node.expand()
                value = node.simulate()
                
            node.backpropagate(value)
            
        best_child = max(root.children, key=lambda c: c.visit_count)
        return best_child.action_taken
