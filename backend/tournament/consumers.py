import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from .models import Tournament, PongMatch
from django.utils import timezone
from django.db.models import Q

import sys


class TournamentMatchmakingConsumer(WebsocketConsumer):
	def connect(self):
		self.gamemode = self.scope['url_route']['kwargs']['gamemode']
		self.tournament_name = self.scope['url_route']['kwargs']['tournament_name']
		self.room_group_name = f'tournament_{self.tournament_name}'
		self.user = self.scope['user']

		try:
			self.tournament_room = get_object_or_404(Tournament, name=self.tournament_name)
		except:
			self.disconnect(0)


		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)

		if self.user not in self.tournament_room.participants.all() and self.tournament_room.participants.count() < self.tournament_room.nb_player:
			self.tournament_room.participants.add(self.user)

		if self.user not in self.tournament_room.users_online.all():
			self.tournament_room.users_online.add(self.user)

		self.accept()
		# if self.tournament_room.last_round == None:
		# 	nb_player = self.tournament_room.nb_player
		# else:
		# 	nb_player = self.tournament_room.participants.count()

		capacity = self.tournament_room.capacity

		async_to_sync(self.channel_layer.group_send)(
				self.room_group_name,
				{
					'type': 'Connection',
					'event': 'connection',
					'players': list(self.tournament_room.participants.all().values("username", "id", "profile_picture")),
					'online': list(self.tournament_room.users_online.all().values("username", "id",  "profile_picture")),
					'games': list(self.tournament_room.matchs.all().values("player1", "player2", "score1", "score2", "winner")),
					'capacity': capacity,
				} 
			)
		
	def Connection(self, event):
		self.send(text_data=json.dumps({
			'type': 'Tournament',
			'event': 'Connection',
			'players': event['players'],
			'online': event['online'],
			'games': event['games'],
			'capacity': event['capacity']
		}))
		
	def launch_match(self):
		values = []
		if self.tournament_room.participants.count() == self.tournament_room.nb_player and self.tournament_room.last_round == None:
			qs = self.tournament_room.participants.all()
			values = [item.id for item in qs]

		if self.tournament_room.last_round != None :
			elem = list(self.tournament_room.matchs.filter(match_date__gte=self.tournament_room.last_round).exclude(winner=None).values())
			values = [item["winner"] for item in elem]
			if (len(values) < self.tournament_room.nb_player or self.tournament_room.users_online.filter(Q(id__in=values)).count() != self.tournament_room.nb_player):
				usrs = list(self.tournament_room.users_online.filter(Q(id__in=values)).values())
				ids = [item["id"] for item in usrs]
				for usr in values:
					if usr not in ids:
						async_to_sync(self.channel_layer.group_send)(
							f'user_{usr}',
							{
								'type': 'notify_user',
								'message': f"{self.tournament_room.name}: new round ready to start",
								# 'tournament': tour.name,
							})
				values = []


		if len(values) == self.tournament_room.nb_player:
			self.tournament_room.last_round = timezone.now()
			self.tournament_room.save()
			i = 0
			while (i < self.tournament_room.nb_player):
				if (i % 2 == 1):
					Match = PongMatch.objects.create(
						player1 = values[i - 1],
						player2 = values[i],
						gamemode = self.gamemode,
						type = "tournament",
					)
					self.tournament_room.matchs.add(Match)

				i += 1
			self.tournament_room.nb_player /= 2
			self.tournament_room.save()


			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name,
				{
					'type': 'Starting_matchs',
					'event': 'Match',
				} 
			)


	def disconnect(self, code):
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)
		if not self.tournament_room:
			return
		if self.user in self.tournament_room.users_online.all():
			self.tournament_room.users_online.remove(self.user)
		del self.tournament_room.last_round
		if self.user in self.tournament_room.participants.all() and self.tournament_room.last_round == None:
			self.tournament_room.participants.remove(self.user)
			if (self.tournament_room.participants.count() == 0):
				self.tournament_room.delete()
	
	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		event = text_data_json['event']
		if (event == 'Match_button'):
			self.launch_match()

	def Starting_matchs(self, event):
		
		del self.tournament_room.last_round
		qs = self.tournament_room.matchs.filter(match_date__gte=self.tournament_room.last_round).all()
		values = [{"id":item.id, "player1":item.player1, "player2":item.player2} for item in qs]

		for game in values:
			if self.user.id == game["player1"] or self.user.id == game["player2"]:
				self.send(text_data=json.dumps({
					'type': 'Starting_match',
					'event': 'Match',
					'game_id':game["id"],
					'gamemode': self.gamemode,
				}))

