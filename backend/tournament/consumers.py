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

		self.accept()
		if self.tournament_room.last_round == None:
			nb_player = self.tournament_room.nb_player
		else:
			nb_player = self.tournament_room.participants.count()

		async_to_sync(self.channel_layer.group_send)(
				self.room_group_name,
				{
					'type': 'Connection',
					'event': 'connection',
					'players': list(self.tournament_room.participants.all().values("username")),
					'games': list(self.tournament_room.matchs.all().values("player1", "player2", "score1", "score2", "winner")),
					'nb_players': nb_player,
				} 
			)
		
	def Connection(self, event):
		self.send(text_data=json.dumps({
			'type': 'Tournament',
			'event': 'Connection',
			'players': event['players'],
			'games': event['games'],
			'nb_players': event['nb_players']
		}))
		
	def launch_match(self):
		values = []
		if self.tournament_room.participants.count() == self.tournament_room.nb_player and self.tournament_room.last_round == None:
			qs = self.tournament_room.participants.all()
			values = [item.id for item in qs]

		if self.tournament_room.last_round != None :
			elem = list(self.tournament_room.matchs.filter(match_date__gte=self.tournament_room.last_round).exclude(winner=None).values())
			values = [item["winner"] for item in elem]
			if (len(values) < self.tournament_room.nb_player or self.tournament_room.participants.filter(Q(id=values[0]) | Q(id=values[1])).count() != self.tournament_room.nb_player):
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
		# if self.user in self.tournament_room.participants.all() and self.tournament_room.last_round == None:
		# 	print("dico", file=sys.stderr)
		# 	self.tournament_room.participants.remove(self.user)
	
	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		event = text_data_json['event']
		if (event == 'Match_button'):
			self.launch_match()

	def Starting_matchs(self, event):
		qs = self.tournament_room.matchs.all()
		values = [{"id":item.id, "player1":item.player1, "player2":item.player2} for item in qs]

		for game in values:
			if self.user.id == game["player1"] or self.user.id == game["player2"]:
				print(game["id"], file=sys.stderr)
				self.send(text_data=json.dumps({
					'type': 'Starting_match',
					'event': 'Match',
					'game_id':game["id"],
					'gamemode': self.gamemode,
				}))

