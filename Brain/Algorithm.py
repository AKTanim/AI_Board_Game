import pygame
from Engine import Gameplay
from Brain import Information

# Define the evaluation function
def eval_func(idx, color):
    # Calculate number of pieces on board
    singles_white, singles_black, doubles_white, doubles_black, total_white, total_black = Gameplay.calc_pieces(idx)

    # calculate score of the board
    if color == 'white':
        score = 30 * (total_white - total_black) + 2 * (doubles_white - singles_white)
    else:
        score = 30 * (total_black - total_white) + 2 * (doubles_black - singles_black)

    return score

# Define MiniMax algorithm
def minimax(idx, depth, max_turn, color):
    # get player and bot color
    bot, player = Information.get_bot_player_color(depth, color)

    if depth == 0 or Gameplay.chcek_winner(idx, player) != None:
        #print("Minimax finished")
        return eval_func(idx, color), idx

    if max_turn:
        max_score = -100000
        best_move = None
        for board_state in Information.get_all_states(idx, bot, depth):
            score = minimax(idx, depth - 1, False, player)[0]
            max_score = max(max_score, score)
            if max_score == score:
                best_move = board_state
        return max_score, best_move

    else:
        min_score = 100000
        best_move = None
        for board_state in Information.get_all_states(idx, player, depth):
            score = minimax(idx, depth - 1, True, bot)[0]
            min_score = min(min_score, score)
            if min_score == score:
                best_move = board_state
        return min_score, best_move

# Define MiniMax algorithm
def alpha_beta(idx, depth, max_turn, color):
    # get player and bot color
    bot, player = Information.get_bot_player_color(depth, color)

    if depth == 0 or Gameplay.chcek_winner(idx, player) != None:
        #print("Minimax finished")
        return eval_func(idx, color), idx

    if max_turn:
        max_score = -100000
        best_move = None
        for board_state in Information.get_all_states(idx, bot, depth):
            score = alpha_beta(idx, depth - 1, False, player)[0]
            max_score = max(max_score, score)
            if score > max_score:       # Alpha Pruning done here
                break
            else:
                best_move = board_state
        return max_score, best_move

    else:
        min_score = 100000
        best_move = None
        for board_state in Information.get_all_states(idx, player, depth):
            score = alpha_beta(idx, depth - 1, True, bot)[0]
            min_score = min(min_score, score)
            if score > min_score:       # Beta pruning done here
                break
            else:
                best_move = board_state
        return min_score, best_move