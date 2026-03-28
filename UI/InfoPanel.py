class InfoPanel:
    def __init__(self, screen, font, screen_info, board):
        self.screen = screen
        self.font = font
        self.screen_info = screen_info
        self.board = board

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
            text_surface = self.font.render(move, True, (255, 255, 255))
            y_offset += 1 if i % 2 == 0 and i != 0 else 0
            self.screen.blit(text_surface, (self.screen_info.start_info_panel + x + (i % 2 * x_margin), y + y_offset * y_margin))
