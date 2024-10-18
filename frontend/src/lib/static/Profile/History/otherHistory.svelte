<script lang="ts">
    import { userData, type Profile } from "$lib/stores/user";
    import { onMount } from "svelte";


    interface User {
        id: number,
        username: string,
        score: number,
        profile_picture_url: string
    }

    interface Game {
        me: User,
        opponent: User,
        gamemode: String,
        type: String,
        winner: Number,
        date: String,
        hours: String,
        players: any[],
    }

    let gamesHistory = new Array<Game>();
    export let data : any;
    export let user : Profile;

    onMount(async () => {
        gamesHistory = await parseHistoryMatches(data);
    })

    async function parseHistoryMatches(data : any[]){
        for (let i = 0; data[i] ; i ++)
        {
            if (data[i].gamemode)
                await ParsePongGame(data[i])
            else
                await ParseShooterGame(data[i])
        }
        return (gamesHistory)
    }

    async function ParsePongGame(data : any) {
        let player1 : any = await userData(data.player1 == user.id ? data.player1 : data.player2);
        let player2 : any = await userData(data.player1 != user.id ? data.player1 : data.player2);
        let scoreMe = 0;
        let scoreOpponent = 0;
        if (data.player1 == user.id){
            scoreMe = data.score1;
            scoreOpponent = data.score2;
        }
        else {
            scoreMe = data.score2;
            scoreOpponent = data.score1;
        }
        let game = {
            me: {
                id: player1.id,
                username: player1.username,
                score: scoreMe,
                profile_picture_url : player1.profile_picture_url
            },
            opponent: {
                id: player2.id,
                username: player2.username,
                score: scoreOpponent,
                profile_picture_url : player2.profile_picture_url
            },
            gamemode: data.gamemode,
            type: data.type,
            winner: data.winner,
            date: data.match_date.substring(0, 10),
            hours: data.match_date.substring(11, 16),
            players: []
        }
        gamesHistory.push(game);
    }

    async function ParseShooterGame(data : any) {
        let player1 : any = await userData(data.players[0] == user.id ? data.players[0] : data.players[2]);
        let player2 : any = await userData(data.players[0] != user.id ? data.players[0] : data.players[2]);
        var players = new Array<any>();
        let scores = data.scores;
        players[0] = [await userData(data.players[0]), scores[0]]
        players[1] = [await userData(data.players[1]), scores[1]]
        players[2] = [await userData(data.players[2]), scores[2]]
        players[3] = [await userData(data.players[3]), scores[3]]
        
        let game = {
            me: {
                id: user.id,
                username: player1.username,
                score: scores[0],
                profile_picture_url : player2.profile_picture_url
            },
            opponent: {
                id: player2.id,
                username: player2.username,
                score: scores[1],
                profile_picture_url : player2.profile_picture_url
            },
            gamemode: "Shooter",
            type: data.type,
            winner: data.winner,
            date: data.match_date.substring(0, 10),
            hours: data.match_date.substring(11, 16),
            players: players
        }
        gamesHistory.push(game);
    }

</script>

<div class="flex-column history-container mb-5 justify-content-top">
    {#if gamesHistory[0] != null}
        {#each gamesHistory as game}
        <div class="row border  rounded match my-1 bg-dark text-truncate {game.winner == game.me.id ? 'border-primary' : 'border-danger'}">
            {#if game.gamemode != "Shooter"}
                <p class="col-4 text-center text-light h4 mt-1">Me</p>
                <p class="col-4 text-center h4 {game.winner == game.me.id ? 'text-primary' : 'text-danger'} mt-1">{game.me.score} / {game.opponent.score}</p>
                <a class="col-4 text-center text-light h4 link mt-1" href={"/profile/" + game.opponent.id}>{game.opponent.username}</a>
            {:else}
                {#each game.players as player}
                    <p class="col-1 text-center h4 {game.winner == game.me.id ? 'text-primary' : 'text-danger'} mt-1">{player[1]}</p>
                    <a class="col-1 text-center text-light h4 link mt-1" href={"/profile/" + player[0].id}>{player[0].username}</a>
                {/each}
            {/if}
                <div class="d-flex">
                    <p class="col-4" style="color:grey;">{game.date}</p>
                    <p class="col-4 game-title text-light text-center">{game.gamemode.toUpperCase()}</p>
                    <p class="col-4 text-end" style="color:grey;">{game.hours}</p>
                </div>
            </div>
        {/each}
    {:else}
        <div class="d-flex history-container justify-content-center align-items-center">
            <h5 class="" style="color:grey;">No match to Display</h5>
        </div>
    {/if}
</div>

<style>
    .history-container{
        width: 22vw;
        height: 45vh;
        margin: 0 auto;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: black grey;
        font-size: 0.9vw;
    }

    .match {
        width: 90%;
        min-width:90%;
        height: 15%;
        margin: auto;
    }

    .h4 {
        font-size: 0.90vw;
    }
    .h3 {
        font-size: 1.3vw;
    }

    .game-title {
        font-weight: 800;
    }

    .link{
        text-decoration:none;
    }

    .link:hover {
        text-decoration: underline;
    }

</style>