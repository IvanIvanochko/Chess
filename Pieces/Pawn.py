import pygame

from Pieces.Queen import Queen
from .ChessPiece import ChessPiece, WHITE

class Pawn(ChessPiece):
    def __init__(self, screen, x, y, color, board):
        super().__init__(screen, x, y, color, board)
        self.piece_notation = ""

        if self.color == WHITE:
            self.image = pygame.image.load("Materials/Pieces/wp.png").convert_alpha()
        else:
            self.image = pygame.image.load("Materials/Pieces/bp.png").convert_alpha()
        
        self.two_sqr_fwd = False # Track if the pawn just moved two squares forward (for en passant)
        self.step_counter = 0 # Track how many moves have been made since this pawn's last move (for en passant)

        self.AFTER_MOVE_L_NEIGHBOR = False
        self.AFTER_MOVE_R_NEIGHBOR = False

        self.en_passant_pieces = []


    def move(self, x, y, record_move=True):
        if self.step_counter > 1:
            self.two_sqr_fwd = False

        if abs(y - self.y) == 2 and not self.has_moved:
            self.two_sqr_fwd = True
            if record_move:
                self.step_counter = 2

            super().move(x, y, record_move=record_move)
            return
    
        super().move(x, y, record_move=record_move)

        if record_move:
            self.step_counter += 1
        
            for piece in self.board.pieces:
                if piece.y == self.y:
                    if (piece.x - self.x) == 1:
                        self.AFTER_MOVE_R_NEIGHBOR = True
                    if (piece.x - self.x) == -1:
                        self.AFTER_MOVE_L_NEIGHBOR = True
        
        if record_move and self.y == (0 if self.board.IS_WHITE_BOTTOM == (self.color == WHITE) else 7):
            self.promote(Queen)
    
    def promote(self, new_piece_class):
        """Promote this pawn to a new piece type"""
        new_piece = new_piece_class(self.screen, self.x, self.y, self.color, self.board)
        index = self.board.pieces.index(self)
        self.board.pieces[index] = new_piece

    
    def get_moves(self):
        """Return a list of standard moves for the pawn"""
        relative_moves = [[0, 1], [-1, 1], [1, 1]] + ([[0, 2]] if not self.has_moved else [])

        if self.board.IS_WHITE_BOTTOM == (self.color == WHITE):
            relative_moves = [[0, -1], [1, -1], [-1, -1]] + ([[0, -2]] if not self.has_moved else [])

        moves = []
        for dx, dy in relative_moves:
            new_x = self.x + dx
            new_y = self.y + dy

            if 0 <= new_x < 8 and 0 <= new_y < 8:
                moves.append((new_x, new_y))

        return moves
    
    def get_possible_moves(self):
        moves = super().get_possible_moves()
        # print(f"Has moved: {self.has_moved} | two_sqr_fwd: {self.two_sqr_fwd} | step_counter: {self.step_counter}")
        moves = self.left_right_atck(moves)
        moves = self.en_passant(moves)
        return moves
    
    def left_right_atck(self, moves, LEFT_ATCK=False, RIGHT_ATCK=False):
        """Check if there are pieces to the left or right of the pawn that it can attack"""
        blocked_moves = []
        for (x, y) in moves:
            dx = x - self.x

            if dx == 0:
                for piece in self.board.pieces:
                    if piece.x == x and piece.y == y:
                        blocked_moves.append((x, y))
                        break
                continue
            elif dx == 1 and not RIGHT_ATCK:
                for piece in self.board.pieces:
                    if piece.x == x and piece.y == y: 
                        RIGHT_ATCK = True
                        break
            elif dx == -1 and not LEFT_ATCK:
                for piece in self.board.pieces:
                    if piece.x == x and piece.y == y: 
                        LEFT_ATCK = True
                        break

        for (x, y) in moves:
            dx = x - self.x
            if dx == 1 and not RIGHT_ATCK:
                blocked_moves.append((x, y))
            elif dx == -1 and not LEFT_ATCK:
                blocked_moves.append((x, y))

        return [move for move in moves if move not in blocked_moves]
    
    def en_passant(self, moves):
        """Handle en passant capture for this pawn"""
        dir = 1 if self.board.IS_WHITE_BOTTOM == (self.color == WHITE) else -1

        if self.y == (3 if self.board.IS_WHITE_BOTTOM == (self.color == WHITE) else 4):
            for piece in self.board.pieces:
                if piece.y == self.y and piece.piece_notation == "":
                    if piece.color != self.color and piece.two_sqr_fwd:
                        if (piece.x - self.x) == 1 and not self.AFTER_MOVE_R_NEIGHBOR:
                            moves.append((piece.x, piece.y - dir))
                            self.en_passant_pieces.append((piece, (piece.x, piece.y - dir)))
                            return moves
                        
                        if (piece.x - self.x) == -1 and not self.AFTER_MOVE_L_NEIGHBOR:
                            moves.append((piece.x, piece.y - dir))
                            self.en_passant_pieces.append((piece, (piece.x, piece.y - dir)))
                            return moves
        return moves
    
    def capture(self, x, y):
        """Handle piece capture"""
        if self.en_passant_pieces:
            for piece, pos in self.en_passant_pieces:
                if pos == (x, y):
                    super().capture(piece.x, piece.y)
                    return
        
        super().capture(x, y)

    def record_pawn(pawn):
        """Record a pawn move in the move history, that was an en passant move"""
        if pawn.two_sqr_fwd:
            pawn.board.move_history.append('P') # Record the pawn move in move history
        else:
            pawn.board.record_move(pawn, pawn.x, pawn.y)
    
    def attack_moves(self):
        """Return a list of attack moves for this Pawn"""
        moves = self.get_moves()

        blocked_moves = []
        for m in moves:
            dx = m[0] - self.x

            if dx == 0:
                blocked_moves.append(m)
        
        return [move for move in moves if move not in blocked_moves]

    def copy(self, board):
        new_piece = super().copy(board)
        new_piece.two_sqr_fwd = self.two_sqr_fwd
        new_piece.step_counter = self.step_counter
        new_piece.AFTER_MOVE_L_NEIGHBOR = self.AFTER_MOVE_L_NEIGHBOR
        new_piece.AFTER_MOVE_R_NEIGHBOR = self.AFTER_MOVE_R_NEIGHBOR
        new_piece.en_passant_pieces = []
        return new_piece
