import math

import pygame
from Pieces import *
from UI import Hint

class Board:
    def __init__(self, screen, color, screen_info):
        self.IS_WHITE_BOTTOM = (color == WHITE)
        self.IS_WHITES_TURN = True

        self.screen = screen
        self.screen_info = screen_info
        self.__board_img = pygame.image.load("Materials/Pieces/board.png")
        self.board = pygame.transform.scale(self.__board_img, (self.screen_info.board_size, self.screen_info.board_size))

        self.__hint_img = pygame.image.load("Materials/hint.png").convert_alpha()
        self.hint = pygame.transform.scale(self.__hint_img, (self.square_size , self.square_size))

        self.hints = []
        for x in range(8):
            for y in range(8):
                self.hints.append(Hint(screen, x, y, self))

        self.captured_pieces = []
        self.pieces = []
        for x in range(8):
            self.pieces.append(Pawn(screen, x, 6, WHITE, self)) # wp
            self.pieces.append(Pawn(screen, x, 1, BLACK, self)) # bp

        self.pieces.append(Queen(screen, 3, 7, WHITE, self)) # wq
        self.pieces.append(Queen(screen, 3, 0, BLACK, self)) # bq

        self.pieces.append(Bishop(screen, 2, 7, WHITE, self)) # wb
        self.pieces.append(Bishop(screen, 5, 7, WHITE, self)) # wb
        self.pieces.append(Bishop(screen, 2, 0, BLACK, self)) # bb
        self.pieces.append(Bishop(screen, 5, 0, BLACK, self)) # bb

        self.pieces.append(Knight(screen, 1, 7, WHITE, self)) # wn
        self.pieces.append(Knight(screen, 6, 7, WHITE, self)) # wn
        self.pieces.append(Knight(screen, 1, 0, BLACK, self)) # bn
        self.pieces.append(Knight(screen, 6, 0, BLACK, self)) # bn

        self.pieces.append(Rook(screen, 0, 7, WHITE, self)) # wr
        self.pieces.append(Rook(screen, 7, 7, WHITE, self)) # wr
        self.pieces.append(Rook(screen, 0, 0, BLACK, self)) # br
        self.pieces.append(Rook(screen, 7, 0, BLACK, self)) # br

        self.pieces.append(King(screen, 4, 7, WHITE, self)) # wk
        self.pieces.append(King(screen, 4, 0, BLACK, self)) # bk

        self.pieces_pos = []
        for piece in self.pieces:
            self.pieces_pos.append((piece.x, piece.y))

        self.move_history = []

    @property
    def square_size(self):
        return int(self.screen_info.board_size // 8)
    
    @property
    def pos_offset_compensation(self):
        return 1 if (self.screen_info.board_size % 8) != 0 else 0

    def position_img(self, x, y):
        """Return the position of the top left corner of the square at (x, y)"""
        return (x * self.square_size + self.pos_offset_compensation, y * self.square_size + self.pos_offset_compensation)

    def draw(self):
        self.screen.blit(self.board, (0, 0))

        for piece in self.pieces:
            piece.draw(self.screen, self.square_size)

        for hint in self.hints:
            # if (hint.x, hint.y) == (1, 1):
            #     hint.show_debug()
            #     print(f"Hint at (1, 1): {hint.x * self.square_size, self.pos_offset_compensation}")
            hint.draw(self.square_size)


    def resize(self, new_size):
        self.screen_info._board_size = int(new_size)
        self.board = pygame.transform.scale(self.__board_img, (int(new_size), int(new_size)))
        self.hint = pygame.transform.scale(self.__hint_img, (self.square_size, self.square_size))

    def update_pieces_pos(self):
        """Update pieces positions"""
        self.pieces_pos = [(piece.x, piece.y) for piece in self.pieces]

    def move_piece(self, piece, x, y, is_whites_turn):
        """Move a piece and toggle turn"""
        piece.move(x, y)
        self.update_pieces_pos()
        piece.deselect()

        return not is_whites_turn
    
    def remove_piece(self, x, y):
        """Remove a piece from the board"""
        for piece in self.pieces:
            if (piece.x, piece.y) == (x, y):
                self.move_history.append('x') # Record the capture in move history

                self.captured_pieces.append(piece)
                self.pieces.remove(piece)
                self.update_pieces_pos()
                break
    
    def record_move(self, piece, x, y):
        """Record a move in the move history"""
        alphabet = "abcdefgh"

        capture_symbol = 'x' if self.move_history and self.move_history[-1] == 'x' else ''
        coordinates = f"{alphabet[x]}{8 - y}"

        move_notation = f"{piece.piece_notation}{capture_symbol}{coordinates}"

        if capture_symbol == 'x':
            self.move_history[-1] = move_notation
        else:
            self.move_history.append(move_notation)

    def record_custom_move(self, notation):
        """Record a custom move in the move history (e.g. for castling)"""
        self.move_history.append(notation)

    