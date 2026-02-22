import pygame
from pieces import WHITE, King

def board_pieces_setup(screen, board, King):
    wk = King(screen, 4, 7, WHITE)

    return wk


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.square_size = self.screen.get_width() // 8 # Floor division to get the size of each square on the board

        self.__board_img = pygame.image.load("Materials/Pieces/board.png")
        self.board = pygame.transform.scale(self.__board_img, (screen.get_width(), screen.get_height()))

    def draw(self):
        self.screen.blit(self.board, (0, 0))

    def resize(self, new_size):
        self.screen = pygame.display.set_mode((new_size, new_size), pygame.RESIZABLE)
        self.square_size = self.screen.get_width() // 8

        self.board = pygame.transform.scale(self.__board_img, (self.screen.get_width(), self.screen.get_height()))
    