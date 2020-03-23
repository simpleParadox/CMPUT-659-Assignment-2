from game import Board, Game
from players.scripts.vanilla_uct_player import Vanilla_UCT
from copy import deepcopy

class Data:
    def generate_data(self):
        training_data = []

        random = Vanilla_UCT(1, 100)
        test = Vanilla_UCT(1, 100)

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
                        chosen_play = random.get_action(game)
                        data_pair = [deepcopy(game), chosen_play]
                    else:
                        chosen_play = test.get_action(game)
                        data_pair = [deepcopy(game), chosen_play]
                    training_data.append(data_pair)
                    if chosen_play == 'n':
                        if current_player == 1:
                            current_player = 2
                        else:
                            current_player = 1
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
            if who_won == 2:
                victories2 += 1
        print(training_data)
        print(victories1, victories2)
        print('Player 1: ', victories1 / (victories1 + victories2))
        print('Player 2: ', victories2 / (victories1 + victories2))
        return training_data