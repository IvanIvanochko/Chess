import random

class RandomEngine:
	def __init__(self, board, color):
		self.board = board
		self.color = color

	def play_turn(self, pieces):
		if not pieces:
			return None

		piece = random.choice(pieces)
		possible_moves = piece.get_possible_moves()

		if not possible_moves:
			return None

		move = random.choice(possible_moves)
		return (piece, move)
