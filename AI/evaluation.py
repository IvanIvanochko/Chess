from Pieces import Bishop, King, Knight, Pawn, Queen, Rook


PIECE_VALUES = {
	Pawn: 100,
	Knight: 320,
	Bishop: 330,
	Rook: 500,
	Queen: 900,
	King: 0,
}


PIECE_SQUARE_TABLES = {
	Pawn: [
		[ 0,   0,   0,   0,   0,   0,   0,   0],
		[ 5,  10,  10, -20, -20,  10,  10,   5],
		[ 5,  -5, -10,   0,   0, -10,  -5,   5],
		[ 0,   0,   0,  20,  20,   0,   0,   0],
		[ 5,   5,  10,  25,  25,  10,   5,   5],
		[10,  10,  20,  30,  30,  20,  10,  10],
		[50,  50,  50,  50,  50,  50,  50,  50],
		[ 0,   0,   0,   0,   0,   0,   0,   0],
	],
	Knight: [
		[-50, -40, -30, -30, -30, -30, -40, -50],
		[-40, -20,   0,   0,   0,   0, -20, -40],
		[-30,   0,  10,  15,  15,  10,   0, -30],
		[-30,   5,  15,  20,  20,  15,   5, -30],
		[-30,   0,  15,  20,  20,  15,   0, -30],
		[-30,   5,  10,  15,  15,  10,   5, -30],
		[-40, -20,   0,   5,   5,   0, -20, -40],
		[-50, -40, -30, -30, -30, -30, -40, -50],
	],
	Bishop: [
		[-20, -10, -10, -10, -10, -10, -10, -20],
		[-10,   0,   0,   0,   0,   0,   0, -10],
		[-10,   0,   5,  10,  10,   5,   0, -10],
		[-10,   5,   5,  10,  10,   5,   5, -10],
		[-10,   0,  10,  10,  10,  10,   0, -10],
		[-10,  10,  10,  10,  10,  10,  10, -10],
		[-10,   5,   0,   0,   0,   0,   5, -10],
		[-20, -10, -10, -10, -10, -10, -10, -20],
	],
	Rook: [
		[ 0,  0,  0,  5,  5,  0,  0,  0],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[ 5, 10, 10, 10, 10, 10, 10,  5],
		[ 0,  0,  0,  0,  0,  0,  0,  0],
	],
	Queen: [
		[-20, -10, -10, -5, -5, -10, -10, -20],
		[-10,   0,   0,  0,  0,   5,   0, -10],
		[-10,   0,   5,  5,  5,   5,   5, -10],
		[ -5,   0,   5,  5,  5,   5,   0,  -5],
		[  0,   0,   5,  5,  5,   5,   0,  -5],
		[-10,   5,   5,  5,  5,   5,   0, -10],
		[-10,   0,   5,  0,  0,   0,   0, -10],
		[-20, -10, -10, -5, -5, -10, -10, -20],
	],
	King: [
		[-30, -40, -40, -50, -50, -40, -40, -30],
		[-30, -40, -40, -50, -50, -40, -40, -30],
		[-30, -40, -40, -50, -50, -40, -40, -30],
		[-30, -40, -40, -50, -50, -40, -40, -30],
		[-20, -30, -30, -40, -40, -30, -30, -20],
		[-10, -20, -20, -20, -20, -20, -20, -10],
		[ 20,  20,   0,   0,   0,   0,  20,  20],
		[ 20,  30,  10,   0,   0,  10,  30,  20],
	],
}


def _mirror_row(y):
	return 7 - y


def get_piece_value(piece):
	return PIECE_VALUES.get(type(piece), 0)


def get_piece_square_value(piece):
	table = PIECE_SQUARE_TABLES.get(type(piece))
	if table is None:
		return 0

	row = piece.y if piece.color == "WHITE" else _mirror_row(piece.y)
	return table[row][piece.x]


def evaluate_piece(piece):
	return get_piece_value(piece) + get_piece_square_value(piece)


def evaluate_board(board, perspective_color=None):
	"""Return a score in centipawns.

	Positive means White is better by default, or the given perspective_color is better if provided.
	"""
	score = 0

	for piece in board.pieces:
		piece_score = evaluate_piece(piece)
		if piece.color == "WHITE":
			score += piece_score
		else:
			score -= piece_score

	if perspective_color == "BLACK":
		score = -score

	return score