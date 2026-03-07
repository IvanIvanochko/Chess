import pygame
from .ChessPiece import ChessPiece, WHITE

class King(ChessPiece):
    def __init__(self, screen, x, y, color, board):
        super().__init__(screen, x, y, color, board)

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
