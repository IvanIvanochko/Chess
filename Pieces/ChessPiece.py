import pygame

WHITE = "WHITE"
BLACK = "BLACK"

class ChessPiece:
    """Parent class for all chess pieces"""
    def __init__(self, screen, x, y, color, board):
        self.board = board
        self.screen = screen
        self.image = None
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.has_moved = False
        self.is_selected = False
        self.is_selectable = True
        self.color = color
        self.piece_type = self.color + " " + self.__class__.__name__
        self.piece_notation = "" # Algebraic notation for this piece
        self.square_size = self.board.square_size
        self.forced_moves = [] 
    
    def draw(self, screen, square_size): 
        self.screen = screen
        self.square_size = square_size
        self.resize()
        self.screen.blit(self.piece_img, self.board.position_img(self.x, self.y))
    
    def move(self, x, y, record_move=True):
        if record_move:
            self.board.record_move(self, x, y, old_x=self.x, old_y=self.y, has_moved=self.has_moved)
    
        self.x = x
        self.y = y

        if record_move and not self.has_moved:
            self.has_moved = True

    def resize(self):
        self.piece_img = pygame.transform.scale(self.image, (self.square_size, self.square_size))

    def is_clicked(self, mouse_x, mouse_y):
        """Check if mouse click is on this piece"""
        piece_rect = self.piece_img.get_rect(topleft=self.board.position_img(self.x, self.y))
        return piece_rect.collidepoint(mouse_x, mouse_y)
    
    def select(self):
        """Handle piece selection"""
        if not self.is_selectable:
            return
        
        self.is_selected = True
        print(f"Selected {self.piece_type}")

        blocked_moves = []
        possible_moves = self.get_possible_moves()

        enemy_positions = {
            (piece.x, piece.y)
            for piece in self.board.pieces
            if piece.color != self.color
        }

        if self.forced_moves:
            possible_moves = self.forced_moves
        elif not self.piece_notation == "K": # Check if the move puts own king in check
            previous_pos = (self.x, self.y)
            
            for move in possible_moves: 
                self.move(*move, record_move = False)
                self.board.update_pieces_pos()

                if self.board.king_in_check(next((p for p in self.board.pieces if p.piece_notation == "K" and p.color == self.color), None)):
                    if move not in enemy_positions: # update_pieces_pos does not account for captures
                        blocked_moves.append(move)

                self.move(*previous_pos, record_move = False)
                self.board.update_pieces_pos()

            possible_moves = [move for move in possible_moves if move not in blocked_moves]

        for hint in self.board.hints:
            if (hint.x, hint.y) in possible_moves:
                hint.show(is_capture=(hint.x, hint.y) in enemy_positions)
    
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
        blocked_moves = []

        for move in moves:
            for piece in self.board.pieces:
                if (piece.x, piece.y) == move:
                    if piece.color == self.color:
                        blocked_moves.append(move)
                        break
        
        return [move for move in moves if move not in blocked_moves]
    
    def capture(self, x, y):
        """Handle piece capture"""
        self.board.remove_piece(x, y)

    def attack_moves(self):
        """Return a list of attack moves for this piece"""
        return self.get_possible_moves()

    def copy(self, board):
        """Create a detached copy of this piece for a cloned board."""
        new_piece = self.__class__(self.screen, self.x, self.y, self.color, board)
        new_piece.start_x = self.start_x
        new_piece.start_y = self.start_y
        new_piece.has_moved = self.has_moved
        new_piece.is_selected = False
        new_piece.is_selectable = self.is_selectable
        new_piece.forced_moves = list(self.forced_moves)
        return new_piece
    
    @staticmethod
    def normalize_direction(v):
        x, y = v
        return (
            (x > 0) - (x < 0),
            (y > 0) - (y < 0)
        )