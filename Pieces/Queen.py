import pygame
from .ChessPiece import ChessPiece, WHITE

class Queen(ChessPiece):
    def __init__(self, screen, x, y, color, board):
        super().__init__(screen, x, y, color, board)
        self.color = color
        if self.color == WHITE:
            self.image = pygame.image.load("Materials/Pieces/wq.png").convert_alpha()
        else:
            self.image = pygame.image.load("Materials/Pieces/bq.png").convert_alpha()
    
    def get_moves(self):
        """Return a list of standard moves for the queen"""
        relative_moves = []

        for i in range(0, 7):
            relative_moves.append([i, 0])
            relative_moves.append([0, i])
            relative_moves.append([-i, 0])
            relative_moves.append([0, -i])
            
            relative_moves.append([i, i])
            relative_moves.append([-i, i])
            relative_moves.append([i, -i])
            relative_moves.append([-i, -i])

        moves = []
        for dx, dy in relative_moves:
            new_x = self.x + dx
            new_y = self.y + dy

            if 0 <= new_x < 8 and 0 <= new_y < 8:
                moves.append((new_x, new_y))

        return moves

    def get_possible_moves(self):
        """Return a list of possible moves for the queen"""
        moves = ChessPiece.get_possible_moves(self)
        
        blocked_moves = []

        for m in moves:
            # Direction of Bishop movement
            drx_b = 1 if m[0] - self.x > 0 else -1
            dry_b = 1 if m[1] - self.y > 0 else -1

            # Direction of Rook movement
            drx_r = 0 if m[0] - self.x == 0 else 1 if m[0] - self.x > 0 else -1
            dry_r = 0 if m[1] - self.y == 0 else 1 if m[1] - self.y > 0 else -1

            if m in blocked_moves:
                continue

            for piece in self.board.pieces:
                if piece.x == self.x and piece.y == self.y:
                    continue

                piece_dx = piece.x - self.x
                piece_dy = piece.y - self.y
                piece_dist2 = piece_dx*piece_dx + piece_dy*piece_dy

                # If there's a piece in the way of the move (Bishop-like movement)
                if piece.x == (m[0] - drx_b) and piece.y == (m[1] - dry_b):  
                    for i in range(0, 7):
                        dr_move = (self.x + drx_b * i, self.y + dry_b * i)

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

                # If there's a piece in the way of the move (Rook-like movement)
                elif piece.x == (m[0] - drx_r) and piece.y == (m[1] - dry_r):
                    for i in range(0, 7):
                        dr_move = (self.x + drx_r * i, self.y + dry_r * i)

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
