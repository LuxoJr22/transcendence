<script lang="ts">
    import { onMount } from "svelte";

	let currentUrl : string = window.location.href;
	var gamemode = currentUrl.substring(currentUrl.lastIndexOf('/') + 1);
	var allUsers = []
	var allGames = []
	var nb_players = 0

	let url = 'ws://localhost:8000/ws/tournament/pong/' + gamemode + '/?token=' + localStorage.getItem('access_token');
	const chatSocket = new WebSocket(url)


	chatSocket.onmessage = function(e) {
	
		let data = JSON.parse(e.data)
		if (data.event == "Connection")
		{
			allUsers = data.players;
			allGames = data.games;
			nb_players = data.nb_players;
			console.log(data)
			document.getElementById("bracket").replaceChildren(create_bracket(nb_players))
		}
		if (data.event == "Match")
		{
			localStorage.setItem('game_id', data.game_id);
			window.location.href = '/matchmaking/pong/private';
		}
	}

	chatSocket.onclose = function(e) {
			window.location.href = '/tournament';
		}


	function start_match() {
		chatSocket.send(JSON.stringify({
				'event':'Match_button',
			}))
	}
	//onMount(async () => {

		function create_match(position : string)
		{
			var match = document.createElement("div");
			match.className = `match-${position} team`;
			return (match)
		}

		function create_versus(winner : string)
		{
			var match1 = create_match("top")
			var match2 = create_match("bottom")
			var versus = document.createElement("div");
			versus.className = `match ${winner}`
			versus.appendChild(match1)
			versus.appendChild(match2)

			var matchlines = document.createElement("div");
			matchlines.className = 'match-lines'
			var lineone =  document.createElement("div");
			lineone.className = "line one"
			var linetwo =  document.createElement("div");
			linetwo.className = "line two"
			matchlines.appendChild(lineone)
			matchlines.appendChild(linetwo)
			versus.appendChild(matchlines)

			var matchlinesv = document.createElement("div");
			matchlinesv.className = 'match-lines alt'
			var linev = document.createElement("div");
			linev.className = "line one"
			matchlinesv.appendChild(linev)
			versus.appendChild(matchlinesv)

			return (versus)
		}

		function create_column(i : number)
		{
			var column = document.createElement("div");
			column.className = "column";
			while (i > 0)
			{
				column.appendChild(create_versus(""))
				i --
			}
			return (column)
		}

		function create_bracket(nb_player : number)
		{
			var bracket = document.createElement("div");
			bracket.className = "bracket";
			nb_player /= 2
			while (nb_player >= 1)
			{
				bracket.appendChild(create_column(nb_player))
				nb_player /= 2;
			}
			return( bracket)
		}
		

</script>


