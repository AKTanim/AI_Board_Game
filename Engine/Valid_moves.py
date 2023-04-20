import pygame
from Engine import Gameplay
from .Constants import val_mov, wh1, wh2, bl1, bl2, sq_size, blue


# initialize the dictionary of valid moves
def initiate_val_mov(idx, row, col):
    source = (row, col)
    piece = idx[row][col]
    key = str((piece, source))
    #print(key)
    return key

# Valid moves in left diagonal
def get_valid_left(key, idx, row, col, step, end):
    #print("Left valid moves")
    c = col - 1
    for r in range(row+step, end, step):
        if c < 0:       # out of board
            break
        if idx[r][c] == '00':  # as long as the square is empty
            val_mov[key].append((r, c))  # update the dictionary with valid moves
        else:   # if the square is occupied
            # check for transpose
            break
        c -= 1  # update column value

# Valid moves in right diagonal
def get_valid_right(key, idx, row, col, step, end):
    #print("Right valid moves")
    c = col + 1
    for r in range(row+step, end, step):
        if c > 7:       # out of board
            break
        if idx[r][c] == '00':  # as long as the square is empty
            val_mov[key].append((r, c))     # update the dictionary with valid moves
        else:   # if the square is occupied
            # check for transpose
            break
        c += 1  # update column value

# Valid transpose moves
def get_valid_transpose(key, idx, row, col, left_tr, right_tr):
    #print("Transpose valid moves")
    idx_val_source = idx[row][col]

    if col == 0:  # out of left edge of the board
        idx_val_left = '00'
        idx_val_right = idx[right_tr[0]][right_tr[1]]
    elif col == 7:  # out of right edge of the board
        idx_val_right = '00'
        idx_val_left = idx[left_tr[0]][left_tr[1]]
    else:
        idx_val_left = idx[left_tr[0]][left_tr[1]]
        idx_val_right = idx[right_tr[0]][right_tr[1]]


    #print("here 1", idx_val_left[1], idx_val_right[1])
    if idx_val_source[1] == '2' and idx_val_left[1] == '1' and idx_val_source[0] == idx_val_left[0]:
        #print("Transpose done")
        print(idx[1][2])
        print(idx[6][5])
        # if color matches and destination is a single piece
        val_mov[key].append(left_tr)  # update the dictionary with valid moves

    if idx_val_source[1] == '2' and idx_val_right[1] == '1' and idx_val_source[0] == idx_val_right[0]:
        # if color matches and destination is a single piece
        val_mov[key].append(right_tr)  # update the dictionary with valid moves



# get valid moves for a selected piece
def get_valid_moves(idx, row, col, player):
    key = initiate_val_mov(idx, row, col)
    val_mov.update({key:[]})     # initiate dictionary with key

    if player == 'white':
        if idx[row][col] == wh1:
            step, end = -1, -1

        elif idx[row][col] == bl2:
            step, end = -1, -1
            left_tr = (row-1, col-1)
            right_tr = (row-1, col+1)

        elif idx[row][col] == wh2:
            step, end = 1, 8
            left_tr = (row + 1, col - 1)
            right_tr = (row + 1, col + 1)

        elif idx[row][col] == bl1:
            step, end = 1, 8

        else:   # when empty square is clicked
            step, end = -1, -1

        get_valid_left(key, idx, row, col, step, end)   # Valid moves towards left diagonal
        get_valid_right(key, idx, row, col, step, end)  # Valid moves towards right diagonal
        if idx[row][col] == wh2 or idx[row][col] == bl2:
            get_valid_transpose(key, idx, row, col, left_tr, right_tr)

    else:
        if idx[row][col] == bl1:
            step, end = -1, -1

        elif idx[row][col] == wh2:
            step, end = -1, -1
            left_tr = (row - 1, col - 1)
            right_tr = (row - 1, col + 1)

        elif idx[row][col] == bl2:
            step, end = 1, 8
            left_tr = (row + 1, col - 1)
            right_tr = (row + 1, col + 1)

        elif idx[row][col] == wh1:
            step, end = 1, 8

        else:   # when empty square is clicked
            step, end = -1, -1

        get_valid_left(key, idx, row, col, step, end)
        get_valid_right(key, idx, row, col, step, end)
        if idx[row][col] == wh2 or idx[row][col] == bl2:
            get_valid_transpose(key, idx, row, col, left_tr, right_tr)

    if idx[row][col] == '00':  # if clicked on an empty square
        val_mov.clear()
    #print("Valid moves:", val_mov)
    print("Please wait for the Bot...")
    return val_mov

# Highlight the valid moves
def draw_valid_moves(screen, val_mov_dict, idx, row, col, turn, player):
    # Draw the valid moves
    for value in list(val_mov_dict.values()):
        for i in range(len(value)):
            pygame.draw.circle(screen, blue, (value[i][1] * sq_size + sq_size // 2, value[i][0] * sq_size + sq_size // 2), 15)
    pygame.display.update()

    # Check moves and take action
    idx_new, turn_new = Gameplay.check_moves(idx, row, col, val_mov_dict, turn, player, screen)

    return idx_new, turn_new