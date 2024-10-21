import time

class Flag:
	def __init__(self):
		self.last = 0
		self.position = {'x':0, 'y':8, 'z':-5}
		self.ispicked = 0
		self.isdropped = 0
		self.player_id = 0
		self.players_in = []
		self.poss = 0

	def checkPlayer(self, position, id, dt):
		if (self.is_in(position)):
			if (id not in self.players_in):
				self.players_in.append(id)
			if (len(self.players_in) == 1):
				self.poss += dt
				if (self.poss >= 5):
					self.poss = 0
					self.player_id = self.players_in[0]
					self.players_in.pop()
			else:
				self.poss = 0
		else:
			if (id in self.players_in):
				self.players_in.remove(id)

		if (self.player_id == id and not self.is_in(position)):
			self.player_id = 0


	def is_in(self, position):
		if (position['x'] >= self.position['x'] - 7.5 and position['x'] <= self.position['x'] + 7.5
	  		and	position['y'] >= self.position['y'] and position['y'] <= self.position['y']+ 5
			and position['z'] >= self.position['z'] - 7.5 and position['z'] <= self.position['z'] + 7.5):
			return (1)
		return (0)
		

	
	