<div class="container">
    <div class="row mt-5">
		<div class="d-flex justify-content-center border-bottom">
            <button on:click={start_match} class="btn btn-primary mb-3" type="button"><p class="mb-1">Launch Tournament</p></button>
        </div>
		<p class="mt-2"style="color:white;">{gamemode}</p>
		<div class="modal-body d-flex justify-content-center row user-container m-0 me-2 mb-2">
            {#each allUsers as user}
                <div class="row p-0 m-2">
                    <div class="btn text-light border rounded" aria-label="Close">
                        <p class="d-inline">{user.username}</p>
                    </div>
                </div>
            {/each}
            {#if !allUsers[0]}
                <p class="d-flex justify-content-center mt-3" style="color:grey;">Empty players list</p>
            {/if}
        </div>
    </div>
</div>
<div class="theme theme-dark" id="bracket">
	<!-- <div class="bracket disable-image"> -->
	  <!-- <div class="column">
		<div class="match winner-top">
		  <div class="match-top team">
			<span class="image"></span>
			<span class="name">Orlando Jetsetters</span>
			<span class="score">2</span>
		  </div>
		</div>
	</div> -->
		<!--  <div class="match-bottom team">
			<span class="image"></span>
			<span class="name">D.C. Senators</span>
			<span class="score">1</span>
		  </div>
		  <div class="match-lines">
			<div class="line one"></div>
			<div class="line two"></div>
		  </div>
		  <div class="match-lines alt">
			<div class="line one"></div>
		  </div>
		</div>
		<div class="match winner-bottom">
		  <div class="match-top team">
			<span class="image"></span>
			<span class="name">New Orleans Rockstars</span>
			<span class="score">1</span>
		  </div>
		  <div class="match-bottom team">
			<span class="image"></span>
			<span class="name">West Virginia Runners</span>
			<span class="score">2</span>
		  </div>
		  <div class="match-lines">
			<div class="line one"></div>
			<div class="line two"></div>
		  </div>
		  <div class="match-lines alt">
			<div class="line one"></div>
		  </div>
		</div>
	  </div>
	  <div class="column">
		<div class="match winner-bottom">
		  <div class="match-top team">
			<span class="image"></span>
			<span class="name">Orlando Jetsetters</span>
			<span class="score">1</span>
		  </div>
		  <div class="match-bottom team">
			<span class="image"></span>
			<span class="name">West Virginia Runners</span>
			<span class="score">2</span>
		  </div>
		  <div class="match-lines">
			<div class="line one"></div>
			<div class="line two"></div>
		  </div>
		  <div class="match-lines alt">
			<div class="line one"></div>
		  </div>
		</div>
	  </div>  -->
	<!-- </div> -->
  </div>


<style>
	/* .theme {
		height: 100%;
		width: 100%;
		position: absolute;
	} */
	:global(.bracket) {
		padding: 40px;
		margin: 5px;
	}
	:global(.bracket) {
		display: flex;
		flex-direction: row;
		position: relative;
	}
	:global(.column) {
		display: flex;
		flex-direction: column;
		min-height: 100%;
		justify-content: space-around;
		align-content: center;
	}
	:global(.match) {
		position: relative;
		display: flex;
		flex-direction: column;
		min-width: 240px;
		max-width: 240px;
		height: 62px;
		margin: 12px 24px 12px 0;
	}
	:global(.match .team) {
		display: flex;
		align-items: center;
		width: 100%;
		height: 100%;
		border: 1px solid black;
		position: relative;
	}
	:global(.match .team span) {
		padding-left: 8px;
	}
	:global(.match .team span:last-child) {
		padding-right: 8px;
	}
	:global(.match .team .score) {
		font-size: 14px;
		margin-left: auto;
	}
	:global(.match .team:first-child) {
		margin-bottom: -1px;
	}
	:global(.match-lines) {
		display: block;
		position: absolute;
		top: 50%;
		bottom: 0;
		margin-top: 0px;
		right: -1px;
	}
	:global(.match-lines .line) {
		background: #36404e;
		position: absolute;
	}
	:global(.match-lines .line.one) {
		height: 1px;
		width: 12px;
	}
	:global(.match-lines .line.two) {
		height: 44px;
		width: 1px;
		left: 11px;
	}
	:global(.match-lines.alt) {
		left: -12px;
	}
	:global(.match:nth-child(even) .match-lines .line.two) {
		transform: translate(0, -100%);
	}
	:global(.column:first-child .match-lines.alt) {
		display: none;
	}
	:global(.column:last-child .match-lines) {
		display: none;
	}
	:global(.column:last-child .match-lines.alt) {
		display: block;
	}
	:global(.column:nth-child(2) .match-lines .line.two) {
		height: 88px;
	}
	:global(.column:nth-child(3) .match-lines .line.two) {
	  height: 175px;
	}
	.disable-image .image {
		display: none !important;
	}
	:global(.theme-dark .team) {
		background: #182026;
		border-color: #232c36;
		color: #6b798c;
	}
	:global(.theme-dark .winner-top .match-top,
	.theme-dark .winner-bottom .match-bottom) {
		background: #232c36;
		color: #e3e8ef;
		border-color: #36404e;
		z-index: 1;
	}
	:global(.theme-dark .winner-top .match-top .score,
	.theme-dark .winner-bottom .match-bottom .score) {
		color: #03d9ce;
	}

</style>

