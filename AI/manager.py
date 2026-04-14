from Pieces import BLACK, WHITE

from AI.engines.minimax_engine import MinimaxEngine
from AI.engines.random_engine import RandomEngine


class AIManager:
	def __init__(self, board, color=BLACK, technique="random"):
		self.board = board
		self.color = color
		self.technique = technique
		self.engine = self._create_engine()

	def set_technique(self, technique):
		"""Change the AI's strategy."""
		self.technique = technique
		self.engine = self._create_engine()

	def _create_engine(self):
		if self.technique == "random":
			return RandomEngine(self.board, self.color)
		if self.technique == "minimax":
			return MinimaxEngine(self.board, self.color)

		raise ValueError(f"Unsupported AI technique: {self.technique}")

	def play_turn(self):
		"""Entry point for AI turns."""
		own_pieces = []
		
		if self.board.IS_WHITES_TURN and self.color == WHITE:
			own_pieces = [piece for piece in self.board.pieces if piece.color == WHITE]
		elif not self.board.IS_WHITES_TURN and self.color == BLACK:
			own_pieces = [piece for piece in self.board.pieces if piece.color == BLACK]

		movable_pieces = [piece for piece in own_pieces if piece.get_possible_moves()]
		
		return self.engine.play_turn(movable_pieces)
