import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from .models import Shooter
from .game_class import Game
import math
import time

dictio = {}

class ShooterConsumer(WebsocketConsumer):
	def connect(self):
		self.room_group_name = 'tttt'
		self.user = self.scope['user']

		try:
			self.shooter_room = get_object_or_404(Shooter, group_name=self.room_group_name)
		except:
			self.shooter_room = Shooter.objects.create(
				group_name = self.room_group_name,
			)
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)
		if self.user not in self.shooter_room.users_online.all():
			self.shooter_room.users_online.add(self.user)
		if self.room_group_name not in dictio:
			dictio[self.room_group_name] = Game()
		self.game = dictio[self.room_group_name]
		if (self.user not in self.game.ids):
			self.id = len(self.game.ids) + 1
			self.game.ids[self.user] = self.id
			self.game.players.append(self.game.CreatePlayer(self.id - 1, self.user.skin, self.user.username))
		else:
			self.id = self.game.ids[self.user]
			self.game.players[self.id - 1]["skin"] = self.user.skin

		self.accept()

		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type':'Connected',
				'id':self.id,
				'position':self.game.players[self.id - 1]["spawn"],
				'rotation':self.game.players[self.id - 1]["rotaspawn"],
			}
		)


	def disconnect(self, code):
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)
		if self.user in self.shooter_room.users_online.all():
			self.shooter_room.users_online.remove(self.user)
		if self.shooter_room.users_online.count() == 0:
			if (self.room_group_name in dictio):
				del dictio[self.room_group_name]
			self.shooter_room.delete()


	def receive(self, text_data):
		text_data_json = json.loads(text_data)

		t = self.game.last
		self.game.last = time.perf_counter()
		dt = self.game.last - t

		event = text_data_json['event']
		id = text_data_json['id'] - 1
		if (event == "hit"):
			target = text_data_json['target']
			if self.game.flag.player_id == target + 1:
				self.game.flag.player_id = 0
				async_to_sync(self.channel_layer.group_send)(
					self.room_group_name,
					{
						'type':'Flag',
						'event':'dropped',
						'id':target + 1,
					}
				)
			self.game.players[target]["hit"] = 1
			self.game.players[target]["position"] = self.game.players[target]["spawn"]
			self.game.players[target]["death"] += 1
			self.game.players[id]["score"] += 100
			self.game.players[id]["kill"] += 1
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

		if (self.game.flag.player_id == 0):
			self.game.flag.checkPlayer(self.game.players[id]["position"], id + 1, dt)
			if (self.game.flag.player_id != 0):
				async_to_sync(self.channel_layer.group_send)(
					self.room_group_name,
					{
						'type':'Flag',
						'event':'picked',
						'id':self.game.flag.player_id,
					}
				)
		else:
			self.game.players[self.game.flag.player_id - 1]["score"] += dt * 4
				
			
		self.game.players[id]["direction"] = text_data_json['player'][1]
		self.game.players[id]["controller"] = text_data_json['controller']
		if self.id == id + 1:
			self.Shooter_event(event)

	def Connected(self, event):

		self.send(text_data=json.dumps({
			'type':'Shooter',
			'event':'Connected',
			'players':self.game.players,
			'position': event['position'],
			'rotation': event['rotation'],
			'id': event['id'],
			'flag': self.game.flag.player_id
		}))

	def Flag(self, event):
		self.send(text_data=json.dumps({
			'type':'Shooter',
			'event':'Flag_' + event["event"],
			'id':event['id'],
		}))

	def Shooter_event(self, event):

		self.send(text_data=json.dumps({
			'type':'Shooter',
			'event':event,
			'players':self.game.players,
			'f':[self.game.flag.poss, self.game.flag.player_id]
		}))