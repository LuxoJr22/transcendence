import asyncio
from .player_class import Player

class Game:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.ballx = 0
		self.balldir = 1
		self.player1 = Player(-10, 0)
		self.player2 = Player(10, 0)


	def update(self):
		self.ballx += 0.2 * self.balldir
		self.collisions()
		self.player1.move()
		self.player2.move()


	def collisions(self):
		if (self.ballx >= self.player2.x - 0.7 and self.balldir == 1):
			self.balldir = -1
		if (self.ballx <= self.player1.x + 0.7 and self.balldir == -1):
			self.balldir = 1


	def lerp(self, first, second, inter):
		diff = second - first
		return (first + (diff * inter))
	#def checkCollisions(self):