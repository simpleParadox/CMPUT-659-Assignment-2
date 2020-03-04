import numpy as np
from players.scripts.Script import Script
from players.scripts.synthesizer import Synthesizer
from game import Board, Game
from importlib import import_module
import random
from players.scripts.player_test import PlayerTest
from players.scripts.LinearPlayer import LinearPlayer

class PlayerPart3():
    def __init__(self):
        self.script_rules = {}
    def get_scripts(self, n=5):
        # Use the synth object to get the rules
        synth = Synthesizer()
        player_scripts = []
        path = "C:\\Users\\Rohan\\Desktop\\cant-stop-assignment\\players\\scripts\\"
        for i in range(n):
            rules = synth.synthesize()
            script = Script(rules=rules, id=i)
            self.script_rules[i] = script.getRules()
            script.saveFile(path=path)
            player_scripts.append(path+"Script"+str(i)+".py")
        return player_scripts





def evaluate_gens(p=None):
    # This method evaluates the scripts after the evolutionary algorithm.
    if p is None:
        raise Exception()
    # The set p contains the id of the scripts.
    # Create a list to store the scores of each player.
    scores = [0 for temp in range(len(p))]
    # The range(len(p)) will return a list with the indexes of p. Eg. if p=[1,2,30001]
    # then i and j will have values in [0,1,2].
    p_list = list(p)
    rules_counter = [0 for _ in range(len(p_list))]
    for i in range(len(p_list)):
        for j in range(len(p_list)):
            if i != j:
                print("Scripts playing -> ", i, j)
                player1_script = import_module('players.scripts.Script'+str(p_list[i]))
                player2_script = import_module('players.scripts.Script'+str(p_list[j]))
                player1_class = getattr(player1_script, 'Script' + str(p_list[i]))
                player2_class = getattr(player2_script, 'Script' + str(p_list[j]))
                player1 = player1_class()
                player2 = player2_class()
                victories1 = 0
                victories2 = 0
                for _ in range(20):
                    game = Game(n_players=2, dice_number=4, dice_value=3, column_range=[2, 6],
                                offset=2, initial_height=1)

                    is_over = False
                    who_won = None

                    number_of_moves = 0
                    current_player = game.player_turn
                    while not is_over:
                        moves = game.available_moves()
                        if game.is_player_busted(moves):
                            if current_player == 1:
                                current_player = 2
                            else:
                                current_player = 1
                            continue
                        else:
                            if game.player_turn == 1:
                                chosen_play = player1.get_action(game)
                            else:
                                chosen_play = player2.get_action(game)
                            if chosen_play == 'n':
                                if current_player == 1:
                                    current_player = 2
                                else:
                                    current_player = 1
                            # These lines are commented out for a cleaner console.
                            # print('Chose: ', chosen_play)
                            # game.print_board()
                            game.play(chosen_play)
                            # game.print_board()
                            number_of_moves += 1

                            print()
                        who_won, is_over = game.is_finished()

                        if number_of_moves >= 200:
                            is_over = True
                            who_won = -1
                            print('No Winner!')

                    if who_won == 1:
                        victories1 += 1
                        scores[i] += victories1
                    if who_won == 2:
                        victories2 += 1
                        scores[j] += victories2
                rules_counter[i] = player1.get_counter_calls()
                rules_counter[j] = player2.get_counter_calls()
                # rules_counter[i] = player1.get_counter_calls()
                # rules_counter[j] = player2.get_counter_calls()
                # print('Player 1: ', victories1 / (victories1 + victories2))
                # print('Player 2: ', victories2 / (victories1 + victories2))

    return scores, rules_counter

def elite_scripts(fitness, e):
    elites = [int(_) for _ in range(len(fitness))]
    inds = [i for _,i in sorted(zip(fitness, elites), reverse=True)]
    return inds[:e]

def tournament(fitness, t):
    script_indices = [int(_) for _ in range(len(fitness))]
    # Select randomly
    first_list = np.random.choice(script_indices, t, replace=False)
    second_list = np.random.choice(script_indices, t, replace=False)
    first_fitness = [fitness[i] for i in first_list]
    second_fitness = [fitness[j] for j in second_list]
    p1 = [i for _,i in sorted(zip(first_fitness, first_list), reverse=True)][0]
    p2 = [j for _,j in sorted(zip(second_fitness, second_list), reverse=True)][0]

    # p1 and p2 are the indices of the best scripts from the tournament.
    return p1, p2

