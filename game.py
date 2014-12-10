
class Player():

	color = ""

	def __init__(self, player):
		self.color = player

	def play(self):
		pass
		# Get a move here


class Piece():
	color = ""
	owner = ""
	x = -1
	y = -1

	def __init__(self, color):
		self.color = color
		if color == "king":
			self.owner = "white"
		else:
			self.owner = color

	def __str__(self):
		return self.color[0]


class Board():
	tiles = []
	size = 11

	def __init__(self):
		self._set_start()

	def __str__(self):
		ret = ""
		for i in range(self.size):
			ret += str(self.tiles[i]) + "\n"
		return ret

	def _set_start(self):
		bp = lambda: Piece("black")
		wp = lambda: Piece("white")
		kp = lambda: Piece("king")

		self.tiles = [
[None, None, None, bp(), bp(), bp(), bp(), bp(), None, None, None],
[None, None, None, None, None, bp(), None, None, None, None, None],
[None, None, None, None, None, None, None, None, None, None, None],
[bp(), None, None, None, None, wp(), None, None, None, None, bp()],
[bp(), None, None, None, wp(), wp(), wp(), None, None, None, bp()],
[bp(), None, None, wp(), wp(), kp(), wp(), wp(), None, bp(), bp()],
[bp(), None, None, None, wp(), wp(), wp(), None, None, None, bp()],
[bp(), None, None, None, None, wp(), None, None, None, None, bp()],
[None, None, None, None, None, None, None, None, None, None, None],
[None, None, None, None, None, bp(), None, None, None, None, None],
[None, None, None, bp(), bp(), bp(), bp(), bp(), None, None, None],
]
		# Set pieces to have their location internally
		for i in range(size):
			for j in range(size):
				if self.tiles[i][j]:
					self.tiles[i][j].x = i
					self.tiles[i][j].y = i

	def _check_path(self, move):
		pass

	def move(self, move):
		if move.piece !=  move.player:
			raise Exception("IncorrectPlayerMove")
		elif move.piece.x != move.x and move.piece.y != move.y:
			raise Exception("BadMove")
		# Add cases for corners and center piece
		self._check_path(move)

		self.tiles[move.x][move.y] = self.tiles.piece
		self.tiles[move.piece.x][move.piece.y] = None
