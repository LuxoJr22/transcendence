<script lang="ts">
	import Settings from "$lib/static/Profile/Settings.svelte";
	import { auth, fetchUser, type AuthState } from "$lib/stores/auth";
	import { onMount } from "svelte";
	const img = new URL('$lib/assets/pong.png', import.meta.url).href
	const img1 = new URL('$lib/assets/game2.png', import.meta.url).href

	let linkGame = "/matchmaking/pong/public";
	let state: AuthState;
		state = $auth;

	onMount(() => {
		auth.subscribe((value : AuthState) =>{
			state = value;
		});
	})

	function changeLink() {
		if (linkGame == "/matchmaking/pong/public")
			linkGame = "/shooter"
		else
			linkGame = "/matchmaking/pong/public"
	}

</script>

<div class="container-fluid my-5" style="width:95vw; height:85vh;">
	<div class="row">
		<div class="d-flex justify-content-start align-items-start col-xl-6 col-12">
			<div id="carouselExample" class="carousel slide container-game">
				<div class="carousel-inner">
					<div class="carousel-item active">
						<img src={img} class="d-block" alt="">
					</div>
					<div class="carousel-item">
						<img src={img1} class="d-block" alt="">
					</div>
				</div>
				<button on:click={changeLink} class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
					<span class="carousel-control-prev-icon" aria-hidden="true"></span>
					<span class="visually-hidden">Previous</span>
				</button>
				<button on:click={changeLink} 
				class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
					<span class="carousel-control-next-icon" aria-hidden="true"></span>
					<span class="visually-hidden">Next</span>
				</button>
			</div>
		</div>
		<div class="container d-flex align-items-center justify-content-center col-xl-6 col-12">
			<div class="ms-5 ps-2">
				<div class="row mb-3">
					<div class="card mycard mx-3 bg-warning-subtle">
						<div class="card-body">
							<h5 class="card-title">Online Mode</h5>
							<p class="card-text">Play online against other players.</p>
							<a href={linkGame} class="btn btn-dark">Play</a>
						</div>
					</div>
					<div class="card mycard bg-warning-subtle">
						<div class="card-body">
							<h5 class="card-title">Tournament</h5>
							<p class="card-text">Compete in tournaments and prove your skills.</p>
							<a href="/tournament" class="btn btn-dark">Create or Join</a>
						</div>
					</div>
				</div>
				<div class="row">
					<div class="card mycard bg-warning-subtle mx-3">
						<div class="card-body">
							<h5 class="card-title">Chat</h5>
							<p class="card-text">Chatting with other people.</p>
							<a href="/chat/home" class="btn btn-dark">Here we go</a>
						</div>
					</div>
					<div class="card mycard bg-warning-subtle">
						<div class="card-body">
							<h5 class="card-title">Character Customization</h5>
							<p class="card-text">Choose you character !</p>
							<a href="/selection" class="btn btn-dark">Go</a>
						</div>
					</div>
				</div>
			</div>
		</div>
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
</style>
