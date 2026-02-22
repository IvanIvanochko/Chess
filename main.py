import pygame
from board import Board
from pieces import BLACK, WHITE

pygame.init()

screen = pygame.display.set_mode((700, 700), pygame.RESIZABLE)
screen_width, screen_height = screen.get_size()

board = Board(screen)

running = True
x = 0
clock = pygame.time.Clock()
delta_time = 0.1
elapsed_time = 0.0

selected_piece = None
IS_WHITES_TURN = True

while running:
    board.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # handle window close events
            running = False
        elif event.type == pygame.VIDEORESIZE: # handle window resize events
            size = min(event.size[0], event.size[1]) # maintain 1:1 aspect ratio
            screen = pygame.display.set_mode((size, size), pygame.RESIZABLE)
            board.resize(size) 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            x_clicked = mouse_x // board.square_size
            y_clicked = mouse_y // board.square_size

            piece_clicked = False
            for piece in board.pieces:
                if piece.is_clicked(mouse_x, mouse_y) and selected_piece is None:
                    if (IS_WHITES_TURN and piece.color == WHITE) or (not IS_WHITES_TURN and piece.color == BLACK):
                        selected_piece = piece
                        selected_piece.select()
                        piece_clicked = True
                elif piece.is_clicked(mouse_x, mouse_y) and selected_piece is not None:
                    piece_clicked = True
                    if piece == selected_piece:
                        piece.deselect()
                        selected_piece = None
                    elif piece != selected_piece:
                        pass # TODO: Handle piece capture
            
            # Deselect if no piece was clicked
            if not piece_clicked and selected_piece is not None and (x_clicked, y_clicked) not in selected_piece.get_possible_moves():
                selected_piece.deselect()
                selected_piece = None
            
            if selected_piece:
                if (x_clicked, y_clicked) in selected_piece.get_possible_moves():
                    selected_piece.move(x_clicked, y_clicked)
                    board.pieces_pos = [(piece.x, piece.y) for piece in board.pieces] # Update pieces positions
                    selected_piece.deselect()
                    selected_piece = None
                    IS_WHITES_TURN = not IS_WHITES_TURN

    pygame.display.flip() # show what we have drawn
    delta_time = clock.tick(60) / 1000.0 # limit to 60 frames per second and get the time since the last frame in seconds

pygame.quit()