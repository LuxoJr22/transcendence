import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from .models import Shooter
from .game_class import Game
import math

dictio = {}

class ShooterConsumer(WebsocketConsumer):
	def connect(self):
		self.room_group_name = 's'
		self.user = self.scope['user']

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
		if self.room_group_name not in dictio:
			dictio[self.room_group_name] = Game()
		self.game = dictio[self.room_group_name]
		if (self.user not in self.game.ids):
			self.id = len(self.game.ids) + 1
			self.game.ids[self.user] = self.id
			self.game.players.append(self.game.CreatePlayer(27, 3, 34, {'x': 104, 'y':1, 'z':0}, {'x':0, 'y':math.pi / 2, 'z':0}, self.user.skin))
		else:
			self.id = self.game.ids[self.user]
			self.game.players[self.id - 1]["skin"] = self.user.skin

		self.accept()

		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type':'Connected',
				'id':self.id,
			}
		)


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
		id = text_data_json['id'] - 1
		if (event == "hit"):
			target = text_data_json['target']
			self.game.players[target]["hit"] = 1
			self.game.players[target]["position"] = self.game.players[target]["spawn"]
			self.game.players[id]["score"] += 100
			return 
		
		if (self.game.players[id]["hit"] != 1):
			self.game.players[id]["position"] = text_data_json['player'][0]
		else:
			self.send(text_data=json.dumps({
				'type':'Shooter',
				'event':'hit',
				'position': self.game.players[id]["position"],
				'rotation': self.game.players[id]["rotaspawn"]
			}))
			self.game.players[id]["hit"] = 0
		self.game.players[id]["direction"] = text_data_json['player'][1]
		self.game.players[id]["controller"] = text_data_json['controller']
		if self.id == id + 1:
			self.Shooter_event(event)

	def Connected(self, event):

		self.send(text_data=json.dumps({
			'type':'Shooter',
			'event':'Connected',
			'players':self.game.players,
			'id': event['id']
		}))

	def Shooter_event(self, event):

		self.send(text_data=json.dumps({
			'type':'Shooter',
			'event':event,
			'players':self.game.players,
		}))