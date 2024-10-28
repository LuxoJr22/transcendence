import json, operator, time, sys
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from .models import Shooter, ShooterMatch, PlayerScore
from users.models import User
from .game_class import Game

dictio = {}

WAITING = 0
LAUNCHING = 1
LAUNCHED = 2 
FINISHED = 3
QUIT = 4


class ShooterConsumer(WebsocketConsumer):
	def connect(self):
		self.room_group_name = self.scope['url_route']['kwargs']['room_name']
		self.user = self.scope['user']
		self.in_game = 0

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
		self.accept()
		try:
			self.shootermatch = get_object_or_404(ShooterMatch, room_name=self.room_group_name)
		except:
			return self.close(3000, "Match don't exist")		
		if self.user not in self.shooter_room.users_online.all():
			self.shooter_room.users_online.add(self.user)
		else:
			print("oui", file=sys.stderr)
			return self.close(3000, "Already in match")
		if self.room_group_name not in dictio:
			dictio[self.room_group_name] = Game()
		self.game = dictio[self.room_group_name]
		if (self.user not in self.game.ids):
			self.id = len(self.game.ids) + 1
			self.game.ids[self.user] = self.id
			self.game.players.append(self.game.CreatePlayer(self.id - 1, self.user.id , self.user.skin, self.user.username))
		else:
			self.id = self.game.ids[self.user]
			self.game.players[self.id - 1]["skin"] = self.user.skin

		self.in_game = 1
		

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
		if self.user in self.shooter_room.users_online.all() and self.in_game == 1:
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
		if (len(self.game.players) >= 4 and self.game.game_state == WAITING):
			self.game.game_state = LAUNCHING
			self.game.timer = 6
		if (self.game.game_state == LAUNCHING and self.game.timer <= 0):
			self.game.timer = 480
			self.game.game_state = LAUNCHED
			for players in self.game.players:
				players["score"] = 0
				players["hit"] = 1
				players["position"] = players["spawn"]
				players["death"] = 0
				players["kill"] = 0
		if (self.game.game_state == LAUNCHED and self.game.timer <= 0):
			self.game.game_state = FINISHED
		for player in self.game.players:
			if player["score"] >= 1000 and self.game.game_state == LAUNCHED:
				self.game.game_state = FINISHED
		if self.game.game_state == WAITING:
			self.game.timer += dt 
		else:
			self.game.timer -= dt
		if (self.game.game_state == FINISHED and self.shootermatch.winner == None):
			newlist = sorted(self.game.players, key=operator.itemgetter('score', 'kill', 'death', 'id', 'username'), reverse=True)
			self.shootermatch.winner = newlist[0]['id']
			gain = 10
			for play in newlist:
				self.shootermatch.scores.add(PlayerScore.objects.create(player_id=play["id"], score=play["score"]))
				usr = User.objects.filter(id=play["id"]).all().first()
				usr.shooter_elo += gain
				gain -= 5
				usr.save()
			self.shootermatch.save()
			self.game.game_state = QUIT
			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name,
				{
					'type':'Quit',
					'event':'Quit',
					'username':newlist[0]['username']
				}
			)

		event = text_data_json['event']
		id = text_data_json['id'] - 1

		if (self.game.players[id]["position"]['y'] <= -30):
			self.game.players[id]["hit"] = 1
			self.game.players[id]["position"] = self.game.players[id]["spawn"]
			self.game.players[id]["death"] += 1
		if (event == "hit"):
			target = text_data_json['target']
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
			if self.game.flag.player_id == id + 1:
				self.game.flag.player_id = 0
				async_to_sync(self.channel_layer.group_send)(
					self.room_group_name,
					{
						'type':'Flag',
						'event':'dropped',
						'id':id + 1,
					}
				)
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
		if self.id == id + 1 and event == "frame" and self.game.game_state != QUIT:
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

	def Quit(self, event):
		self.send(text_data=json.dumps({
			'type':'Shooter',
			'event':'Quit',
			'username':event['username']
		}))

	def Shooter_event(self, event):

		self.send(text_data=json.dumps({
			'type':'Shooter',
			'event':event,
			'players':self.game.players,
			'timer': self.game.timer,
			'f':[self.game.flag.poss, self.game.flag.player_id]
		}))
