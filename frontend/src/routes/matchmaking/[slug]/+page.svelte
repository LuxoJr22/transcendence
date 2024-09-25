<script lang="ts">
	import { onMount } from 'svelte';
	import { auth, fetchUser } from '../../../stores/auth';
	import type { AuthState } from '../../../stores/auth';

	let state: AuthState;
	$: $auth, state = $auth;
	var ws: WebSocket;

	let currentUrl : string = window.location.href;
	let gamemode = currentUrl.substring(currentUrl.lastIndexOf('/') + 1);

	onMount(async () => {
		console.log(gamemode);
		if (localStorage.getItem('access_token'))
			await fetchUser();
		if (state.isAuthenticated && (gamemode == 'pong' || gamemode == 'pong_retro')) { //state.isAuthenticated && 
			ws = new WebSocket('/ws/pong_matchmaking/' + gamemode + '/?token=' + state.accessToken);
			ws.onmessage = (event) => {
				let data = JSON.parse(event.data);
				if (data.event == 'Match' && state.user?.id == data.player1_id || state.user?.id == data.player2_id) {
					let gamemode = data.gamemode;
					let room_name = data.room_name;
					ws.close();
					localStorage.setItem('room_name', room_name);
					window.location.href = '/' + gamemode;
				}
			}
		}
		else
			window.location.href = '/';
	});

</script>

<div class="container-fluid">
	<p style="color: white">WAITING FOR OPONENT</p>
</div>