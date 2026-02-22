import pygame

WHITE = "white"
BLACK = "black"

class ChessPiece:
    """Parent class for all chess pieces""" # doc string to explain the purpose of this class
    def __init__(self, screen, x, y, color):
        self.screen = screen
        self.image = None
        self.x = x
        self.y = y
        self.color = color
        self.sq = self.screen.get_width() // 8
    
    def draw(self, screen, square_size): 
        self.screen = screen
        self.resize(square_size)
        self.screen.blit(self.piece_img, (self.x * square_size, self.y * square_size))
    
    def move(self, x, y):
        self.x = x
        self.y = y

    def resize(self, square_size):
        self.piece_img = pygame.transform.scale(self.image, (square_size, square_size))

class King(ChessPiece):
    def __init__(self, screen, x, y, color):
        super().__init__(screen, x, y, color) # call the parent class's __init__ method to initialize the common attributes
        self.color = color
        if self.color == WHITE:
            self.image = pygame.image.load("Materials/Pieces/wk.png").convert_alpha()
        else:
            self.image = pygame.image.load("Materials/Pieces/bk.png").convert_alpha()
    
    def move(self, x, y):
        self.x = x
        self.y = y