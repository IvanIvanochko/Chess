import pygame
from Pieces import *

class Board:
    def __init__(self, screen, color, screen_info):
        self.IS_WHITE_BOTTOM = (color == WHITE)
        self.IS_WHITES_TURN = True

        self.screen = screen
        self.screen_info = screen_info
        self.square_size = self.screen_info.board_size // 8 # Floor division to get the size of each square on the board

        self.__board_img = pygame.image.load("Materials/Pieces/board.png")
        self.board = pygame.transform.scale(self.__board_img, (self.screen_info.board_size, self.screen_info.board_size))

        self.__hint_img = pygame.image.load("Materials/hint.png").convert_alpha()
        self.hint = pygame.transform.scale(self.__hint_img, (self.screen_info.board_size, self.screen_info.board_size))

        self.hints = []
        for x in range(8):
            for y in range(8):
                self.hints.append(Hint(screen, x, y))

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

    def draw(self):
        self.screen.blit(self.board, (0, 0))

        for piece in self.pieces:
            piece.draw(self.screen, self.square_size)

        for hint in self.hints:
            hint.draw(self.square_size)


    def resize(self, new_size):
        self.screen = pygame.display.set_mode((new_size, new_size), pygame.RESIZABLE)
        self.square_size = self.screen.get_width() // 8

        self.board = pygame.transform.scale(self.__board_img, (self.screen.get_width(), self.screen.get_height()))

    def update_pieces_pos(self):
        """Update pieces positions"""
        self.pieces_pos = [(piece.x, piece.y) for piece in self.pieces]

    def move_piece(self, piece, x, y, is_whites_turn):
        """Move a piece and toggle turn"""
        self.record_move(piece, x, y)

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

        piece_name = piece.__class__.__name__[0].upper() if piece.__class__ != Pawn else ""
        capture_symbol = 'x' if self.move_history and self.move_history[-1] == 'x' else ''
        coordinates = f"{alphabet[x]}{8 - y}"

        move_notation = f"{piece_name}{capture_symbol}{coordinates}"

        if capture_symbol == 'x':
            self.move_history[-1] = move_notation
        else:
            self.move_history.append(move_notation)


class Hint:
    def __init__(self, screen, x, y):
        self.is_visible = False
        self.is_capture = False
        self.is_debug = False
        self.x = x
        self.y = y
        self.screen = screen
        self.__hint_img = pygame.image.load("Materials/hint.png").convert_alpha()
        self.__capture_hint_img = pygame.image.load("Materials/capture_hint.png").convert_alpha()

        self.square_size = self.screen.get_width() // 8
        self.hint = pygame.transform.scale(self.__hint_img, (self.square_size, self.square_size))
        self.capture_hint = pygame.transform.scale(self.__capture_hint_img, (self.square_size, self.square_size))

    def draw(self, square_size):
        if not self.is_visible:  # Only draw if visible
            return

        self.square_size = square_size
        
        if self.is_debug:
            # Create red debug surface
            hint_surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            hint_surface.fill((255, 0, 0, 128))  # Red with 50% transparency
        else:
            self.resize()
            hint_surface = self.capture_hint if self.is_capture else self.hint
        
        self.screen.blit(hint_surface, (self.x * self.square_size, self.y * self.square_size))

    def resize(self):
        self.hint = pygame.transform.scale(self.__hint_img, (self.square_size, self.square_size))
        self.capture_hint = pygame.transform.scale(self.__capture_hint_img, (self.square_size, self.square_size))

    def show(self, is_capture=False):
        self.is_visible = True
        self.is_capture = is_capture
        self.is_debug = False

    def show_debug(self):
        self.is_visible = True
        self.is_capture = False
        self.is_debug = True
    
    def hide(self):
        self.is_visible = False
        self.is_capture = False
        self.is_debug = False

    