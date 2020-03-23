import random
import numpy as np
import random
import collections
from game import Board, Game
from players.scripts.player_test import PlayerTest
from players.scripts.player_random import PlayerRandom
from players.scripts.vanilla_uct_player import Vanilla_UCT # Use this to replace the players.
from players.scripts.DSL import DSL
from players.scripts.data import Data
import sys
from copy import deepcopy
from  players.scripts.LinearPlayer import LinearPlayer
from players.scripts.Script import Script
from players.scripts.tree import Tree
from importlib import import_module
import os
import time


class MH():
    def __init__(self):
        self.dsl = DSL()
        self.tree = Tree(self.dsl)
        self.path = "C:\\Users\\Rohan\\Desktop\\cant-stop-assignment\\created_scripts\\"

    def proposal(self, id):
        # This method will return a sample script from the class Tree.
        rules = self.tree.change_tree()
        rules = [rules]
        script = Script(rules, id)
        script.saveFile(self.path)
        return rules

    def save_rules(self, run, rules):
        f_rules = open('best_rules.txt','a+')
        f_rules.write("Run " + str(run) + str(" -> "))
        f_rules.write(str(rules))
        f_rules.write("\n\n\n\n\n")
        f_rules.close()

    def m_h(self):
        start_time = time.time()
        path_final = "C:\\Users\\Rohan\\Desktop\\cant-stop-assignment\\players\\scripts\\"
        # Implement Metropolis-Hastings algorithm here.
        data = Data()
        all_rules = []
        # Retrieve the training data for the MH algorithm.
        training_data = data.generate_data()
        mid_time = time.time()
        print("Initial length -> ", len(training_data))
        script_id = 0
        score_prev = None
        n = 5
        time_log = open("time_log.txt",'a+')
        for i in range(n):
            simulation_rules = []
            best_id = 0
            best_score = 0
            best_score = 0
            simulation_correct_pairs = []
            simulation_scores = []
            best_rules = set()
            simulation_start_time = time.time()
            for _ in range(1000):
                sim_id = int(str(i) + "0" + str(_))
                rules = self.proposal(sim_id)
                script = import_module('created_scripts.Script' + str(sim_id))
                script_class = getattr(script, 'Script' + str(sim_id))
                player = script_class()
                # Use the training_data to get the action and then evaluate the cost function
                # Send the game states as inputs to the player script and then check for the output
                # Compare the output and evaluate the cost function.
                loss = 0
                correct_pairs = []
                for pair in training_data:
                    # print("Training pair ->", pair)
                    action = player.get_action(pair[0])
                    # print("action returned from player ->", action)
                    # print("Actual pair -> ",pair)
                    if action != pair[1]:
                        loss += 1
                    else:
                        correct_pairs.append(pair)
                score_curr = np.exp(-0.5 * loss)
                simulation_scores.append(score_curr)
                if loss == 0:
                    print("0 loss")
                # print("Current score for simulation -> ", _, " is ",  score_curr)
                alpha = None
                if score_prev is not None:
                    alpha = min(1, score_curr / score_prev)
                    # print("Score division is -> ", score_curr / score_prev)
                    if score_curr > score_prev:
                        best_id = _
                        best_score = score_curr
                else:
                    alpha = 1
                # print(alpha)
                accept = np.random.choice(['y','n'],p=[alpha, 1-alpha])
                # print("Accept -> ", accept)
                # print("Loss -> ", loss)
                # print("Score prev vs current -> ", score_prev, score_curr)

                if accept == 'y':
                    # Accept the program
                    # 'simulation_rules' contains the rules for that script.
                    simulation_rules.append(rules)
                    # Remove the pairs from the training data.
                    simulation_correct_pairs.append(correct_pairs)
                    score_prev = score_curr
                else:
                    simulation_rules.append([])
                    simulation_correct_pairs.append([])
                # if len(all_rules) > 4:
                #     break
                # os.remove(self.path + 'Script' + str(i) + '.py')
            print("best_id -> ", best_id)
            print("Best_score -> ", simulation_scores[best_id])
            best_score = max(simulation_scores)
            print("Max score -> ", best_score)
            all_rules.append(simulation_rules[best_id])
            for k in range(len(simulation_scores)):
                if simulation_scores[k] == best_score:
                    training_data = [i for i in training_data if i not in simulation_correct_pairs[k]]
                    best_rules.update(simulation_rules[k][0])
            simulation_end_time = time.time()
            time_log.write("Iteration " + str(i) + " -> " + str(simulation_end_time - simulation_start_time) + "\n\n")
            print("Length of dataset-> ", len(training_data))
            self.save_rules(i, best_rules)
            temp_id = int(str(i)+"0"+str(best_id))
            s = Script(simulation_rules[best_id], temp_id)
            s.saveFile(path_final)
            print("Simulation Scores -> ", i, len(simulation_scores),simulation_scores)
        end_time = time.time()
        time_log.write("Total time -> " + str(end_time - start_time) + "\n\n\n")
        time_log.close()
        return all_rules


mh = MH()
res = mh.m_h()
print("All rules -> ", res)
