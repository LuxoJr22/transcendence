class Player:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.controller = {"xp": 0, "xn": 0, "yp": 0, "yn": 0, "charge": 0}
		self.bind = {"up": 83, "down": 90, "left":68, "right":81, "charge":32}

	def move(self):
		mx = self.controller["xp"] + self.controller["xn"]
		my = self.controller["yp"] + self.controller["yn"]

		self.x -= mx
		self.y -= my

	def keydown (self, keyCode):
		if keyCode == self.bind["up"]:
			self.controller["yp"] = 0.15
		if keyCode == self.bind["down"]:
			self.controller["yn"] = -0.15
		if keyCode == self.bind["left"]:
			self.controller["xn"] = -0.15
		if keyCode == self.bind["right"]:
			self.controller["xp"] = 0.15
		if keyCode == self.bind["charge"]:
			self.controller["charge"] = 1

	def keyup (self, keyCode):
		if keyCode == self.bind["up"]:
			self.controller["yp"] = 0
		if keyCode == self.bind["down"]:
			self.controller["yn"] = 0
		if keyCode == self.bind["left"]:
			self.controller["xn"] = 0
		if keyCode == self.bind["right"]:
			self.controller["xp"] = 0

		if keyCode == self.bind["charge"]:
			self.controller["charge"] = 0