"""
This is the main driver file.
It will be responsible for taking user input and displaying the current gameplay object
"""

import pygame as p
import Chess_engine

p.init()  # initializing the pygame
WIDTH = HEIGHT = 600
DIMENSION = 8  # Dimension of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION  # WIDTH // DIMENSION
IMAGES = {}  # Global dictionary of images


def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bP","wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR", "wP"] # List of images of the pieces
    for piece in pieces:
        IMAGES[piece] = p.image.load("Images/" + piece + ".png")  # loading the images of the pieces for the Image directory

"""
The main driver file for our code.
This will handle user input.
"""

def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    gs = Chess_engine.Game_state()  # calling the constructor. Get access to the board and other variables
    #print(gs.board)
    valid_moves = gs.get_valid_moves()
    move_made = False # flag variable when a move is made
    load_images()
    running = True
    sq_selected = ()  # tuple of row and column, keep track of the last click of the player 
    player_clicks = [] # to keep track of the player clicks 
    game_over = False
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:  # to use the mouse
                if not game_over:
                    location = p.mouse.get_pos()  #(x, y) location of the cursor
                    col = location[0] // SQ_SIZE  # x co-ordinate of the cursor
                    row = location[1] // SQ_SIZE  # y co-ordinate of the cursor
                    if sq_selected == (row, col): # if the player clicked the same square twice
                        sq_selected = ()     # deselect
                        player_clicks = []   # clear the player clicks
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected) # append for 1st and 2nd clicks
                    if len(player_clicks) == 2: #after 2nd click
                        move = Chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)
                        print(move.get_chess_notation())
                        if move in valid_moves:
                            gs.make_move(move)
                            move_made = True
                        sq_selected = ()  # reset user clicks
                        player_clicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_u:  # undo when "u" is pressed 
                    gs.undo_move()
                    move_made = True
                    sq_selected = ()  # reset user clicks
                if e.key == p.K_r:  #reset the game when "r" is pressed
                    gs = Chess_engine.Game_state()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs, valid_moves, sq_selected)

        if gs.checkmate:
            game_over = True
            if gs.white_to_move:
                result(screen, "Checkmate! Black WINS")
            else:
                result(screen, "Checkmate! White WINS")
        elif gs.stalemate:
            game_over = True
            result(screen, "Stalemate")
        
        p.display.flip()

def highlight_squares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ("w" if gs.white_to_move else "b"):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("darkblue"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE) )
            s.fill(p.Color("yellow"))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))

"""
responsible for all the graphics
"""

def draw_game_state(screen, gs, valid_moves, sq_selected):
    draw_board(screen, gs.board)  # draws squares on the board
    highlight_squares(screen, gs, valid_moves, sq_selected)
    # draw_pieces(screen, gs.board)  # draws pieces on the board

"""
draws squares on the board
draws pieces on the board using current Game_state.borad
"""

def draw_board(screen, board):
    colors = [p.Color("gray"), p.Color("lightgreen")]  # list of two colours for the squares
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]  # light squares gonna have even parity and dark squares gonna have odd parity
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            piece = board[r][c]
            if piece != " ":   # not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def result(screen, text):
    font = p.font.SysFont("Italics", 50, True, False)
    text_object = font.render(text, 0, p.Color("Red"))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH//2 - text_object.get_width()//2, HEIGHT//2 - text_object.get_height()//2)
    screen.blit(text_object, text_location)

if __name__ == "__main__":
    main()
