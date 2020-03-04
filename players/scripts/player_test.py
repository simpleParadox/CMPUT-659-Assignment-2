from players.player import Player
from players.scripts.DSL import DSL
import numpy as np

class PlayerTest(Player):

    """
    This file contains a highly sophisticated script containing
    nested conditions.
    I will also try to add a chance where with a low
    probability, the test player will choose one of
    the extreme columns but most of the time will choose
    the center column for which the dice had the highest
    probability of appearing.
    
    Try to also add the probability of choosing the yes and
    the no action. - This is implemented.
    """
    def get_action(self, state):
        actions = state.available_moves()
        for a in actions:
            if DSL.actionWinsColumn(state, a):
                return a
            if DSL.isDoubles(a):
                return a
            if DSL.containsNumber(a, 6) or DSL.containsNumber(a, 2):
                if np.random.choice([0, 1], p=[0.6, 0.4]) > 0:
                    return a
            if DSL.isStopAction(a):
                # Return 'y' with 70% probability and 'n' with 30% probability.
                if DSL.hasWonColumn(state, a):
                    return 'n'
                else:
                    return 'y'
            
                
                
                     
        return actions[0]