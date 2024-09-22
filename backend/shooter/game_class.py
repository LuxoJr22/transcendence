from .player_class import Player
import math

class Game:
	def __init__(self):
		self.t = 0
		self.players = []
		self.players.append(Player(27, 3, 34, {'x': 104, 'y':1, 'z':0}, {'x':0, 'y':math.pi / 2, 'z':0}))
		self.players.append(Player(37, 11, 4, {'x': -104, 'y':1, 'z':0}, {'x':0, 'y':-math.pi / 2, 'z':0}))