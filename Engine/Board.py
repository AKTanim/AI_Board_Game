import pygame
from .Constants import width, height, white, black, peach, brown, grey, rows, cols, sq_size, sq_value, padding, border,\
    wh1, wh2, bl1, bl2

# Ask user to choose a color
def select_color(screen, player):
    # Display instruction to choose color
    font1 = pygame.font.Font('freesansbold.ttf', 32)
    font2 = pygame.font.Font('freesansbold.ttf', 20)
    text1 = font1.render('Choose Your Color', True, white, black)
    text2 = font2.render('1. White (Press 1)', True, white, black)
    text3 = font2.render('2. Black (Press 2)', True, white, black)
    screen.blit(text1, (width // 3, height // 3))
    screen.blit(text2, (width // 2.5, height // 2.5))
    screen.blit(text3, (width // 2.5, height // 2.2))

    run = True
    while run:
        # Take input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                run = False
                if event.key == pygame.K_2:
                    player = 'black'

                else:
                    player = 'white'

                print("Player: ", player)
                screen.fill(black)  # Removing instruction
                break
            else:
                run = True
        pygame.display.update()
    return player

# Ask user to choose opposition
def select_opposition(screen):
    # Display instruction to choose color
    font1 = pygame.font.Font('freesansbold.ttf', 32)
    font2 = pygame.font.Font('freesansbold.ttf', 20)
    text1 = font1.render('Play Against:', True, white, black)
    text2 = font2.render('1. Computer (Press 1)', True, white, black)
    text3 = font2.render('2. Human (Press 2)', True, white, black)
    screen.blit(text1, (width // 3, height // 3))
    screen.blit(text2, (width // 2.5, height // 2.5))
    screen.blit(text3, (width // 2.5, height // 2.2))

    run = True
    while run:
        # Take input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                run = False
                if event.key == pygame.K_2:
                    AI = 0

                else:
                    AI = 1

                print("Opponent: ", AI)
                screen.fill(black)  # Removing instruction
                break
            else:
                run = True
        pygame.display.update()
    return AI

# Draw the board
def draw_board(screen):
    screen.fill(peach)  # Background color

    for r in range(rows):
        for c in range(r % 2, cols, 2):
            pygame.draw.rect(screen, brown, (r * sq_size, c * sq_size, sq_size, sq_size))

# Create array representation of the initial state of the board
def board_matrix(player):
    if player == 'white':   # When player chooses white
        for r in range(rows):
            sq_value.append([])
            for c in range(cols):
                if r == 0:
                    if c == 1 or c == 5:
                        sq_value[r].append(wh2)
                    elif c == 3 or c == 7:
                        sq_value[r].append(bl1)
                    else:
                        sq_value[r].append('00')
                elif r == 1:
                    if c == 2 or c == 6:
                        sq_value[r].append(wh2)
                    elif c == 0 or c == 4:
                        sq_value[r].append(bl1)
                    else:
                        sq_value[r].append('00')

                elif r == 6:
                    if c == 3 or c == 7:
                        sq_value[r].append(wh1)
                    elif c == 1 or c == 5:
                        sq_value[r].append(bl2)
                    else:
                        sq_value[r].append('00')

                elif r == 7:
                    if c == 0 or c == 4:
                        sq_value[r].append(wh1)
                    elif c == 2 or c == 6:
                        sq_value[r].append(bl2)
                    else:
                        sq_value[r].append('00')

                else:
                    sq_value[r].append('00')

    else:   # when player chooses black
        for r in range(rows):
            sq_value.append([])
            for c in range(cols):
                if r == 0:
                    if c == 1 or c == 5:
                        sq_value[r].append(bl2)
                    elif c == 3 or c == 7:
                        sq_value[r].append(wh1)
                    else:
                        sq_value[r].append('00')
                elif r == 1:
                    if c == 2 or c == 6:
                        sq_value[r].append(bl2)
                    elif c == 0 or c == 4:
                        sq_value[r].append(wh1)
                    else:
                        sq_value[r].append('00')

                elif r == 6:
                    if c == 3 or c == 7:
                        sq_value[r].append(bl1)
                    elif c == 1 or c == 5:
                        sq_value[r].append(wh2)
                    else:
                        sq_value[r].append('00')

                elif r == 7:
                    if c == 0 or c == 4:
                        sq_value[r].append(bl1)
                    elif c == 2 or c == 6:
                        sq_value[r].append(wh2)
                    else:
                        sq_value[r].append('00')

                else:
                    sq_value[r].append('00')

    #print(sq_value[0][1])
    return sq_value

# Draw the pieces
def draw_pieces(screen, idx_val, row, col):
    # center of the piece
    x = sq_size * col + sq_size // 2
    y = sq_size * row + sq_size // 2

    radius = sq_size // 2 - padding     # radius of the piece

    if idx_val == wh1:  # For single white pieces
        pygame.draw.circle(screen, grey, (x, y), radius + border)
        pygame.draw.circle(screen, white, (x, y), radius)

    elif idx_val == bl1:  # For single black pieces
        pygame.draw.circle(screen, grey, (x, y), radius + border)
        pygame.draw.circle(screen, black, (x, y), radius)

    elif idx_val == wh2:  # For double white pieces
        pygame.draw.circle(screen, grey, (x, y), radius + border)
        pygame.draw.circle(screen, white, (x, y), radius)

        pygame.draw.circle(screen, grey, (x + 8, y - 12), radius + border)
        pygame.draw.circle(screen, white, (x + 8, y - 12), radius)

    elif idx_val == bl2:  # For double black pieces
        pygame.draw.circle(screen, grey, (x, y), radius + border)
        pygame.draw.circle(screen, black, (x, y), radius)

        pygame.draw.circle(screen, grey, (x + 8, y - 12), radius + border)
        pygame.draw.circle(screen, black, (x + 8, y - 12), radius)

    else:
        pass

# Set the initial state of the board
def set_board(screen, player):
    #print('setting')
    draw_board(screen)  # Draw the board grid
    index = board_matrix(player)
    for row in range(rows):
        for col in range(cols):
            draw_pieces(screen, index[row][col], row, col)
    return index

# Update board after every move
def update_board(screen, idx_new):
    screen.fill(black)
    draw_board(screen)  # Draw the board grid
    for row in range(rows):
        for col in range(cols):
            draw_pieces(screen, idx_new[row][col], row, col)    # Draw pieces

    #pygame.display.update()
