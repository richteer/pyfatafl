import re

class Move():
	piece = None
	x = -1
	y = -1
	gex = None
	player = ""

	def __init__(self, piece=None, x=-1,y=-1, player=""):
		self.piece = piece
		self.x = -1
		self.y = -1
		self.gex = re.compile("([wb]) (\d|a),(\d|a) (\d|a),(\d|a)")
		self.player = player

	def parse(self, string, board):
		m = self.gex.match(string)
		if not m:
			return None

		self.player = "white" if m.group(1) == "w" else "black"
		self.x, self.y = (int("0x"+m.group(4),0), int("0x"+m.group(5),0))
		self.piece = board.tiles[int("0x"+m.group(2),0)][int("0x"+m.group(3),0)]
		if not self.piece:
			print("warning, no piece found")
		return self

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
	over = False

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
[bp(), bp(), None, wp(), wp(), kp(), wp(), wp(), None, bp(), bp()],
[bp(), None, None, None, wp(), wp(), wp(), None, None, None, bp()],
[bp(), None, None, None, None, wp(), None, None, None, None, bp()],
[None, None, None, None, None, None, None, None, None, None, None],
[None, None, None, None, None, bp(), None, None, None, None, None],
[None, None, None, bp(), bp(), bp(), bp(), bp(), None, None, None],
]
		# Set pieces to have their location internally
		for i in range(self.size):
			for j in range(self.size):
				if self.tiles[i][j]:
					self.tiles[i][j].x = i
					self.tiles[i][j].y = j

	def _check_path(self, move):
		px,py = (move.x-move.piece.x, move.y-move.piece.y)
		p = abs(px) if px else abs(py)
		px,py = (-1 if px < 0 else 1 if px != 0 else 0, -1 if py < 0 else 1 if py != 0 else 0)
		a = self.size - 1

		for dx, dy in [(i*px, i*py) for i in range(1,p+1)]:
			if self.tiles[move.piece.x+dx][move.piece.y+dy]:
				return False
			# Fail on crossing the throne if not king
			elif move.piece.x + dx == move.piece.y + dy == self.size // 2 and move.piece.color != "king":
				return False
			# Fail on exit if not king
			elif (move.piece.x+dx,move.piece.y+dy) in [(0,0), (0,a), (a,0), (a, a)] and move.piece.color != "king":
				return False

		return True

	def move(self, move):
		if not move:
			raise Exception("NoneMoveObject")
		elif not move.piece:
			raise Exception("NoneMovePiece")
		elif move.piece.owner != move.player:
			raise Exception("IncorrectPlayer")
		elif move.piece.x != move.x and move.piece.y != move.y or not self._check_path(move):
			raise Exception("BadMove")

		self.tiles[move.x][move.y] = move.piece
		self.tiles[move.piece.x][move.piece.y] = None
		move.piece.x = move.x
		move.piece.y = move.y

		self._update(move.piece)

	def _update(self, piece):

		a = self.size - 1
		if piece.color == "king" and (piece.x,piece.y) in [(0,0), (0,a), (a,0), (a, a)]:
			self.over = "white"

		for x,y in [(0,-1),(0,1),(-1,0),(1,0)]:
			px = piece.x + x
			py = piece.y + y
			if px < 0 or px >= self.size or py < 0 or py >= self.size:
				continue # OOB
			if self.tiles[px][py] != None:
				if self.tiles[px][py].color == "king":
					self.over = "black"
					for dx, dy in [(0,-1),(0,1),(1,0),(-1,0)]:
						if px < 0 or px >= self.size or py < 0 or py >= self.size:
							self.over = False
							break
						elif not self.tiles[px+dx][py+dy] or self.tiles[px+dx][py+dy].color != "black":
							self.over = False
							break
					pass # put king logic here
				elif self.tiles[px][py].color != piece.color:
					dpx = px + x
					dpy = py + y
					if px < 0 or px >= self.size or py < 0 or py >= self.size:
						continue # OOB
					elif self.tiles[dpx][dpy] and self.tiles[dpx][dpy].color == piece.color:
						self.tiles[px][py] = None
						continue
				

	def show(self):
		print("  " + " ".join([hex(i).replace("0x","") for i in range(self.size)]))
		print(("-".join([" "] + ["-" for i in range(self.size)])+"\n").join([hex(int(i)).replace("0x","") + "|" + "|".join([(lambda p: " " if not p else p.color[0])(j) for j in self.tiles[i]] + ["\n"]) for i in range(self.size)]))

if __name__ == "__main__":
	b = Board()
	turn = "bw"
	t = False
	b.show()
	while not b.over:
		string = input(turn[t]+" move? ")
		m = Move().parse(turn[t] + " " + string, b)
		try:
			b.move(m)
		except Exception as e:
			print(e)
			continue
		t = not t
		b.show()
	print(b.over,"wins!")
		
