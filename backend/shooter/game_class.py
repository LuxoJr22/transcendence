from .player_class import Player
import math

class Game:
	def __init__(self):
		self.t = 0
		self.ids = {}
		self.players = []

	def CreatePlayer(self, x, y, z, spawn, rotaspawn, skin):
		return {
		'skin': skin,
		'position' : {'x': x, 'y':y, 'z':z},
		'direction' : {'x': 0, 'y':0, 'z':0},
		'controller' : {"xp": 0, "xn": 0, "yp": 0, "yn": 0, "jump":0},
		'score' : 0,
		'spawn' : spawn,
		'rotaspawn' : rotaspawn,
		'hit' : 0,
		}