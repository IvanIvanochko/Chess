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

    def get_moves(self):
        """Return a list of standard moves for this piece"""
        return []
    
    def get_possible_moves(self):
        """Return a list of possible moves for this piece"""
        moves = self.get_moves()
        blocked_moves = []  # Track moves to remove instead of removing during iteration (it doesn't work to remove items from a list while iterating over it)

        for move in moves:
            for piece in self.board.pieces:
                if (piece.x, piece.y) == move:
                    if piece.color == self.color:  # Can't move to a square occupied by a piece of the same color
                        blocked_moves.append(move)
                        break
        
        # Remove blocked moves after iteration
        return [move for move in moves if move not in blocked_moves]
    
    def capture(self, x, y):
        """Handle piece capture"""
        self.board.remove_piece(x, y)

    def attack_moves(self):
        """Return a list of attack moves for this piece (used for checking if the king is in check)"""
        return self.get_moves()
        

class King(ChessPiece):
    def __init__(self, screen, x, y, color, board):
        super().__init__(screen, x, y, color, board) # call the parent class's __init__ method to initialize the common attributes
        self.color = color
        if self.color == WHITE:
            self.image = pygame.image.load("Materials/Pieces/wk.png").convert_alpha()
        else:
            self.image = pygame.image.load("Materials/Pieces/bk.png").convert_alpha()

    def get_moves(self):
        """Return a list of standard moves for the king"""
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
    
    def get_possible_moves(self):
        moves = super().get_possible_moves()

        blocked_moves = [] 
        # Remove moves that would put the king in check
        for enemy_piece in self.board.pieces:
            if enemy_piece.color != self.color:
                common_moves = [move for move in moves if move in enemy_piece.attack_moves()]
                if common_moves:
                    blocked_moves.extend(common_moves)

        # for move in moves:
        #     for piece in self.board.pieces:
        #             if piece.color != self.color:  # Either allowed move to capture the piece or skip the move
        #                 for enemy_friend in self.board.pieces:
        #                     if enemy_friend.color != self.color:
        #                         if (piece.x, piece.y) in enemy_friend.get_moves():  # Can't capture a piece that is defended by an enemy piece
        #                             blocked_moves.append(move)
        #                             break

        return [move for move in moves if move not in blocked_moves]
    
class Pawn(ChessPiece):
    def __init__(self, screen, x, y, color, board):
        super().__init__(screen, x, y, color, board) # call the parent class's __init__ method to initialize the common attributes
        self.color = color
        if self.color == WHITE:
            self.image = pygame.image.load("Materials/Pieces/wp.png").convert_alpha()
        else:
            self.image = pygame.image.load("Materials/Pieces/bp.png").convert_alpha()
        
        self.IS_FIRST_MOVE = True

    def move(self, x, y):
        super().move(x, y)

        self.IS_FIRST_MOVE = False
    
    def get_moves(self):
        """Return a list of standard moves for the pawn"""
        relative_moves = [[0,1], [-1,1], [1,1]] + ([[0,2]] if self.IS_FIRST_MOVE else [])

        if self.board.IS_WHITE_BOTTOM == (self.color == WHITE): # xnor
            relative_moves = [[0,-1], [1,-1], [-1,-1]] + ([[0,-2]] if self.IS_FIRST_MOVE else [])

        moves = []  # Start with empty list for absolute positions
        for dx, dy in relative_moves:
                new_x = self.x + dx
                new_y = self.y + dy

                if 0 <= new_x < 8 and 0 <= new_y < 8: # Check if the move is within the board boundaries
                    moves.append((new_x, new_y))

        return moves
    
    def get_possible_moves(self):
        moves = super().get_possible_moves()
        
        # Remove attack moves that are not valid (i.e. no piece to capture)
        blocked_moves = []  

        LEFT_ATCK, RIGHT_ATCK = False, False
        for m in moves:
            dx = m[0] - self.x

            if dx == 0:  # Front move
                for piece in self.board.pieces:
                    if piece.x == m[0] and piece.y == m[1]:  # Can't move forward if there's a piece in the way
                        blocked_moves.append(m)
                        break
                continue
            elif dx == 1: # Right attack move is only valid if there's an enemy piece to capture
                for piece in self.board.pieces:
                    if piece.x == m[0] and piece.y == m[1]: 
                        RIGHT_ATCK = True
                        break
            elif dx == -1: # Left attack move is only valid if there's an enemy piece to capture
                for piece in self.board.pieces:
                    if piece.x == m[0] and piece.y == m[1]: 
                        LEFT_ATCK = True
                        break

        # Remove attack moves that are not valid (i.e. no piece to capture)
        for m in moves:
            dx = m[0] - self.x
            if dx == 1 and not RIGHT_ATCK:  # Right attack move is only valid if there's an enemy piece to capture
                blocked_moves.append(m)
            elif dx == -1 and not LEFT_ATCK: # Left attack move is only valid if there's an enemy piece to capture
                blocked_moves.append(m)

                
        return [move for move in moves if move not in blocked_moves]
    
    def attack_moves(self):
        """Return a list of attack moves for this Pawn"""
        moves = self.get_moves()

        blocked_moves = [] 
        for m in moves:
            dx = m[0] - self.x

            if dx == 0:  # Front move
                blocked_moves.append(m)
        
        return [move for move in moves if move not in blocked_moves]