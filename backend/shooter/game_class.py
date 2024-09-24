from .flag_class import Flag
import math

class Game:
	def __init__(self):
		self.last = 0
		self.t = 0
		self.ids = {}
		self.players = []
		self.flag = Flag()

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