import pygame

from board import Board
from Pieces import BLACK, WHITE
from UI import InfoPanel, ScreenInfo
from AI import AIManager    

# events
FINISHED_MOVE_EVENT = pygame.event.custom_type()

class ChessGame:
    def __init__(self):
        pygame.init()

        self.screen_info = ScreenInfo(
            board_size=700,
            info_panel_width=300
        )

        self.screen = pygame.display.set_mode((self.screen_info.total_width, self.screen_info.total_height), pygame.RESIZABLE)
        pygame.display.set_caption("Chess")
        self.font = pygame.font.Font(None, 48)

        self.board = Board(self.screen, WHITE, self.screen_info)
        self.ai_manager = AIManager(self.board, color=BLACK)

        self.info_panel = InfoPanel(self.screen, self.font, self.screen_info, self.board)

        self.selected_piece = None
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            
            self.board.draw()

            self.info_panel.display_whose_turn(10, 10)
            self.info_panel.display_move_history(10, 60)

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

        if event.type == FINISHED_MOVE_EVENT:
            if not self.board.IS_WHITES_TURN:
                print("White's turn")
                self.AI_Response()

    def AI_Response(self):
        print("AI is thinking...")
        ai_move = self.ai_manager.play_turn()

        if ai_move is None:
            return

        piece = ai_move[0]
        move = ai_move[1]

        piece.capture(move[0], move[1])

        self.board.move_piece(
            piece,
            move[0],
            move[1]
        )

        
    def handle_resize(self, event):
        width, height = event.size
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.board.resize(width * self.screen_info.board_ratio)

    def handle_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_clicked = mouse_x // self.board.square_size
        y_clicked = mouse_y // self.board.square_size
        target_square = (x_clicked, y_clicked)

        clicked_piece = self.get_piece_at(mouse_x, mouse_y)

        # No piece currently selected
        if self.selected_piece is None:
            if self.is_current_players_piece(clicked_piece):
                self.select_piece(clicked_piece)
            return

        # Deselect if clicked on the same piece
        if clicked_piece == self.selected_piece:
            self.clear_selection()
            return

        # Select another piece of the current player
        if clicked_piece and clicked_piece.color == self.selected_piece.color:
            self.select_piece(clicked_piece)
            return

        # Move or capture
        if target_square in self.selected_piece.get_possible_moves():
            self.selected_piece.capture(x_clicked, y_clicked)

            self.board.move_piece(
                self.selected_piece,
                x_clicked,
                y_clicked
            )

            self.selected_piece = None

            pygame.event.post(pygame.event.Event(FINISHED_MOVE_EVENT, reason="finished move"))

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