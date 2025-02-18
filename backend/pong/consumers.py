import json, time, asyncio
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.db import models
from django.shortcuts import get_object_or_404
from users.models import User
from tournament.models import Tournament
from .models import PongGroup, PongMatchmaking, PongMatch
from datetime import timedelta
from django.utils import timezone
from .game_class import Game

import sys

WAITING = 0
LAUNCHED = 1

dictio = {}


class PrivateMatchmakingConsumer(WebsocketConsumer):
	def connect(self):
		self.gamemode = self.scope['url_route']['kwargs']['gamemode']
		self.game_id = self.scope['url_route']['kwargs']['game_id']
		self.room_group_name = f'private_matchmaking_{self.game_id}'
		self.user = self.scope['user']
		
		try:
			self.matchmaking_room = get_object_or_404(PongMatchmaking, group_name=self.room_group_name)
		except:
			self.matchmaking_room = PongMatchmaking.objects.create(
				group_name = self.room_group_name,
			)
		self.accept()
		try:
			self.pongmatch = get_object_or_404(PongMatch, id=self.game_id)
		except:
			return self.close(3000, "Game found don't exist")

		if self.user.id != self.pongmatch.player1 and self.user.id != self.pongmatch.player2:
			return self.close(3000, "You are not a player in found game")

		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)

		if self.user not in self.matchmaking_room.users_online.all():
			self.matchmaking_room.users_online.add(self.user)
		
		
		
		if self.matchmaking_room.users_online.count() >= 2:
			self.player1 = self.pongmatch.player1
			self.player2 = self.pongmatch.player2

			dictio[f'{self.gamemode}_{self.game_id}'] = Game(self.gamemode, self.pongmatch.id, self.player1, self.player2)

			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name,
				{
					'type': 'Pong_match',
					'event': 'Match',
					'player1_id': self.player1,
					'player2_id': self.player2,
					'match_id':self.game_id,
				} 
			)

	def disconnect(self, code):
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)
		if self.user in self.matchmaking_room.users_online.all():
			self.matchmaking_room.users_online.remove(self.user)
		if self.matchmaking_room.users_online.count() == 0:
			self.matchmaking_room.delete()

	def Pong_match(self, event):
		self.send(text_data=json.dumps({
			'type': 'Pong_match',
			'event': 'Match',
			'player1_id': event['player1_id'],
			'player2_id': event['player2_id'],
			'gamemode': self.gamemode,
			'match_id': self.game_id,
			'room_name': f'{self.gamemode}_{self.game_id}'
		}))


