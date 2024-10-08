import asyncio
import time
from .player_class import Player
from .utils import lerp

class Game:
	def __init__(self, gamemode, game_id, player1, player2):
		self.game_id = game_id
		self.t = -time.perf_counter()
		self.endscoring = 0
		self.winner = 0
		self.scoring = 0
		self.lastscore = 1
		self.game_state = 0
		self.gamemode = gamemode
		self.limit = {'yp':7, 'yn':-7}
		self.ballx = 0
		self.bally = 0
		self.balldir = 1.5
		self.last = 0
		self.balldiry = 0
		self.ballspeed = 1
		if (self.gamemode == "pong"):
			self.player1 = Player(-10, 0, {"px": 0, "py":8, "nx":-18, "ny":-8}, 1, player1)
			self.player2 = Player(10, 0, {"px": 18, "py":8, "nx": 0, "ny":-8}, -1, player2)
		else :
			self.player1 = Player(-17, 0, {"px": 0, "py":8, "nx":-18, "ny":-8}, 1, player1)
			self.player2 = Player(17, 0, {"px": 18, "py":8, "nx": 0, "ny":-8}, -1, player2)
			self.limit = {'yp': 10, 'yn':-10}


	def update(self):
		t = self.last
		self.last = time.perf_counter()
		dt = self.last - t
		if (t == 0):
			dt = 0
		self.t += dt
		dt *= 100
		if (not self.scoring):
			self.ballx += 0.2 * self.balldir * dt
			self.bally += 0.5 * self.balldiry * dt
		self.collisions(dt)
		self.player1.move(dt)
		self.player2.move(dt)


	def collisions(self, dt):
		if (self.ballx <= self.player2.x + 0.7 and self.ballx >= self.player2.x - 0.7 and self.balldir > 0 and self.bally >= self.player2.y - 2 and self.bally <= self.player2.y + 2
	  			and self.player2.controller["charge"] == 0):
			self.balldiry = (self.bally - self.player2.y) * 0.2
			if (self.balldir > 1.5):
				self.player2.knockback = 0.4
			self.balldir = -1 * self.player2.charging

		if (self.ballx <= self.player1.x + 0.7 and self.ballx >= self.player1.x - 0.7 and self.balldir < 0 and self.bally >= self.player1.y - 2 and self.bally <= self.player1.y + 2
	  			and self.player1.controller["charge"] == 0):
			self.balldiry = (self.bally - self.player1.y) * 0.2
			if (self.balldir < -1.5):
				self.player1.knockback = -0.4
			self.balldir = 1 * self.player1.charging

		if (self.balldir < 0):
			self.balldir = lerp(self.balldir, -self.ballspeed, 0.05, dt)
		if (self.balldir > 0 ):
			self.balldir = lerp(self.balldir, self.ballspeed, 0.05, dt)
		if ((self.bally >= self.limit["yp"] and self.balldiry > 0) or (self.bally <= self.limit["yn"] and self.balldiry < 0)):
			self.balldiry *= -1
		if (self.ballx >= 18 or self.ballx <= -18):
			if (self.ballx >= 18):
				self.player1.score += 1
				self.lastscore = 1
				if self.player1.score >= 11 and self.winner == 0:
					self.winner = self.player1.id
			if (self.ballx <= -18):
				self.player2.score += 1
				self.lastscore = -1
				if self.player2.score >= 11 and self.winner == 0:
					self.winner = self.player2.id
			self.scoring = 1
			self.ballx = 0
			self.bally = 16
			self.endscoring = self.t + 2
			if (self.winner):
				self.endscoring += 20
		if (self.endscoring < self.t and self.scoring):
			self.reset()

	def reset(self):
		self.scoring = 0
		self.ballx = 0
		self.bally = 0
		self.balldir = 1.5 * self.lastscore
		self.balldiry = 0
		self.ballspeed = 1
		
		self.player2.y = 0
		self.player1.y = 0
		if (self.gamemode == 'pong'):
			self.player1.x = -10
			self.player2.x = 10
		else:
			self.player1.x = -17
			self.player2.x = 17
		
		

