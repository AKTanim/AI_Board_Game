# AI board game: Impasse
# Course: Intelligent Search & Games
# AI, Maastricht University
# Done by Amirul Karim Tanim (i6287477)
import pygame
pygame.init()
import sys
from Engine import Board, Gameplay, Valid_moves
from Engine.Constants import FPS, width, height, white, black
from Brain import Bot

# Initialize game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('IMPASSE')

# Main function
def main():
    run = True
    clk = pygame.time.Clock()
    player = 0  # variable to enable the player to choose a color
    AI = 0  # To activate AI
    board_index = []     # Array representation of the board
    turn = 'w'  # Player turn (white or black)


    player = Board.select_color(screen, player)     # Let the player select color
    AI = Board.select_opposition(screen)    # Let the player choose opposition
    board_index = Board.set_board(screen, player)  # Set the initial state of the board
    pygame.display.update()

    while run:
        #print("main run")
        clk.tick(FPS)

        # Check winner
        winner = Gameplay.chcek_winner(board_index, player)
        if winner != None:
            print("*** Game over ***")
            print(f"... {winner} wins ...")
            run = False

        # Call the AI
        if player == 'white' and AI == 1 and turn == 'b':
            turn, board_index = Bot.ai_main(player, board_index, screen, turn)
            Board.update_board(screen, board_index)  # Update the board after bot makes the move
            print("AI done")
            #pygame.time.delay(10000)
        elif player == 'black' and AI == 1 and turn == 'w':
            #Board.update_board(screen, board_index)  # Update the board before bot makes the move
            turn, board_index = Bot.ai_main(player, board_index, screen, turn)
            Board.update_board(screen, board_index)  # Update the board after bot makes the move
        else:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Check if the 'close' button was clicked
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()   # get mouse position
                row, col = Gameplay.clicked_row_col(mouse_x, mouse_y)   # Calculate the row-column from position

                # check turn
                pos_val = board_index[row][col]
                if turn != pos_val[0]:  # if turn doesn't match selected piece color or selected square is empty
                    break

                # Get all valid moves for the selected piece and then draw them
                val_mov = Valid_moves.get_valid_moves(board_index, row, col, player)
                board_index_new, turn_new = Valid_moves.draw_valid_moves(screen, val_mov, board_index, \
                                                                         row, col, turn, player)

                Board.update_board(screen, board_index_new)     # Update board
                val_mov.clear()

                # change turn for next iteration
                if turn_new == 'w':
                    turn = 'b'
                else:
                    turn = 'w'

        pygame.display.update()

main()