class MatchmakingConsumer(WebsocketConsumer):
	def connect(self):
		self.gamemode = self.scope['url_route']['kwargs']['gamemode']
		self.room_group_name = f'{self.gamemode}_matchmaking'
		self.user = self.scope['user']
		self.t = 0
		self.range = 0

		try:
			self.matchmaking_room = get_object_or_404(PongMatchmaking, group_name=self.room_group_name)
		except:
			self.matchmaking_room = PongMatchmaking.objects.create(
				group_name = self.room_group_name,
			)

		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)

		if self.user not in self.matchmaking_room.users_online.all():
			self.matchmaking_room.users_online.add(self.user)
		
		self.accept()

		self.send(text_data=json.dumps({
			'type': 'Pong_matchmaking',
			'event': 'Research',
		}))

	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		event = text_data_json['event']
		if (event == 'Research'):
			self.doMatchmaking(text_data_json)

	def disconnect(self, code):
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)
		if self.user in self.matchmaking_room.users_online.all():
			self.matchmaking_room.users_online.remove(self.user)

	def doMatchmaking(self, event):
		currentMatch = list(PongMatch.objects.filter(
			models.Q(type="normal") & models.Q(winner=None) &
			(models.Q(player1=self.user.id) | models.Q(player2=self.user.id))))
		if currentMatch:
			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name,
				{
					'type': 'Pong_match',
					'event': 'Match',
					'player1_id': currentMatch[0].player1,
					'player2_id': currentMatch[0].player2,
					'match_id': currentMatch[0].id,
				} 
			)
			return

		if (self.range < 150 and self.t < time.perf_counter()):
			self.range += 30
			self.t = time.perf_counter() + 5
		oponents = list(self.matchmaking_room.users_online.filter(
			models.Q(pong_elo__gte=self.user.pong_elo-self.range) & 
			models.Q(pong_elo__lte=self.user.pong_elo+self.range) & 
			~models.Q(id=self.user.id)))

		if len(oponents) > 0:
			self.player1 = self.user.id
			self.player2 = oponents[0].id

			if (PongMatch.objects.filter(models.Q(player2=self.user.id) & models.Q(match_date__gte=timezone.now() - timedelta(seconds=5))).count() == 0):
				self.pongmatch = PongMatch.objects.create(
					player1 = self.player1,
					player2 = self.player2,
					gamemode = self.gamemode,
					type = "normal"
				)
				dictio[f'{self.gamemode}_{self.pongmatch.id}'] = Game(self.gamemode, self.pongmatch.id, self.player1, self.player2)

				async_to_sync(self.channel_layer.group_send)(
					self.room_group_name,
					{
						'type': 'Pong_match',
						'event': 'Match',
						'player1_id': self.player1,
						'player2_id': self.player2,
						'match_id':self.pongmatch.id,
					} 
				)
		else:
			self.send(text_data=json.dumps({
			'type': 'Pong_matchmaking',
			'event': 'Research',
			}))

	def Pong_match(self, event):
		self.send(text_data=json.dumps({
			'type': 'Pong_match',
			'event': 'Match',
			'player1_id': event['player1_id'],
			'player2_id': event['player2_id'],
			'gamemode': self.gamemode,
			'match_id': event["match_id"],
			'room_name': f'{self.gamemode}_{event["match_id"]}'
		}))


