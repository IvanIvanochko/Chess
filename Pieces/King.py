import pygame

from Pieces.Rook import Rook
from .ChessPiece import BLACK, ChessPiece, WHITE

class King(ChessPiece):
    def __init__(self, screen, x, y, color, board):
        super().__init__(screen, x, y, color, board)
        self.piece_notation = "K"

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

                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    moves.append((new_x, new_y))

        moves = list(dict.fromkeys(tuple(move) for move in moves)) # Remove duplicates

        return moves
    
    def get_possible_moves(self):
        moves = super().get_possible_moves()
        moves.extend(self.get_castle_moves()) # Add castling moves

        blocked_moves = []

        # All possible enemies moves
        all_enemy_moves = []
        for piece in self.board.pieces:
            if piece.color != self.color: # Ignore King to prevent infinite recursion on get_possible_moves
                all_enemy_moves.extend(piece.attack_moves())

                if (piece.x, piece.y) in all_enemy_moves:
                    all_enemy_moves.remove((piece.x, piece.y))

        # Check if any of the king's moves are attacked by enemy pieces and block those moves
        blocked_moves.extend([move for move in moves if move in all_enemy_moves]) 

        # Debugging: Show which moves are blocked
        for hint in self.board.hints:
            if (hint.x, hint.y) in blocked_moves:
                hint.show_debug()

        return [move for move in moves if move not in blocked_moves]
    
    def attack_moves(self):
        """Return a list of attack moves for the king"""
        return self.get_moves()
    
    def get_castle_moves(self):
        """Handle castling for the king"""

        if self.x != self.start_x or self.y != self.start_y: # King has moved, cannot castle
            return []
        
        if self.has_moved: # King has moved, cannot castle
            return []
        
        left_rook = None
        right_rook = None

        for piece in self.board.pieces:
            if isinstance(piece, Rook) and piece.color == self.color:
                if piece.x < self.x: # Left rook
                    left_rook = piece
                else: # Right rook
                    right_rook = piece

        RIGHT_CASTLE = True
        LEFT_CASTLE = True

        if left_rook.has_moved:
            LEFT_CASTLE = False
        if right_rook.has_moved:    
            RIGHT_CASTLE = False

        if not LEFT_CASTLE and not RIGHT_CASTLE:
            return []
        
        for piece in self.board.pieces:
            for i in [5, 6]:
                if piece.x == i and piece.y == self.start_y:
                    RIGHT_CASTLE = False
                    break
            for i in [1, 2, 3]:
                if piece.x == i and piece.y == self.start_y:
                    LEFT_CASTLE = False
                    break

        if not LEFT_CASTLE and not RIGHT_CASTLE:
            return []
        
        moves = []
        if RIGHT_CASTLE:
            moves.append((self.x + 2, self.y))
        if LEFT_CASTLE: 
            moves.append((self.x - 2, self.y))
        
        return moves
        
    def move(self, x, y):
        if x == self.x + 2 and y == self.start_y: # Right castle
            rook = next((piece for piece in self.board.pieces if isinstance(piece, Rook) and piece.color == self.color and piece.x > self.x), None)
            if rook:
                rook.move(self.x + 1, self.y, record_move=False) 
                self.board.record_custom_move("O-O")

        if x == self.x - 2 and y == self.start_y: # Left castle
            rook = next((piece for piece in self.board.pieces if isinstance(piece, Rook) and piece.color == self.color and piece.x < self.x), None)
            if rook:
                rook.move(self.x - 1, self.y, record_move=False) 
                self.board.record_custom_move("O-O-O")

        super().move(x, y, record_move=False)
        