def crossover(p1_rules, p2_rules):
    # This method returns a new script(rules) with the crossover of the 'if' conditions of the parents.
    # First generate splits for both the scripts
    """
    One more thing that can be done is generate two scripts and
    then play them against each other. Return the best script. However, for simplicity,
    I am using the procedure described in the assignment pdf.
    """
    split_index1 = random.randint(0, len(p1_rules))
    split1 = p1_rules[0:split_index1 + 1]

    split_index2 = random.randint(0, len(p2_rules))
    split2 = p2_rules[split_index2:]

    for rule in split2:
        split1.append(rule)
    # child_script = Script(child_rules, id = child_id)

    # Return the rules of the child.
    print("split1 is->",split1)
    return split1


def mutate(child_rules, rate, id):
    mutated_rules = []
    has_mutated = False
    for i in range(len(child_rules)):
        # checking if mutation will happen
        synth = Synthesizer()
        if random.randint(0, 100) < rate * 100:
            has_mutated = True
            rule = synth.synthesize()
            # verify if mutation replaces old rule
            if random.randint(0, 100) < rate * 100:
                mutated_rules.append(rule[0])
            else:
                mutated_rules.append(child_rules[i])
                mutated_rules.append(rule[0])
        else:
            mutated_rules.append(child_rules[i])
    print("Mutated Rules ->", mutated_rules)
    script = Script(mutated_rules, id=id)
    path = "C:\\Users\\Rohan\\Desktop\\cant-stop-assignment\\players\\scripts\\"
    script.saveFile(path=path)
    return mutated_rules


def remove_unused_rules(plys, players_rules, rules_counter):
    path = "C:\\Users\\Rohan\\Desktop\\cant-stop-assignment\\players\\scripts\\"
    players = list(plys)
    new_rules = {}
    for sn in range(len(players)):
        rule_count = rules_counter[sn] # rule_count holds a list.
        temp_new_rules = []
        list_index = [i for i in range(len(rule_count))]
        # list_index = list_index[::-1]
        for c in list_index:
            prpsn_len = len(players_rules[players[sn]])
            if rule_count[c] > 0:
                if c < prpsn_len:
                    temp_new_rules.append(players_rules[players[sn]][c])
        new_rules[players[sn]] = temp_new_rules
        final_rules = []
        for new_rule in temp_new_rules:
            if new_rule not in final_rules:
                final_rules.append(new_rule)
        new_script = Script(final_rules, id=players[sn])
        new_script.saveFile(path=path)

    return players_rules
    # Now you have to save the file with the removed rules with the respective script_ids present in list 'players'.


