import pygame
import sys
from Engine import Board
from .Constants import sq_size, rows, cols, wh1, wh2, bl1, bl2, green, red

# Check winner
def chcek_winner(idx, player):
    # Get number of pieces
    singles_white, singles_black, doubles_white, doubles_black, total_white, total_black = calc_pieces(idx)

    # Check if the last piece is in the furthest row and remove it to announce the winner
    for c in range(cols):
        if player == 'white':
            if total_white == 1 and idx[0][c] == wh1:
                idx[0][c] = '00'
                total_white = 0
                break
            elif total_black == 1 and idx[7][c] == bl1:
                idx[0][c] = '00'
                total_black = 0
                break
        else:
            if total_black == 1 and idx[0][c] == bl1:
                idx[0][c] = '00'
                total_black = 0
                break
            elif total_white == 1 and idx[7][c] == wh1:
                idx[0][c] = '00'
                total_white = 0
                break

    if total_white == 0:
        winner = 'WHITE'
    elif total_black == 0:
        winner = 'BLACK'
    else:
        winner = None
    return winner

# Calculate the number of pieces
def calc_pieces(idx):
    singles_white, singles_black = 0, 0
    doubles_white, doubles_black = 0, 0
    total_white, total_black = 0, 0
    for r in range(rows):
        for c in range(cols):
            pos = idx[r][c]
            if pos == wh1:
                singles_white += 1
            elif pos == wh2:
                doubles_white += 1
            elif pos == bl1:
                singles_black += 1
            elif pos == bl2:
                doubles_black += 1
            else:
                pass

    total_white = singles_white + doubles_white * 2
    total_black = singles_black + doubles_black * 2
    #print(f"Total White: {total_white}\nTotal Black: {total_black}")

    return singles_white, singles_black, doubles_white, doubles_black, total_white, total_black


