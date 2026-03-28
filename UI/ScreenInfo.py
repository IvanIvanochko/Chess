class ScreenInfo:
    def __init__(self, board_size, info_panel_width):
            self._board_size = board_size
            self._info_panel_width = info_panel_width

    @property
    def board_size(self):
        return self._board_size
    
    @board_size.setter
    def board_size(self, new_board_size):
        self._board_size = new_board_size

    @property
    def start_info_panel(self):
        return self._board_size
    
    @property
    def total_width(self):
        return self.board_size + self._info_panel_width
    
    @property
    def total_height(self):
        return self.board_size
    
    @property
    def board_ratio(self):
        return self.board_size / self.total_width
    
    @property
    def info_panel_ratio(self):
        return self._info_panel_width / self.total_width