def EZS(gens=5, n=10, elite=4, t=4, mutate_rate=0.5):
    generation_fitness_values = [] # This will hold the fitness values for the scripts in each generation (The scripts may not be the same).
    part3 = PlayerPart3()
    player_scripts = part3.get_scripts(n=n) # Initialize population of scripts.
    players = [int(i) for i in range(len(player_scripts))]
    c_id = ""
    # players_indexes = [int(script_id) for script_id in player_scripts]
    gen_fitness = None
    final_indexes = None
    for _ in range(gens):
        c_id = str(_)
        count = 0
        # Evaluate(P) where P is players. Note that the list 'players' contains the id of scripts.
        fitness_values, rules_counter = evaluate_gens(players)
        generation_fitness_values.append(fitness_values)
        """
        'players' is the collection of script ids after each generation
        'rules_counter' is the value of 'get_counter_calls'
        'part3.script_rules' contains all the rules for all the scripts keyed with the script_id.
        """

        updated_rules = remove_unused_rules(players, part3.script_rules, rules_counter)
        for key in updated_rules.keys():
            part3.script_rules[key] = updated_rules[key]

        elite_indexes = elite_scripts(fitness_values, elite)
        p_prime = set()
        p_prime = p_prime.union(elite_indexes)
        while len(p_prime) < len(players):
            count += 1
            c_id = str(_)
            c_id = c_id + "000" + str(count)
            # Here the fitness values are used to randomly select some scripts.
            # First I randomly select the scripts based on the fitness
            p1, p2 = tournament(fitness_values, t)
            # 'c' contains the rules after crossover from the parents.
            c = crossover(part3.script_rules[p1], part3.script_rules[p2])
            # Now the mutate operation
            # c_mutated contains the mutated rules with the id=int(c_id)
            c_mutated = mutate(c, mutate_rate, id=int(c_id))
            part3.script_rules[int(c_id)] = c_mutated
            # Insert the mutated script id into p_prime
            p_prime = p_prime.union([int(c_id)])

        players = p_prime

        # The following line is added to remove the __pycache__ file to avoid conflicts.
    # shutil.rmtree("C:\\Users\\Rohan\\Desktop\\Coursework\\Winter 2020\\CMPUT 659\\Assignment 1\\cant-stop-assignment\\__pycache__")

    gen_fitness, rules_counter = evaluate_gens(players)
    players = list(players)
        # Reusing the elite_scripts method to get the best script.
    # inds = [i for _, i in sorted(zip(gen_fitness, final_indexes), reverse=True)]
    best_script_index = elite_scripts(gen_fitness,1)[0]
    best_script_id = players[best_script_index]
    print("The best script after EZS is ->", "Script"+str(best_script_id))
    return generation_fitness_values, best_script_id
# What is the difference between elite functions and the evaluation function.


def compare_scripts(generation_fit_values, best_id):
    first_gen_best_id = elite_scripts(generation_fit_values, 1)[0]

    # Now basically play the game here.
    player1_script = import_module('players.scripts.Script' + str(first_gen_best_id))
    player2_script = import_module('players.scripts.Script' + str(best_id))
    player1_class = getattr(player1_script, 'Script' + str(first_gen_best_id))
    player2_class = getattr(player2_script, 'Script' + str(best_id))

    player1 = None
    player2 = None
    id1 = None
    id2 = None
    scores1 = []
    scores2 = []
    for g in range(2):
        # This for loop is to evaluate how each script performs when given the first chance to play.
        if(g==0):
            player1 = player1_class()
            player2 = player2_class()
            id1 = first_gen_best_id
            id2 = best_id
        else:
            player1 = player2_class()
            player2 = player1_class()
            id1 = best_id
            id2 = first_gen_best_id

        victories1 = 0
        victories2 = 0

        # A total of 100 matches are played where each player gets a chance to be the first player.
        for _ in range(100):
            game = Game(n_players=2, dice_number=4, dice_value=3, column_range=[2, 6],
                        offset=2, initial_height=1)

            is_over = False
            who_won = None

            number_of_moves = 0
            current_player = game.player_turn
            while not is_over:
                moves = game.available_moves()
                if game.is_player_busted(moves):
                    if current_player == 1:
                        current_player = 2
                    else:
                        current_player = 1
                    continue
                else:
                    if game.player_turn == 1:
                        chosen_play = player1.get_action(game)
                    else:
                        chosen_play = player2.get_action(game)
                    if chosen_play == 'n':
                        if current_player == 1:
                            current_player = 2
                        else:
                            current_player = 1
                    print('Chose: ', chosen_play)
                    game.print_board()
                    game.play(chosen_play)
                    game.print_board()
                    number_of_moves += 1

                    print()
                who_won, is_over = game.is_finished()

                if number_of_moves >= 200:
                    is_over = True
                    who_won = -1
                    print('No Winner!')

            if who_won == 1:
                victories1 += 1
            if who_won == 2:
                victories2 += 1
        print(victories1, victories2)
        if g == 0:
            scores1.append(victories1)
            scores2.append(victories2)
        else:
            scores1.append(victories2)
            scores2.append(victories1)
        # print('Player 1 with Script ID: ', id1, " -> ", victories1 / (victories1 + victories2))
        # print('Player 2 with Script ID: ', id2, " -> ", victories2 / (victories1 + victories2))

    return first_gen_best_id, scores1, scores2


