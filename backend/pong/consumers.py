import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from .models import PongGroup, PongMatchmaking, PongMatch
from .game_class import Game

dictio = {}

class MatchmakingConsumer(WebsocketConsumer):
	def connect(self):
		self.gamemode = self.scope['url_route']['kwargs']['gamemode']
		self.room_group_name = f'{self.gamemode}_matchmaking'
		self.user = self.scope['user']

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
		
		if self.matchmaking_room.users_online.count() >= 2:
			qs = self.matchmaking_room.users_online.all()
			values = [item.id for item in qs]

			self.player1 = values[0]
			self.player2 = values[1]

			self.pongmatch = PongMatch.objects.create(
				player1 = self.player1,
				player2 = self.player2,
			)
			dictio[f'{self.gamemode}_{self.player1}_{self.player2}'] = Game(self.gamemode, self.pongmatch.id)

			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name,
				{
					'type': 'Pong_match',
					'event': 'Match',
					'player1_id': self.player1,
					'player2_id': self.player2,
				} 
			)

	def disconnect(self, code):
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)
		if self.user in self.matchmaking_room.users_online.all():
			self.matchmaking_room.users_online.remove(self.user)

	def Pong_match(self, event):
		self.send(text_data=json.dumps({
			'type': 'Pong_match',
			'event': 'Match',
			'player1_id': event['player1_id'],
			'player2_id': event['player2_id'],
			'gamemode': self.gamemode,
			'room_name': f'{self.gamemode}_{event["player1_id"]}_{event["player2_id"]}'
		}))


class PongConsumer(WebsocketConsumer):
	def connect(self):
		self.gamemode = self.scope['url_route']['kwargs']['gamemode']
		self.room_group_name = self.scope['url_route']['kwargs']['room_name']
		self.user = self.scope['user']
		self.id = 0

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
		
		if self.user not in self.pongroom.users_online.all():
			self.pongroom.users_online.add(self.user)
		if self.pongroom.users_online.count() == 1:
			self.id = 1
		else:
			self.id = 2
		if (self.room_group_name not in dictio):
			self.disconnect()
		self.game = dictio[self.room_group_name]
		self.accept()
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
		if self.user in self.pongroom.users_online.all():
			self.pongroom.users_online.remove(self.user)
		if self.pongroom.users_online.count() == 0:
			del dictio[self.room_group_name]
			self.pongroom.delete()

	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		event = text_data_json['event']
		if 'player1' in text_data_json:
			self.game.player1.controller = text_data_json['player1']
			if self.id == 1:
				self.Pong_event(event)
		if 'player2' in text_data_json:
			self.game.player2.controller = text_data_json['player2']
			if self.id == 2:
				self.Pong_event(event)
		self.game.update()


	def Pong_event(self, event):
		self.send(text_data=json.dumps({
			'type':'Pong',
			'event':event,
			'scoring':self.game.scoring,
			'ball':self.game.ballx,
			'bally':self.game.bally,
			'player1':[self.game.player1.x, self.game.player1.y, self.game.player1.score, self.game.player1.controller],
			'player2':[self.game.player2.x, self.game.player2.y, self.game.player2.score, self.game.player2.controller],
			'time':self.game.t
		}))
