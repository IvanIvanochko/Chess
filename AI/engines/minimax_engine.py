from AI.evaluation import evaluate_board


class MinimaxEngine:
    def __init__(self, board, color, depth=2):
        self.board = board
        self.color = color
        self.depth = depth
        self.simulation_board = None

    def maxi(self, depth, simulation_board):
        if (depth == 0):
            return evaluate_board(simulation_board, perspective_color=self.color), None, None
        
        max_score = -float('inf')
        piece, move = None, None
        for i, (p, m) in enumerate(simulation_board.get_all_moves()):
            simulation_board.simulate_move(p, m)

            score, _, _ = self.mini(depth - 1, simulation_board)
            if score > max_score:
                max_score = score
                piece, move = p, m

            simulation_board.undo_move()

        return max_score, piece, move

    def mini( self, depth, simulation_board ):
        if (depth == 0):
            return evaluate_board(simulation_board, perspective_color=self.color), None, None
        
        min_score = float('inf')
        piece, move = None, None
        for i, (p, m) in enumerate(simulation_board.get_all_moves()):
            simulation_board.simulate_move(p, m)

            score, _, _ = self.maxi(depth - 1, simulation_board)
            if score < min_score:
                min_score = score
                piece, move = p, m

            simulation_board.undo_move()

        return min_score, piece, move
    
    def play_turn(self, pieces):
        if not pieces:
            return None

        self.simulation_board = self.board.copy()
        score, piece, move = self.mini(self.depth, self.simulation_board)
        print(f"Minimax chose move with score: {score} for piece {piece} to move to {move}")

        if piece is None or move is None:
            return None
        
        actual_piece = next((p for p in self.board.pieces if p.start_x == piece.start_x and p.start_y == piece.start_y and type(p) == type(piece)), None)

        return (actual_piece, move)