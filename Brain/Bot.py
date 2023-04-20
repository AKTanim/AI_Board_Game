import pygame
from Engine import Valid_moves, Board
from Engine.Constants import rows, cols
from Brain import Algorithm

def ai_main(player, idx, screen, turn):
    # Select Bot's color
    if player == 'white':
        bot = 'black'
    else:
        bot = 'white'

    # get the best move. Must use even depth. Otherwise a slight change of code is necessary in...
    # the function "Information.get_bot_player_color(depth, color)" since it depends on the depth
    # This is simple MiniMax
    #score, idx_new = Algorithm.minimax(idx, 4, True, bot)

    # This is MiniMax with Alpha-Beta Pruning
    score, idx_new = Algorithm.alpha_beta(idx, 4, True, bot)

    # change turn
    if turn == 'w':
        turn = 'b'
    else:
        turn = 'w'

    return turn, idx_new