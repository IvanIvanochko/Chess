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

        return moves
    
    def get_possible_moves(self):
        moves = super().get_possible_moves()

        blocked_moves = []
        for enemy_piece in self.board.pieces:
            if enemy_piece.color != self.color:
                common_moves = [move for move in moves if move in enemy_piece.attack_moves()]
                if common_moves:
                    blocked_moves.extend(common_moves)

        return [move for move in moves if move not in blocked_moves]
