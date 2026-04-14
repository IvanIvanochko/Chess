import pygame


class InfoPanel:
    def __init__(self, screen, font, screen_info, board):
        self.screen = screen
        self.font = font
        self.screen_info = screen_info
        self.board = board
        self.undo_button_rect = pygame.Rect(
            self.screen_info.start_info_panel + 10,
            self.screen_info.total_height - 70,
            180,
            48,
        )

    def display_whose_turn(self, x, y):
        if self.board.IS_WHITES_TURN:
            text_surface = self.font.render("White's Turn", True, (255, 255, 255))
        else:
            text_surface = self.font.render("Black's Turn", True, (255, 255, 255))
            
        self.screen.blit(text_surface, (self.screen_info.start_info_panel + x, y))

    def display_move_history(self, x, y, x_margin=150, y_margin=40):
        move_history = self.board.move_history
        y_offset = 0
        for i, move in enumerate(move_history):
            text_surface = self.font.render(move["notation"], True, (255, 255, 255))
            y_offset += 1 if i % 2 == 0 and i != 0 else 0
            self.screen.blit(text_surface, (self.screen_info.start_info_panel + x + (i % 2 * x_margin), y + y_offset * y_margin))

    def draw_undo_button(self, x, y):
        self.undo_button_rect = pygame.Rect(
            self.screen_info.start_info_panel + x,
            self.screen_info.total_height + y,
            180,
            48,
        )

        pygame.draw.rect(self.screen, (70, 70, 70), self.undo_button_rect, border_radius=8)
        pygame.draw.rect(self.screen, (180, 180, 180), self.undo_button_rect, width=2, border_radius=8)

        button_font = pygame.font.Font(None, 36)
        label = button_font.render("Undo", True, (255, 255, 255))
        label_rect = label.get_rect(center=self.undo_button_rect.center)
        self.screen.blit(label, label_rect)

    def is_undo_clicked(self, mouse_x, mouse_y):
        return self.undo_button_rect.collidepoint(mouse_x, mouse_y)
