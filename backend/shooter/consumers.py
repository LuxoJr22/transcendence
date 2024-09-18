import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from .models import Shooter
from .game_class import Game

dictio = {}

class ShooterConsumer(WebsocketConsumer):
	def connect(self):
		self.room_group_name = 't'
		self.user = self.scope['user']
		self.id = 0

		try:
			self.pongroom = get_object_or_404(Shooter, group_name=self.room_group_name)
		except:
			self.pongroom = Shooter.objects.create(
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
			dictio[self.room_group_name] = Game()
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
		if (event == "hit"):
			if text_data_json['id'] == 1:
				self.game.player2.hit = 1
				self.game.player2.position = self.game.player2.spawn
			if text_data_json['id'] == 2:
				self.game.player1.hit = 1
				self.game.player1.position = self.game.player1.spawn
			return 

		if text_data_json['id'] == 1:
			if (self.game.player1.hit != 1):
				self.game.player1.position = text_data_json['player'][0]
			else:
				self.send(text_data=json.dumps({
					'type':'Shooter',
					'event':'hit',
					'position': self.game.player1.position
				}))
				self.game.player1.hit = 0
			self.game.player1.direction = text_data_json['player'][1]
			self.game.player1.controller = text_data_json['controller']
			if self.id == 1:
				self.Shooter_event(event)
		if text_data_json['id'] == 2:
			if (self.game.player2.hit != 1):
				self.game.player2.position = text_data_json['player'][0]
			else:
				self.send(text_data=json.dumps({
					'type':'Shooter',
					'event':'hit',
					'position': self.game.player2.position
				}))
				self.game.player2.hit = 0
			self.game.player2.direction = text_data_json['player'][1]
			self.game.player2.controller = text_data_json['controller']
			self
			if self.id == 2:
				self.Shooter_event(event)

	def Shooter_event(self, event):

		self.send(text_data=json.dumps({
			'type':'Shooter',
			'event':event,
			'player1':[self.game.player1.position, self.game.player1.direction],
			'player2':[self.game.player2.position, self.game.player2.direction],
			'controller1':self.game.player1.controller,
			'controller2':self.game.player2.controller,
		}))