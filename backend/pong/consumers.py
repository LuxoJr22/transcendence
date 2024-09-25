import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from .models import PongGroup
from .game_class import Game

dictio = {}

class PongConsumer(WebsocketConsumer):
	def connect(self):
		self.room_group_name = 'tests'
		self.gamemode = self.scope['url_route']['kwargs']['gamemode']
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
			dictio[self.room_group_name] = Game(self.gamemode)
		else:
			self.id = 2
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