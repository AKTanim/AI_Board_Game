FPS = 60    # Frames Per Second

# size
width, height = 800, 800    # Game window size
rows, cols = 8, 8
sq_size = width/ cols   # size of the grid squares
padding = 20    # padding between square and piece
border = 2     # Outline of the piece to make it pronounced

# rgb colors
peach = (188, 92, 88)
brown = (255, 203, 164)
black = (0, 0, 0)
white = (255, 255, 255)
coral = (255, 127, 80)
grey = (128, 128, 128)
blue = (61, 183, 228)
green = (0, 255, 0)
red = (255, 0, 0)

# Game related
sq_value = []   # Array to represent board squares
wh1, wh2, bl1, bl2 = 'w1', 'w2', 'b1', 'b2'     # color and piece type
val_mov = {}    # A dictionary to keep the valid moves where key is the piece clicked
clicked = 0     # To check whether a piece was clicked or not