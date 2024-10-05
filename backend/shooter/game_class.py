from .flag_class import Flag
import math
import sys
import time



class Game:
	def __init__(self):
		self.game_state = 0
		self.last = 0
		self.winner = 0
		self.timer = -time.perf_counter()
		self.ids = {}
		self.players = []
		self.flag = Flag()

	def CreatePlayer(self, id, user_id, skin, username):
		sidenb = (id // 2)
		spawn = {'x': 100 * math.pow(-1, id) , 'y':0, 'z':0  + (sidenb * 5 *  math.pow(-1, sidenb))}
		rotaspawn = {'x':0, 'y':math.pi / 2 * math.pow(-1, id), 'z':0}
		return {
		'skin': skin,
		'username': username,
		'position' : spawn,
		'direction' : {'x': 0, 'y':0, 'z':0},
		'controller' : {"xp": 0, "xn": 0, "yp": 0, "yn": 0, "jump":0},
		'score' : 0,
		'death': 0,
		'kill': 0,
		'spawn' : spawn,
		'rotaspawn' : rotaspawn,
		'hit' : 0,
		'id':user_id
		}