<script lang="ts">
	import {beforeNavigate, goto } from '$app/navigation';
    import { getAccessToken } from '$lib/stores/auth';

	interface Dictionary<T> {
        [Key: string]: T;
    }
	interface Dict<T, C> {
		[Key: string]: T | C;
	}

	let currentUrl : string = window.location.href;
	var tournament_name = currentUrl.substring(currentUrl.lastIndexOf('/') + 1);
	var allUsers : Dictionary<string>[] = []
	var allGames : Dictionary<string>[]  = []
	var allOnline : Dictionary<string>[]  = []
	var Users : string[] = []
	var capacity = 0
	var winners : (string | null)[]  = []

	let url = '/ws/tournament/pong/' + tournament_name + '/?token=' + localStorage.getItem('access_token');
	const chatSocket = new WebSocket(url)


	chatSocket.onmessage = function(e) {
		
		let data = JSON.parse(e.data)
		if (data.event == "Connection")
		{
			allUsers = data.players;
			allGames = data.games;
			allOnline = data.online;
			capacity = data.capacity;
			data.players.forEach((element : Dict<number, string>) => {
				if (typeof element.id == "number" && typeof element.username == "string")
					Users[element.id] = element.username
			});
			document.getElementById("bracket")?.replaceChildren(create_bracket(capacity, allGames, allUsers))
		}
		if (data.event == "Match")
		{
			localStorage.setItem('game_id', data.game_id);
			goto('/matchmaking/pong/private');
		}
	}

	chatSocket.onclose = function(e) {
		if (e.code != 1000)
			goto('/tournament');
	}


	function start_match() {
		chatSocket.send(JSON.stringify({
			'event':'Match_button',
			'winners':winners,
		}))
	}

	function create_match(position : string, name : number | null | string, score : number | null)
	{
		var match = document.createElement("div");
		match.className = `match-${position} team`;
		var name_span = document.createElement("span");
		name_span.className = "name"
		if (typeof name == "number" && Users[name])
			name_span.textContent = Users[name]
		else if (typeof name == "string" || name == null)
			name_span.textContent = name
		match.appendChild(name_span)
		var score_span = document.createElement("span");
		score_span.className = "score"
		if (score)
			score_span.textContent = `${score}`
		match.appendChild(score_span)
		return (match)
	}

	function create_versus(game : Dict<string | null, number>)
	{
		if (game && (typeof game.score1 == "number" || game.score1 == null) && (typeof game.score2 == "number" || game.score2 == null))
		{
			var match1 = create_match("top", game.player1, game.score1)
			var match2 = create_match("bottom", game.player2, game.score2)
		}
		else
		{
			var match1 = create_match("top", null, null)
			var match2 = create_match("bottom", null, null)
		}
		var versus = document.createElement("div");
		
		var winner;
		if (game && game.winner == game.player1)
			winner = "winner-top"
		else if (game && game.winner == game.player2)
			winner = "winner-bottom"
		else
			winner = ""
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

	function create_column(i : number, allgames  : Dictionary<string | null>[], act_game : number)
	{
		var column = document.createElement("div");
		column.className = "column";
		var total = i
		while (i > 0)
		{
			column.appendChild(create_versus(allgames[act_game + (total - i)]))
			i --
		}
		return (column)
	}

	function create_bracket(capacity : number, allgames : Dictionary<string | null>[], allusers :  Dictionary<string>[])
	{
		winners = []
		var bracket = document.createElement("div");
		var act_game = 0
		bracket.className = "bracket";
		capacity /= 2
		var i = 0
		if (allgames.length == 0)
		{
			while (allusers[i])
			{
				winners.push(allusers[i].id)
				if (i % 2 == 1)
				{
					allgames.push({player1:allusers[i - 1].username, player2:allusers[i].username, score1:null, score2:null})
				}
				i ++
			}
		}
		else if (capacity >= 1)
		{
			let start = allgames.length - capacity;
			
			while (allgames[start])
			{
				winners.push(allgames[start].winner)
				start ++;
			}
			let i = 0
			while (winners[i])
			{
				if (i % 2 == 1)
					allgames.push({player1:winners[i - 1], player2:winners[i], score1:null, score2:null})
				i ++
			}
		}
		while (capacity >= 1)
		{
			bracket.appendChild(create_column(capacity, allgames, act_game))
			act_game += capacity;
			capacity /= 2;
		}
		return( bracket)
	}

	beforeNavigate(() => {
		if (chatSocket)
			chatSocket.close()
	})
		

</script>


<div class="container">
    <div class="row mt-5">
		
		<h4 class="mt-2 d-flex justify-content-center"style="color:white;">{tournament_name}</h4>
		<div class="theme theme-dark" id="bracket"></div>
		<div class="d-flex justify-content-center">
            <button on:click={start_match} class="btn btn-primary mb-3" type="button"><p class="mb-1">Launch Tournament</p></button>
        </div>
		<div class="d-flex justify-content-center row position-relative">
			<p class="text-light text-center text-decoration-underline h5">Players:</p>
            {#each allUsers as user}
                <div class="">
					{#if allOnline.some(actuser => actuser.id == user.id)}
						<div class="d-flex text-light rounded position-relative" style="left:45%;">
							<img alt="profile_picture" src={"/media/" + user.profile_picture} width=3% height=auto class="rounded-circle" style="object-fit:cover; aspect-ratio:1">
							<p class="m-0 p-0 mt-1 ms-2">{user.username}</p>
						</div>
					{:else}
						<div class="d-flex rounded position-relative " style="color:grey; left:45%;">
							<img alt="profile_picture" src={"/media/" + user.profile_picture} width=3% height=auto class="rounded-circle" style="object-fit:cover; aspect-ratio:1">
							<p class="m-0 p-0 mt-1 ms-2">{user.username}</p>
						</div>
					{/if}
                </div>
            {/each}
            {#if !allUsers[0]}
                <p class="d-flex justify-content-center mt-3" style="color:grey;">Empty players list</p>
            {/if}
        </div>
    </div>
</div>



<style>
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

