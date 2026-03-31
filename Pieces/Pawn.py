import pygame
from .ChessPiece import ChessPiece, WHITE

class Pawn(ChessPiece):
    def __init__(self, screen, x, y, color, board):
        super().__init__(screen, x, y, color, board)
        self.piece_notation = ""

        if self.color == WHITE:
            self.image = pygame.image.load("Materials/Pieces/wp.png").convert_alpha()
        else:
            self.image = pygame.image.load("Materials/Pieces/bp.png").convert_alpha()
        
        self.IS_FIRST_MOVE = True
        self.two_sqr_fwd = False # Track if the pawn just moved two squares forward (for en passant)
        self.step_counter = 0 # Track how many moves have been made since this pawn's last move (for en passant)

    def move(self, x, y, record_move=True):
        super().move(x, y, record_move=record_move)

        if record_move:
            self.step_counter += 1

        if self.step_counter > 1:
            self.two_sqr_fwd = False # Reset two-square move status after one turn has passed
            self.IS_FIRST_MOVE = False
            
        if abs(y - self.y) == 2:
            self.two_sqr_fwd = True
    
    def get_moves(self):
        """Return a list of standard moves for the pawn"""
        relative_moves = [[0, 1], [-1, 1], [1, 1]] + ([[0, 2]] if self.IS_FIRST_MOVE else [])

        if self.board.IS_WHITE_BOTTOM == (self.color == WHITE):
            relative_moves = [[0, -1], [1, -1], [-1, -1]] + ([[0, -2]] if self.IS_FIRST_MOVE else [])

        moves = []
        for dx, dy in relative_moves:
            new_x = self.x + dx
            new_y = self.y + dy

            if 0 <= new_x < 8 and 0 <= new_y < 8:
                moves.append((new_x, new_y))

        return moves
    
    def get_possible_moves(self):
        moves = super().get_possible_moves()
        
        blocked_moves = []

        LEFT_ATCK, RIGHT_ATCK = False, False
        for m in moves:
            dx = m[0] - self.x

            if dx == 0:
                for piece in self.board.pieces:
                    if piece.x == m[0] and piece.y == m[1]:
                        blocked_moves.append(m)
                        break
                continue
            elif dx == 1:
                for piece in self.board.pieces:
                    if piece.x == m[0] and piece.y == m[1]: 
                        RIGHT_ATCK = True
                        break
            elif dx == -1:
                for piece in self.board.pieces:
                    if piece.x == m[0] and piece.y == m[1]: 
                        LEFT_ATCK = True
                        break

        for m in moves:
            dx = m[0] - self.x
            if dx == 1 and not RIGHT_ATCK:
                blocked_moves.append(m)
            elif dx == -1 and not LEFT_ATCK:
                blocked_moves.append(m)

        return [move for move in moves if move not in blocked_moves]
    
    def attack_moves(self):
        """Return a list of attack moves for this Pawn"""
        moves = self.get_moves()

        blocked_moves = []
        for m in moves:
            dx = m[0] - self.x

            if dx == 0:
                blocked_moves.append(m)
        
        return [move for move in moves if move not in blocked_moves]