# Find the row and column position when a piece is clicked
def clicked_row_col(mouse_x, mouse_y):
    row = int(mouse_y // sq_size)
    col = int(mouse_x // sq_size)
    #print(row, ',', col)
    return row, col

# Check if Bear off is possible
def bear_off_check(player, idx, turn, screen):
    if player == 'white':
        for c in range(cols):
            if turn == 'w' and idx[7][c] == wh2:    # check white doubles on it's nearest row
                pygame.draw.circle(screen, green,(sq_size * c + sq_size // 2, sq_size * 7 + sq_size // 2), 15)
                idx = bear_off(idx, 7, c)

            if turn == 'b' and idx[0][c] == bl2:  # check black doubles on it's nearest row
                pygame.draw.circle(screen, green, (sq_size * c + sq_size // 2, 0 + sq_size // 2), 15)
                idx = bear_off(idx, 0, c)

    else:
        for c in range(cols):
            if turn == 'b' and idx[7][c] == bl2:    # check black doubles on it's nearest row
                pygame.draw.circle(screen, green,(sq_size * c + sq_size // 2, sq_size * 7 + sq_size // 2), 15)
                idx = bear_off(idx, 7, c)

            if turn == 'w' and idx[0][c] == wh2:    # check white doubles on it's nearest row
                pygame.draw.circle(screen, green, (sq_size * c + sq_size // 2, 0 + sq_size // 2), 15)
                idx = bear_off(idx, 0, c)

    return idx

# Bear off a piece
def bear_off(idx, r, c):
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Check if the 'close' button was clicked
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # get mouse position
                row, col = clicked_row_col(mouse_x, mouse_y)  # Calculate the row-column from position

                if (r, c) == (row, col):
                    run = False
                    temp = idx[r][c]
                    idx[r][c] = temp[0] + '1'   # making single piece
                    break
                else:
                    print("You must bear-off the pieces indicated by green circles")
                    run = True
            else:
                run = True
        pygame.display.update()
    return idx

# Check if any piece can be crowned
def crowning_check(player, idx, turn, screen):
    crowning = '0'
    crown_dest = 0
    val_singles = []

    if player == 'white':
        for c in range(cols):   # Check the farthest row for singles that can be crowned
            if turn == 'w' and idx[0][c] == wh1:    # for white's turn
                # identify crowning destination
                crowning = 'w'
                pygame.draw.circle(screen, green, (sq_size * c + sq_size // 2, 0 + sq_size // 2), 15)
                crown_dest = (0, c)
                break

            if turn == 'b' and idx[7][c] == bl1:  # for black's turn
                # identify crowning destination
                crowning = 'b'
                pygame.draw.circle(screen, green, (sq_size * c + sq_size // 2, sq_size * 7 + sq_size // 2), 15)
                crown_dest = (7, c)
                break

        # Collect all the valid singles that can be used as the crown
        if crowning == 'w': # for white's turn
            for row in range(1, rows, 1):
                for col in range(cols):
                    pos = idx[row][col]
                    if pos[0] == 'w' and pos[1] == '1':
                        val_singles.append((row, col))
                        pygame.draw.circle(screen, red, (sq_size * col + sq_size // 2, sq_size * row + sq_size // 2),\
                                          15)
        elif crowning == 'b':   # for black's turn
            for row in range(rows - 1):
                for col in range(cols):
                    pos = idx[row][col]
                    if pos[0] == 'b' and pos[1] == '1':
                        val_singles.append((row, col))
                        pygame.draw.circle(screen, red, (sq_size * col + sq_size // 2, sq_size * row + sq_size // 2),\
                                           15)

    else:
        for c in range(cols):  # Check the furthest row for singles that can be crowned
            if turn == 'b' and idx[0][c] == bl1:  # for white's turn
                crowning = 'b'
                pygame.draw.circle(screen, green, (sq_size * c + sq_size // 2, 0 + sq_size // 2), 15)
                crown_dest = (0, c)
                break

            elif turn == 'w' and idx[7][c] == wh1:  # for black's turn
                crowning = 'w'
                pygame.draw.circle(screen, green, (sq_size * c + sq_size // 2, sq_size * 7 + sq_size // 2), 15)
                crown_dest = (7, c)
                break

        # Collect all the valid singles that can be used as the crown
        if crowning == 'b':  # for white's turn
            for row in range(1, rows, 1):
                for col in range(cols):
                    pos = idx[row][col]
                    if pos[0] == 'b' and pos[1] == '1':
                        val_singles.append((row, col))
                        pygame.draw.circle(screen, red, (sq_size * col + sq_size // 2, sq_size * row + sq_size // 2), \
                                           15)
        else:  # for black's turn
            for row in range(rows - 1):
                for col in range(cols):
                    pos = idx[row][col]
                    if pos[0] == 'w' and pos[1] == '1':
                        val_singles.append((row, col))
                        pygame.draw.circle(screen, red, (sq_size * col + sq_size // 2, sq_size * row + sq_size // 2), \
                                           15)

    if crown_dest != 0 and len(val_singles) != 0:   # only if valid crowning piece are available
        idx = crown(idx, crown_dest, val_singles)
    return idx

# Crown a piece
def crown(idx, crown_dest, val_singles):
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the 'close' button was clicked
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # get mouse position
                row, col = clicked_row_col(mouse_x, mouse_y)  # Calculate the row-column from position

                if (row, col) in val_singles:
                    run = False
                    target = idx[crown_dest[0]][crown_dest[1]]
                    idx[row][col] = '00'
                    idx[crown_dest[0]][crown_dest[1]] = target[0] + '2' # make it a double piece
                    break

                else:
                    print("You must Crown by one of the pieces indicated by red")
                    run = True

            else:
                run = True

        pygame.display.update()
    return idx




# Move pieces to selected square position
def move_pieces(idx, row, col, val_mov_dict):
    #print("Hi")
    run = True
    while run:
        for event in pygame.event.get():
            #print("check 1")
            if event.type == pygame.QUIT:  # Check if the 'close' button was clicked
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #print("check 2")
                mouse_x, mouse_y = pygame.mouse.get_pos()  # get mouse position
                r, c = clicked_row_col(mouse_x, mouse_y)  # Calculate the row-column from position
                #print(val_mov_dict)

                for value in list(val_mov_dict.values()):
                    if (r, c) in value:
                        # Check if it's a transpose move
                        if idx[r][c] != '00':
                            # move the top piece only
                            source = idx[row][col]
                            dest = idx[r][c]
                            idx[r][c] = idx[row][col]
                            idx[row][col] = source[0] + dest[1] # creates the index value of a single piece

                        else:
                            # move piece value to new position
                            idx[r][c] = idx[row][col]
                            idx[row][col] = '00'
                        #print("Past position:", idx[row][col])
                        #print("New position:", idx[r][c])
                    else:   # if clicked on invalid square
                        val_mov_dict.clear()
                        print("Invalid Selection")

                run = False

    return idx, val_mov_dict

# Check available moves and take actions
def check_moves(idx, row, col, val_mov_dict, turn, player, screen):
    # Click and move the piece
    #print("Turn", turn)
    idx_new, val_mov_new = move_pieces(idx, row, col, val_mov_dict)
    Board.update_board(screen, idx_new)

    # Check availability of priority moves
    #print("Turn", turn)
    idx_new = bear_off_check(player, idx_new, turn, screen)   # Check if any bear-off is possible
    Board.update_board(screen, idx_new)
    idx_new = crowning_check(player, idx_new, turn, screen)   # Check if crowning is possible

    if len(val_mov_new.values()) == 0:  # if selection is changed or invalid selection select again
        if turn == 'w':
            turn = 'b'
        else:
            turn = 'w'

    return idx_new, turn
