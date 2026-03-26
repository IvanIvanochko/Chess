import pygame
from .ChessPiece import ChessPiece, WHITE

class Knight(ChessPiece):
    def __init__(self, screen, x, y, color, board):
        super().__init__(screen, x, y, color, board)
        self.piece_notation = "N"

        if self.color == WHITE:
            self.image = pygame.image.load("Materials/Pieces/wn.png").convert_alpha()
        else:
            self.image = pygame.image.load("Materials/Pieces/bn.png").convert_alpha()

    def get_moves(self):
        """Return a list of standard moves for the knight"""
        relative_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        moves = []
        for dx, dy in relative_moves:
            new_x = self.x + dx
            new_y = self.y + dy

            if 0 <= new_x < 8 and 0 <= new_y < 8:
                moves.append((new_x, new_y))

        return moves
    
    def get_possible_moves(self):
        return super().get_possible_moves()