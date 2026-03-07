import pygame
from .ChessPiece import ChessPiece, WHITE

class Queen(ChessPiece):
    def __init__(self, screen, x, y, color, board):
        super().__init__(screen, x, y, color, board)

        if self.color == WHITE:
            self.image = pygame.image.load("Materials/Pieces/wq.png").convert_alpha()
        else:
            self.image = pygame.image.load("Materials/Pieces/bq.png").convert_alpha()
    
    def get_moves(self):
        """Return a list of standard moves for the queen"""
        relative_moves = []

        for i in range(0, 8):
            relative_moves.append([i, 0])
            relative_moves.append([0, i])
            relative_moves.append([-i, 0])
            relative_moves.append([0, -i])
            
            relative_moves.append([i, i])
            relative_moves.append([-i, i])
            relative_moves.append([i, -i])
            relative_moves.append([-i, -i])

        relative_moves = list(dict.fromkeys(tuple(move) for move in relative_moves)) # Remove duplicates
        relative_moves.remove((0, 0)) # Remove the current position

        moves = []
        for dx, dy in relative_moves:
            new_x = self.x + dx
            new_y = self.y + dy

            if 0 <= new_x < 8 and 0 <= new_y < 8:
                moves.append((new_x, new_y))

        return moves

    def get_possible_moves(self):
        """Return a list of possible moves for the queen"""
        moves = self.get_moves()      
        blocked_moves = []
        blocked_moves.append((self.x, self.y))

        for m in moves:
            drx = m[0] - self.x
            dry = m[1] - self.y
            
            drx, dry = ChessPiece.normalize_direction((drx, dry))

            if m in blocked_moves:
                continue

            for piece in self.board.pieces:
                if piece.x == self.x and piece.y == self.y:
                    continue

                piece_dx = piece.x - self.x
                piece_dy = piece.y - self.y
                piece_dist2 = piece_dx*piece_dx + piece_dy*piece_dy

                if piece.x == m[0] and piece.y == m[1]:  
                    for i in range(0, 8):
                        dr_move = (self.x + drx * i, self.y + dry * i)

                        move_dx = dr_move[0] - self.x
                        move_dy = dr_move[1] - self.y
                        move_dist2 = move_dx*move_dx + move_dy*move_dy

                        if dr_move not in moves:
                            continue

                        if piece.color == self.color and move_dist2 < piece_dist2:
                            continue

                        if piece.color != self.color and move_dist2 <= piece_dist2:
                            continue

                        blocked_moves.append(dr_move)
                    break
        
        return [move for move in moves if move not in blocked_moves]
