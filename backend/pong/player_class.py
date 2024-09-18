from .utils import lerp

class Player:
	def __init__(self, x, y, limit, side):
		self.x = x
		self.y = y
		self.side = side
		self.score = 0
		self.limit = limit
		self.knockback = 0
		self.charge = 0
		self.charging = 1
		self.controller = {"xp": 0, "xn": 0, "yp": 0, "yn": 0, "charge": 0}

	def move(self, dt):
		self.knockback = lerp(self.knockback, 0, 0.1, dt)
		mx = self.controller["xp"] + self.controller["xn"] + self.knockback
		my = self.controller["yp"] + self.controller["yn"]

		if (self.controller["charge"]):
			mx = mx / 2
			my = my / 2

		if not ((mx > 0 and self.x >= self.limit["px"]) or (mx < 0 and self.x <= self.limit["nx"])):
			self.x += mx * dt
		if not ((my > 0 and self.y >= self.limit["py"]) or (my < 0 and self.y <= self.limit["ny"])):
			self.y += my * dt
		if (self.controller["charge"] == 0 and self.charge):
			self.knockback = self.charging / 10 * self.side

		if (self.controller["charge"] == 1):
			self.charging = lerp(self.charging, 5, 0.05, dt)
			self.charge  = 1
		else:
			self.charging = lerp(self.charging, 1, 0.1, dt)
			self.charge = 0
		

		
