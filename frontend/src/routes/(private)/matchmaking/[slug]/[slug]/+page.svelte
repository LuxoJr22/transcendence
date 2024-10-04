<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { auth, fetchUser } from '$lib/stores/auth';
	import type { AuthState } from '$lib/stores/auth';

	let state: AuthState;
	$: $auth, state = $auth;
	var ws: WebSocket;

	let currentUrl : string = window.location.href;
	//let gamemode = currentUrl.substring(currentUrl.lastIndexOf('/') + 1);
	let ur = currentUrl.split('/')
	let index = ur.indexOf("matchmaking")
	var gamemode = ur[index + 1];
	var type = ur[index + 2]

	onMount(async () => {
		
		if (localStorage.getItem('access_token'))
			await fetchUser();
		if (state.isAuthenticated && (gamemode == 'pong' || gamemode == 'pong_retro') && type == "public") {
			ws = new WebSocket('/ws/pong_matchmaking/' + gamemode + '/?token=' + state.accessToken);
			ws.onmessage = (event) => {
				let data = JSON.parse(event.data);
				if (data.event == 'Match' && state.user?.id == data.player1_id || state.user?.id == data.player2_id) {
					let gamemode = data.gamemode;
					let room_name = data.room_name;
					ws.close();
					localStorage.setItem('room_name', room_name);
					localStorage.setItem('game_id', data.match_id);
					window.location.href = '/' + gamemode;
				}
				if (data.event == 'Research')
				{
					ws.send(JSON.stringify({
						'event':'Research',
					}))
				}
			}
		}
		else if (state.isAuthenticated && (gamemode == 'pong' || gamemode == 'pong_retro') && type == "private") {
			var game_id = localStorage.getItem('game_id')
			ws = new WebSocket('/ws/pong_private_matchmaking/' + gamemode + '/' + game_id + '/?token=' + state.accessToken);
			ws.onmessage = (event) => {
				let data = JSON.parse(event.data);
				if (data.event == 'Match' && state.user?.id == data.player1_id || state.user?.id == data.player2_id) {
					let gamemode = data.gamemode;
					let room_name = data.room_name;
					ws.close();
					localStorage.setItem('room_name', room_name);
					localStorage.setItem('game_id', data.match_id);
					window.location.href = '/' + gamemode;
				}
			}
		}
		else
			window.location.href = '/';
	});

	onDestroy(() => {
		if (ws)
			ws.close();
	});

</script>

<div class="container-fluid">
	<p style="color: white">WAITING FOR OPONENT</p>
</div>