def compare_user_scripts(best_script_id):

    # Now basically play the game here.
    player1_script = import_module('players.scripts.Script' + str(best_script_id))
    player1_class = getattr(player1_script, 'Script' + str(best_script_id))

    player1 = None
    player2 = None
    id1 = None
    id2 = None
    scores1 = []
    scores2 = []
    for g in range(2):
        # This for loop is to evaluate how each script performs when given the first chance to play.
        if g == 0:
            player1 = player1_class()
            player2 = LinearPlayer()
            id1 = best_script_id
            id2 = 'LinearPlayer'
        else:
            player1 = LinearPlayer()
            player2 = player1_class()
            id1 = 'LinearPlayer'
            id2 = best_script_id

        victories1 = 0
        victories2 = 0

        # A total of 100 matches are played where each player gets a chance to be the first player.
        for _ in range(100):
            game = Game(n_players=2, dice_number=4, dice_value=3, column_range=[2, 6],
                        offset=2, initial_height=1)

            is_over = False
            who_won = None

            number_of_moves = 0
            current_player = game.player_turn
            while not is_over:
                moves = game.available_moves()
                if game.is_player_busted(moves):
                    if current_player == 1:
                        current_player = 2
                    else:
                        current_player = 1
                    continue
                else:
                    if game.player_turn == 1:
                        chosen_play = player1.get_action(game)
                    else:
                        chosen_play = player2.get_action(game)
                    if chosen_play == 'n':
                        if current_player == 1:
                            current_player = 2
                        else:
                            current_player = 1
                    print('Chose: ', chosen_play)
                    game.print_board()
                    game.play(chosen_play)
                    game.print_board()
                    number_of_moves += 1

                    print()
                who_won, is_over = game.is_finished()

                if number_of_moves >= 200:
                    is_over = True
                    who_won = -1
                    print('No Winner!')

            if who_won == 1:
                victories1 += 1
            if who_won == 2:
                victories2 += 1
        print(victories1, victories2)
        if g == 0:
            scores1.append(victories1)
            scores2.append(victories2)
        else:
            scores1.append(victories2)
            scores2.append(victories1)
        # print('Player 1 with Script ID: ', id1, " -> ", victories1 / (victories1 + victories2))
        # print('Player 2 with Script ID: ', id2, " -> ", victories2 / (victories1 + victories2))

    return scores1, scores2


# 'generation_fitness_values' contains the fitness values for each generation.
# The values for the parameters can be changed here.
generation_fitness_values, best_script_id = EZS(n=10, elite=7,t=5, gens=4)


# Now the best_script will be compared to the initial generation. The games are
# played 3 times just to observe scores.
for i in range(3):
    first_gen_best_script, scores1, scores2 = compare_scripts(generation_fitness_values[0], best_script_id)
    print("The scores are for Script", first_gen_best_script, " -> ", scores1, " and for Script", best_script_id," -> ", scores2)
    # Storing the results of comparison of best_script and from the first generation.
    path_desktop = "C:\\Users\\Rohan\\Desktop\\cant-stop-assignment\\"
    file = open(path_desktop + 'results_gen_best.txt', 'a+')
    file.write("\n\n\n")
    file.write("Run")
    file.write(str(i))
    file.write("10,7,5,4")
    file.write("\n-----------------------")
    file.write("\nThe scores are for Script" + str(first_gen_best_script) + " -> " + str(scores1) + " and for Script" + str(best_script_id) + " -> " + str(scores2))
    file.write("\n-----------------------")
    file.close()
    # Comparing the best_script and the user script.
    s1, s2 = compare_user_scripts(best_script_id)
    print("The scores are for Script", best_script_id, " -> ", s1, " and for Script LinearPlayer", " -> ", s2)
    # Storing the results.

    file = open(path_desktop + 'results_best_users.txt', 'a+')
    file.write("\n\n\n")
    file.write("Run")
    file.write(str(i))
    file.write("10,7,5,4")
    file.write("\n-----------------------")
    file.write("\nThe scores are for Script" + str(best_script_id) + " -> " + str(s1) + " and for Script LinearPlayer" + " -> " + str(s2))
    file.write("\n-----------------------")
    file.close()

