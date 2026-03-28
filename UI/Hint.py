import pygame

class Hint:
    def __init__(self, screen, x, y, board):
        self.is_visible = False
        self.is_capture = False
        self.is_debug = False
        self.x = x
        self.y = y
        self.board = board
        self.screen = screen
        self.__hint_img = pygame.image.load("Materials/hint.png").convert_alpha()
        self.__capture_hint_img = pygame.image.load("Materials/capture_hint.png").convert_alpha()

        self.square_size = self.board.square_size
        self.hint = pygame.transform.scale(self.__hint_img, (self.square_size, self.square_size))
        self.capture_hint = pygame.transform.scale(self.__capture_hint_img, (self.square_size, self.square_size))

    def draw(self, square_size):
        if not self.is_visible:  # Only draw if visible
            return

        self.square_size = square_size
        
        if self.is_debug:
            # Create red debug surface
            hint_surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            hint_surface.fill((255, 0, 0, 128))  # Red with 50% transparency
        else:
            self.resize()
            hint_surface = self.capture_hint if self.is_capture else self.hint
        
        self.screen.blit(hint_surface, self.board.position_img(self.x, self.y))

    def resize(self):
        self.hint = pygame.transform.scale(self.__hint_img, (self.square_size, self.square_size))
        self.capture_hint = pygame.transform.scale(self.__capture_hint_img, (self.square_size, self.square_size))

    def show(self, is_capture=False):
        self.is_visible = True
        self.is_capture = is_capture
        self.is_debug = False

    def show_debug(self):
        self.is_visible = True
        self.is_capture = False
        self.is_debug = True
    
    def hide(self):
        self.is_visible = False
        self.is_capture = False
        self.is_debug = False
