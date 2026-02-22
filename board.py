import pygame
from pieces import BLACK, WHITE, King

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.square_size = self.screen.get_width() // 8 # Floor division to get the size of each square on the board

        self.__board_img = pygame.image.load("Materials/Pieces/board.png")
        self.board = pygame.transform.scale(self.__board_img, (screen.get_width(), screen.get_height()))

        self.__hint_img = pygame.image.load("Materials/hint.png").convert_alpha()
        self.hint = pygame.transform.scale(self.__hint_img, (screen.get_width(), screen.get_height()))

        self.hints = []
        for x in range(8):
            for y in range(8):
                self.hints.append(Hint(screen, x, y))

        self.pieces = []
        self.pieces.append(King(screen, 4, 7, WHITE, self)) # wk
        self.pieces.append(King(screen, 4, 0, BLACK, self)) # bk

        self.pieces_pos = []
        for piece in self.pieces:
            self.pieces_pos.append((piece.x, piece.y))

    def draw(self):
        self.screen.blit(self.board, (0, 0))

        for piece in self.pieces:
            piece.draw(self.screen, self.square_size)

        for hint in self.hints:
            hint.draw(self.square_size)


    def resize(self, new_size):
        self.screen = pygame.display.set_mode((new_size, new_size), pygame.RESIZABLE)
        self.square_size = self.screen.get_width() // 8

        self.board = pygame.transform.scale(self.__board_img, (self.screen.get_width(), self.screen.get_height()))

class Hint:
    def __init__(self, screen, x, y):
        self.is_visible = False
        self.x = x
        self.y = y
        self.screen = screen
        self.__hint_img = pygame.image.load("Materials/hint.png").convert_alpha()

        self.square_size = self.screen.get_width() // 8
        self.hint = pygame.transform.scale(self.__hint_img, (self.square_size, self.square_size))

    def draw(self, square_size):
        if not self.is_visible:  # Only draw if visible
            return

        self.square_size = square_size
        self.resize()
        self.screen.blit(self.hint, (self.x * self.square_size, self.y * self.square_size))

    def resize(self):
        self.hint = pygame.transform.scale(self.__hint_img, (self.square_size, self.square_size))

    def show(self):
        self.is_visible = True
    
    def hide(self):
        self.is_visible = False

    