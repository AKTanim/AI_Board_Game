import pygame
from copy import deepcopy, copy
from Engine import Valid_moves, Gameplay
from Engine.Constants import rows, cols, wh1, wh2, bl1,bl2

# get bot player color for different user settings
def get_bot_player_color(depth, color):
    # get player and bot color
    if depth % 2 == 0:  # bot plays first as the max player and depth starts at even position
        bot = color
        if bot == 'white':
            player = 'black'
        else:
            player = 'white'
    else:
        player = color
        if player == 'white':
            bot = 'black'
        else:
            bot = 'white'

    return bot, player

# Get all the piece location for a player
def get_all_pieces(idx, color):
    pieces = []
    for row in range(rows):
        for col in range(cols):
            pos = idx[row][col]
            if pos != '00' and pos[0] == color[0]: # if position is not empty and color matches
                pieces.append((row, col))
    return pieces

# Move pieces without mouse input
def move_pieces(idx, source, dest):
    source_val = idx[source[0]][source[1]]  # value of the source square
    dest_val = idx[dest[0]][dest[1]]    # value of the destination square

    # check for a transpose move
    if dest_val != '00':
        # move the top piece only
        idx[dest[0]][dest[1]] = source_val
        idx[source[0]][source[1]] = source_val[0] + dest_val[1]  # creates the index value of a single piece

    else:
        # move piece value to new position
        idx[dest[0]][dest[1]] = source_val
        idx[source[0]][source[1]] = '00' # empty the source position

    #print("Pieces moved for source, destination", source, dest)
    return idx

# Check for bear off and take action
def bear_off(idx, color, depth):
    # get player and bot color
    bot, player = get_bot_player_color(depth, color)

    if color == 'white':
        for c in range(cols):
            if player == 'white' and idx[7][c] == wh2:    # check doubles on it's nearest row
                temp = idx[7][c]
                idx[7][c] = temp[0] + '1'  # making single piece

            if bot == 'white' and idx[0][c] == wh2:  # check doubles on it's nearest row
                temp = idx[0][c]
                idx[0][c] = temp[0] + '1'  # making single piece

    else:
        for c in range(cols):
            if player == 'black' and idx[7][c] == bl2:    # check doubles on it's nearest row
                temp = idx[7][c]
                idx[7][c] = temp[0] + '1'  # making single piece

            if bot == 'black' and idx[0][c] == bl2:  # check doubles on it's nearest row
                temp = idx[0][c]
                idx[0][c] = temp[0] + '1'  # making single piece

    return idx

# check for crowning and take action
def crowning(idx, color, depth):
    #print("Crowning in progress for color", color)
    # get player and bot color
    bot, player = get_bot_player_color(depth, color)

    crowning = '0'
    crown_dest = 0
    val_singles = []

    if color == 'white':
        for c in range(cols):  # Check the farthest row for singles that can be crowned
            if player == 'white' and idx[0][c] == wh1:
                # identify crowning destination
                crowning = 'p'
                crown_dest = (0, c)
                break

            if bot == 'white' and idx[7][c] == wh1:
                # identify crowning destination
                crowning = 'b'
                crown_dest = (7, c)
                break

         # Collect all the valid singles that can be used as the crown
        if crowning == 'p':
            for row in range(1, rows, 1):
                for col in range(cols):
                    if idx[row][col] == 'w1':
                        val_singles.append((row, col))

        elif crowning == 'b':
            for row in range(rows - 1):
                for col in range(cols):
                    if idx[row][col] == 'w1':
                        val_singles.append((row, col))

    else:
        for c in range(cols):  # Check the farthest row for singles that can be crowned
            if player == 'black' and idx[0][c] == bl1:
                # identify crowning destination
                crowning = 'p'
                crown_dest = (0, c)
                break

            if bot == 'black' and idx[7][c] == bl1:
                # identify crowning destination
                crowning = 'b'
                crown_dest = (7, c)
                break

        # Collect all the valid singles that can be used as the crown
        if crowning == 'p':
            for row in range(1, rows, 1):
                for col in range(cols):
                    if idx[row][col] == 'b1':
                        val_singles.append((row, col))

        elif crowning == 'b':
            for row in range(rows - 1):
                for col in range(cols):
                    if idx[row][col] == 'b1':
                        val_singles.append((row, col))

    # Loop through the valid singles and crown
    if crown_dest != 0 and len(val_singles) != 0:
        #print("Crowning done")
        for val_single in val_singles:
            target = idx[crown_dest[0]][crown_dest[1]]
            idx[val_single[0]][val_single[1]] = '00'
            idx[crown_dest[0]][crown_dest[1]] = target[0] + '2'  # make it a double piece
            return idx

    return idx


# simulate the game
def simulate_game(idx, source, dest, color, depth):
    idx_new = move_pieces(idx, source, dest)    # do the basic moves
    idx_new = bear_off(idx_new, color, depth)  # Check if any bear-off is possible
    idx_new = crowning(idx_new, color, depth)  # Check if crowning is possible


    return idx_new

# Get all the states of the board for all the pieces for a player
def get_all_states(idx, color, depth):
    # get player and bot color
    bot, player = get_bot_player_color(depth, color)
    board_states = []

    for piece_pos in get_all_pieces(idx, color):
        #print(piece_pos)
        valid_moves = Valid_moves.get_valid_moves(idx, piece_pos[0], piece_pos[1], player)
        #print(len(valid_moves.values()))
        if len(list(valid_moves.values())) != []:
            for val_mov in list(valid_moves.values()):
                for i in range(len(val_mov)):
                    temp_idx = deepcopy(idx)    # doesn't change main idx
                    temp_piece_pos = piece_pos
                    new_idx = simulate_game(temp_idx, temp_piece_pos, val_mov[i], color, depth)
                    board_states.append(new_idx)

            valid_moves.clear()
        else:
            valid_moves.clear()

    #print("All states collected. Length: ", len(board_states))
    return board_states