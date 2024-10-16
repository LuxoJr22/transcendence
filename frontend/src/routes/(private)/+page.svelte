<script lang="ts">
	import { auth, type AuthState } from "$lib/stores/auth";
	import { onMount } from "svelte";
	import { goto } from '$app/navigation';
	const img = new URL('$lib/assets/Super-Pong.png', import.meta.url).href
	const img1 = new URL('$lib/assets/Pong-Retro.png', import.meta.url).href

	let linkGame = '';
	let state: AuthState;
		state = $auth;

	onMount(() => {
		auth.subscribe((value : AuthState) =>{
			state = value;
		});
	})

	function gameHref() {
		let games : NodeListOf<HTMLInputElement> = document.getElementsByName('gameRadio');
		let tmp = null;
		for (let game of games){
			if (game.checked){
				goto((game.id == "shooter" ? '/shooter' : "/matchmaking/" + game.id + "/public/"));
				break ;
			}
		}
	}

</script>

<div class="container-fluid py-5" style="width:95vw; height:85vh;">
	<div class="row mt-5">
		<div class="col-4">
			<label class="form-check-label" for="pong">
			<input class="form-check-input d-none" type="radio" name="gameRadio" id="pong" checked>
				<div class="card m-4 bg-light" style="width: 90%;">
					<img src={img} class="card-img-top p-3" alt="pong" draggable="false">
				</div>
			</label>
		</div>
		<div class="col-4">
			<label class="form-check-label" for="pong_retro">
			<input class="form-check-input d-none" type="radio" name="gameRadio" id="pong_retro">
				<div class="card m-4 bg-black" style="width: 90%;">
					<img src={img1} class="card-img-top p-3" alt="pong" draggable="false">
				</div>
			</label>
		</div>
		<div class="col-4">
			<label class="form-check-label" for="shooter">
			<input class="form-check-input d-none" type="radio" name="gameRadio" id="shooter">
				<div class="card m-4 bg-light" style="width: 90%;">
					<img src={img} class="card-img-top p-3" alt="pong" draggable="false">
				</div>
			</label>
		</div>
	</div>
	<div class="d-flex m-auto align-items-center btn-group-vertical py-5" style="width:15%;">
		<button  class="btn btn-success btn-lg border mb-1 px-5 py-3 title text-truncate" on:click={gameHref}>PLAY</button>
		<a href="/tournament" class="btn btn-light btn-lg border  mb-1 px-5 py-3 subtitle text-truncate">Tournament</a>
		<a href="/selection" class="btn btn-light btn-lg border mb-1 px-5 py-3 subtitle text-truncate">Character</a>
	</div>
</div>

<style>
	.container-game {
		width: 100%;
		display: flex;
	}

	.container-game img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.mycard {
		width: 42%;
	}

	.play-button {
		font-weight: 800;
		font-size: 200%;
	}

	.title {
		font-weight: 800;
		font-size: 170%;
	}

	.subtitle {
		font-weight: 700;
		font-size: 120%;;
	}

	.form-check-input:checked+.card {
		border: solid 5px var(--bs-primary);
		transform: scale(1.1);
	}

	.card:hover {
		cursor: pointer;
		transform: scale(1.1);
		/* animation-name: rotate;
		animation-duration: 1s;
		animation-iteration-count: infinite;
		animation-delay: 0s; */
	}

	/* @keyframes rotate {

		0% {
			transform: rotateZ(0deg);
		}

		100%
		 {
			transform: rotateZ(360deg);
		}
	} */

</style>
