from .player_class import Player

class Game:
	def __init__(self):
		self.t = 0
		self.player1 = Player(27, 3, 34)
		self.player2 = Player(37, 11, 4)