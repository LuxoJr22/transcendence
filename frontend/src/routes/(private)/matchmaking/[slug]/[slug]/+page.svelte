<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { auth, fetchUser, getAccessToken } from '$lib/stores/auth';
	import type { AuthState } from '$lib/stores/auth';
	import Waiting from '$lib/components/Matchmaking/Waiting.svelte';
	import { goto } from '$app/navigation'

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
		const token = await getAccessToken();
		if (token)
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
					goto('/' + gamemode + '/');
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
					localStorage.setItem('room_name', room_name);
					ws.close();
					goto('/' + gamemode + '/');
				}
			}
		}
		else
			goto('/');
	});

	onDestroy(() => {
		if (ws)
			ws.close();
	});

</script>

<div class="d-flex justify-content-center">
	<Waiting />
</div>
<div class="container-fluid d-flex justify-content-center title">
	<p style="color: white">WAITING FOR OPONENT</p>
</div>

<style>
	.title {
		font-family: 'Luckiest Guy';
		font-size: 300%;
	}
</style>