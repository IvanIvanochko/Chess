import pygame

WHITE = "white"
BLACK = "black"

class ChessPiece:
    """Parent class for all chess pieces""" # doc string to explain the purpose of this class
    def __init__(self, screen, x, y, color, board):
        self.board = board
        self.screen = screen
        self.image = None
        self.x = x
        self.y = y
        self.color = color
        self.piece_type = self.color + " " + self.__class__.__name__ # Get the name of the piece type from the class name
        self.square_size = self.screen.get_width() // 8
    
    def draw(self, screen, square_size): 
        self.screen = screen
        self.square_size = square_size
        self.resize()
        self.screen.blit(self.piece_img, (self.x * self.square_size, self.y * self.square_size))
    
    def move(self, x, y):
        self.x = x
        self.y = y

    def resize(self):
        self.piece_img = pygame.transform.scale(self.image, (self.square_size, self.square_size))

    def is_clicked(self, mouse_x, mouse_y):
        """Check if mouse click is on this piece"""
        piece_rect = self.piece_img.get_rect(topleft=(self.x * self.square_size, self.y * self.square_size))
        return piece_rect.collidepoint(mouse_x, mouse_y)
    
    def select(self):
        """Handle piece selection"""
        self.is_selected = True
        print(f"Selected {self.piece_type}")
        for hint in self.board.hints:
            if (hint.x, hint.y) in self.get_possible_moves():
                hint.show()
    
    def deselect(self):
        """Handle piece deselection"""
        self.is_selected = False
        print(f"Deselected {self.piece_type}")
        for hint in self.board.hints:
            hint.hide()

    def get_possible_moves(self):
        """Return a list of possible moves for this piece"""
        return []

class King(ChessPiece):
    def __init__(self, screen, x, y, color, board):
        super().__init__(screen, x, y, color, board) # call the parent class's __init__ method to initialize the common attributes
        self.color = color
        if self.color == WHITE:
            self.image = pygame.image.load("Materials/Pieces/wk.png").convert_alpha()
        else:
            self.image = pygame.image.load("Materials/Pieces/bk.png").convert_alpha()
    
    def move(self, x, y):
        self.x = x
        self.y = y
    
    def get_possible_moves(self):
        """Return a list of possible moves for the king"""
        moves = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x = self.x + dx
                new_y = self.y + dy

                if 0 <= new_x < 8 and 0 <= new_y < 8: # Check if the move is within the board boundaries
                    moves.append((new_x, new_y))

        return moves