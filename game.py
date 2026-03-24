import pygame

from board import Board
from Pieces import BLACK, WHITE


class ChessGame:
    def __init__(self, window_size=700):
        pygame.init()
        self.screen = pygame.display.set_mode((window_size, window_size), pygame.RESIZABLE)
        pygame.display.set_caption("Chess")

        self.board = Board(self.screen, WHITE)
        self.selected_piece = None
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.board.draw()

            for event in pygame.event.get():
                self.handle_event(event)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return

        if event.type == pygame.VIDEORESIZE:
            self.handle_resize(event)
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click()

    def handle_resize(self, event):
        size = min(event.size[0], event.size[1])
        self.screen = pygame.display.set_mode((size, size), pygame.RESIZABLE)
        self.board.resize(size)

    def handle_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_clicked = mouse_x // self.board.square_size
        y_clicked = mouse_y // self.board.square_size
        target_square = (x_clicked, y_clicked)

        clicked_piece = self.get_piece_at(mouse_x, mouse_y)

        if self.selected_piece is None:
            if self.is_current_players_piece(clicked_piece):
                self.select_piece(clicked_piece)
            return

        if clicked_piece == self.selected_piece:
            self.clear_selection()
            return

        if clicked_piece and clicked_piece.color == self.selected_piece.color:
            self.select_piece(clicked_piece)
            return

        if target_square in self.selected_piece.get_possible_moves():
            if clicked_piece and clicked_piece.color != self.selected_piece.color:
                self.selected_piece.capture(x_clicked, y_clicked)

            self.board.IS_WHITES_TURN = self.board.move_piece(
                self.selected_piece,
                x_clicked,
                y_clicked,
                self.board.IS_WHITES_TURN,
            )
            self.selected_piece = None
            return

        self.clear_selection()

    def get_piece_at(self, mouse_x, mouse_y):
        for piece in self.board.pieces:
            if piece.is_clicked(mouse_x, mouse_y):
                return piece
        return None

    def is_current_players_piece(self, piece):
        if piece is None:
            return False

        return (
            self.board.IS_WHITES_TURN
            and piece.color == WHITE
            or not self.board.IS_WHITES_TURN
            and piece.color == BLACK
        )

    def select_piece(self, piece):
        if self.selected_piece:
            self.selected_piece.deselect()

        self.selected_piece = piece
        self.selected_piece.select()

    def clear_selection(self):
        if self.selected_piece:
            self.selected_piece.deselect()
            self.selected_piece = None
