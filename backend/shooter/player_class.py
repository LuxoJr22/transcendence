class Player:
	def __init__(self, x, y, z, spawn, rotaspawn):
		self.position = {'x': x, 'y':y, 'z':z}
		self.direction = {'x': 0, 'y':0, 'z':0}
		self.controller = {"xp": 0, "xn": 0, "yp": 0, "yn": 0, "jump":0}
		self.score = 0
		self.spawn = spawn
		self.rotaspawn = rotaspawn
		self.hit = 0
	