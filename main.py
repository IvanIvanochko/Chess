import pygame
from board import Board, board_pieces_setup
from pieces import WHITE, BLACK, ChessPiece, King

pygame.init()

screen = pygame.display.set_mode((700, 700), pygame.RESIZABLE)
screen_width, screen_height = screen.get_size()

board = Board(screen)
    
wk = board_pieces_setup(screen, board, King)

running = True
x = 0
clock = pygame.time.Clock()
delta_time = 0.1
elapsed_time = 0.0

while running:
    board.draw()

    wk.draw(screen, board.square_size)

    # x += 50 * delta_time # move the king to the right at a speed of 50 pixels per second
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # handle window close events
            running = False
        elif event.type == pygame.VIDEORESIZE: # handle window resize events
            size = min(event.size[0], event.size[1]) # maintain 1:1 aspect ratio
            screen = pygame.display.set_mode((size, size), pygame.RESIZABLE)
            board.resize(size) 

    pygame.display.flip() # show what we have drawn
    delta_time = clock.tick(60) / 1000.0 # limit to 60 frames per second and get the time since the last frame in seconds

pygame.quit()