class PongConsumer(WebsocketConsumer):
	def connect(self):
		self.gamemode = self.scope['url_route']['kwargs']['gamemode']
		self.room_group_name = self.scope['url_route']['kwargs']['room_name']
		self.user = self.scope['user']
		self.id = 0
		self.winner = 0
		self.in_game = 0

		try:
			self.pongroom = get_object_or_404(PongGroup, group_name=self.room_group_name)
		except:
			self.pongroom = PongGroup.objects.create(
				group_name = self.room_group_name,
			)
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)
		self.accept()
		if (self.room_group_name not in dictio):
			return self.close(3000, "Game don't exist")
		self.game = dictio[self.room_group_name]

		if self.user not in self.pongroom.users_online.all():
			self.pongroom.users_online.add(self.user)
		if self.game.player1.id == self.user.id:
			self.id = 1
		elif self.game.player2.id == self.user.id:
			self.id = 2
		else:
			return self.close(3000, "You are not a player in this game")
		
		try:
			self.pong_match = get_object_or_404(PongMatch, id=self.game.game_id)
		except:
			return self.close(3000, "Match don't exist")
		
		self.in_game = 1
		self.send(text_data=json.dumps({
			'type':'Pong',
			'event':'Connected',
			'id':self.id
		}))

	def disconnect(self, code):
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)
		if self.user in self.pongroom.users_online.all() and self.in_game == 1:
			self.pongroom.users_online.remove(self.user)
		if self.pongroom.users_online.count() == 0:
			del self.pong_match.winner
			if (self.game.winner == 0 and self.pong_match.winner == None):
				self.pong_match.winner = self.user.id
				self.pong_match.save(update_fields=["winner"])
				self.game.winner = self.user.id
				player1 = User.objects.get(id=self.game.player1.id)
				player2 = User.objects.get(id=self.game.player2.id)
				elo_diff = (player1.pong_elo - player2.pong_elo) / 50
				if (self.game.winner == player1.id and self.pong_match.type == 'normal'):
					player1.pong_elo = player1.pong_elo + (10 - int(elo_diff))
					player2.pong_elo = player2.pong_elo - (10 - int(elo_diff))
				elif (self.pong_match.type == 'normal'):
					player2.pong_elo += (10 + int(elo_diff))
					player1.pong_elo -= (10 + int(elo_diff))
				player1.save()
				player2.save()
			del dictio[self.room_group_name]
			self.pongroom.delete()

	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		event = text_data_json['event']
		if (event == 'frame'):
			self.frame_update(text_data_json)
		if (event == 'ready'):
			self.ready(text_data_json)

	
	def ready(self, text_data_json):
		if (self.id == text_data_json["id"] == 1):
			self.game.player1.ready = 1
		if (self.id == text_data_json["id"] == 2):
			self.game.player2.ready = 1
		if (self.game.player1.ready == self.game.player2.ready == 1 and self.game.launch_game > 5):
			#time.sleep(5)
			self.game.last = 0
			self.game.game_state = LAUNCHED
			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name,
				{
					'type': 'start_game',
					'event': 'game',
				} 
			)
			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name,
				{
					'type': 'Pong_event',
					'event': 'frame',
				} 
			)
		elif self.game.player1.ready == self.game.player2.ready == 1:
			t = self.game.last
			self.game.last = time.perf_counter()
			dt = self.game.last - t
			if (t == 0):
				dt = 0
			self.game.launch_game += dt
			self.send(text_data=json.dumps({
				'type':'Pong',
				'event':'ready',
			}))

	def start_game(self, event):
		self.send(text_data=json.dumps({
			'type':'Pong',
			'event':'start_game',
		}))


	def frame_update(self, text_data_json):
		if 'player1' in text_data_json:
			self.game.player1.controller = text_data_json['player1']
			if self.id == 1:
				self.Pong_event(text_data_json['event'])
		if 'player2' in text_data_json:
			self.game.player2.controller = text_data_json['player2']
			if self.id == 2:
				self.Pong_event(text_data_json['event'])
		self.game.update()
		del self.pong_match.winner
		if (self.game.winner == self.user.id and self.pong_match.winner == None):
			self.pong_match.winner = self.game.winner
			self.pong_match.score1 = self.game.player1.score
			self.pong_match.score2 = self.game.player2.score
			self.pong_match.save()

			if self.pong_match.type == 'normal':
				player1 = User.objects.get(id=self.game.player1.id)
				player2 = User.objects.get(id=self.game.player2.id)
				elo_diff = (player1.pong_elo - player2.pong_elo) / 50
				if (self.game.winner == player1.id):
					player1.pong_elo = player1.pong_elo + (10 - int(elo_diff))
					player2.pong_elo = player2.pong_elo - (10 - int(elo_diff))
				else:
					player2.pong_elo += (10 + int(elo_diff))
					player1.pong_elo -= (10 + int(elo_diff))
				player1.save()
				player2.save()
			elif self.pong_match.type == 'tournament':
				for tournament in Tournament.objects.all():
					if self.pong_match in tournament.matchs.all():
						tour = tournament
				if (len(list(tour.matchs.filter(winner=None))) == 0):
					elem = list(tour.matchs.filter(match_date__gte=tour.last_round).values("winner"))
					if len(elem) == 1:
						return
					for el in elem:
						async_to_sync(self.channel_layer.group_send)(
							f'user_{el["winner"]}',
							{
								'type': 'notify_user',
								'notification_type': 'tournament',
								'message': f"{tour.name}: New round ready to start",
								'info': tour.name,
							})
					
		if (self.pong_match.winner != None and self.winner == 0):
			if (self.pong_match.winner == self.game.player1.id):
				self.winner = 1
			else:
				self.winner = 2
			self.send(text_data=json.dumps({
				'type':'Pong',
				'event':'endMatch',
				'id': self.winner,
			}))
			return



	def Pong_event(self, event):
		self.send(text_data=json.dumps({
			'type':'Pong',
			'event':'frame',
			'scoring':self.game.scoring,
			'ball':self.game.ballx,
			'bally':self.game.bally,
			'player1':[self.game.player1.x, self.game.player1.y, self.game.player1.score, self.game.player1.controller],
			'player2':[self.game.player2.x, self.game.player2.y, self.game.player2.score, self.game.player2.controller],
			'time':self.game.t
		}))
