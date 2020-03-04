from players.player import Player
from players.scripts.DSL import DSL
import numpy as np


class LinearPlayer(Player):
    def get_action(self, state):
        actions = state.available_moves()
        print("Actions: ", actions)
        for a in actions:
            if DSL.actionWinsColumn(state, a):
                return a
            if DSL.isDoubles(a):
                return a
            if DSL.containsNumber(a, (6,2)):
                return a
            if DSL.isStopAction(a):
                return a

        return actions[0]