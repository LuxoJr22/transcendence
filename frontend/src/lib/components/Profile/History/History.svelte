<script lang="ts">
    import { auth, type AuthState } from "$lib/stores/auth";
    import { userData } from "$lib/stores/user";
    import { onMount } from "svelte";
    import { page } from '$app/stores';

    export let data;
    let historyToDisplay : string;
    $: userId = $page.params.id;
    
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
    export let state : AuthState | null;
    
    onMount(async () => {
        auth.subscribe((value) => {
            state = value;
        })
        gamesHistory = await parseHistoryMatches(data);
        historyToDisplay = (someGameOf('pong' ) ? 'pong' : 'Shooter');
    })    

    function someGameOf(gamemode : string){
        for (let i = 0; gamesHistory[i]; i++){
            if (gamesHistory[i].gamemode == gamemode || (gamesHistory[i].gamemode == 'pong_retro' && gamemode == 'pong')){
                return (true);
            }
        }
        return (false);
    }

    async function parseHistoryMatches(data : any[]){
        for (let i = 0; data[i] ; i ++)
        {
            if (data[i].gamemode)
                await ParsePongGame(data[i])
            else
                await ParseShooterGame(data[i])
        }
        return (gamesHistory);
    }

    async function ParsePongGame(data : any) {
        let player1 : any = await userData(data.player1 == userId ? data.player1 : data.player2);
        let player2 : any = await userData(data.player1 != userId ? data.player1 : data.player2);
        let scoreMe = 0;
        let scoreOpponent = 0;
        if (data.player1 == userId){
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

        let player1 : any = await userData(userId);
        let score : number = 0;
        for (let i = 0; data.scores[i]; i++){
            if (data.scores[i].player_id == userId){
                score = data.scores[i].score;
            }
        }
        let game = {
            me: {
                id: userId,
                username: player1.username,
                score: score,
                profile_picture_url : ''
            },
            opponent: {
                id: userId,
                username: player1.username,
                score: score,
                profile_picture_url : ''
            },
            gamemode: "Shooter",
            type: data.type,
            winner: data.winner,
            date: data.match_date.substring(0, 10),
            hours: data.match_date.substring(11, 16),
            players: []
        }
        gamesHistory.push(game);
    }

</script>

<div class="flex-column history-container justify-content-top">
    {#if someGameOf(historyToDisplay)}
        {#each gamesHistory as game}
            {#if game.gamemode != "Shooter" && historyToDisplay == 'pong'}
                <div class="row border  rounded match my-1 bg-dark text-truncate {game.winner == userId ? 'border-primary' : 'border-danger'}">
                    <p class="col-4 text-center text-light h4 mt-1">{state?.user?.id == userId ? 'Me' : game.me.username}</p>
                    <p class="col-4 text-center h4 {game.winner == userId ? 'text-primary' : 'text-danger'} mt-1">{game.me.score} / {game.opponent.score}</p>
                    <a class="col-4 text-center text-light h4 link mt-1" href={"/profile/" + game.opponent.id}>{game.opponent.username}</a>
                    <div class="d-flex">
                        <p class="col-4" style="color:grey;">{game.date}</p>
                        <div class="col-4 d-flex justify-content-center">
                            <p class="game-title text-light text-center">{game.gamemode.toUpperCase()}</p>
                            {#if game.type == 'normal'}
                                <i class="bi bi-people-fill text-light ms-1" title='Public Game'></i>
                            {:else if game.type == 'private'}
                                <i class="bi bi-person-fill-lock text-light ms-1" title='Private Game'></i>
                            {/if}
                        </div>
                        <p class="col-4 text-end" style="color:grey;">{game.hours}</p>
                    </div>
                </div>
            {:else if game.gamemode == "Shooter" && historyToDisplay == 'Shooter'}
                <div class="row border rounded match my-1 bg-dark text-truncate {(game.winner == userId) ? 'border-primary' : 'border-danger'}">
                    <div class="d-flex justify-content-center">
                        <p class="text-center text-light h4 link mt-1 me-2">Score :</p>
                        <p class="text-center h4 {(game.winner == userId) ? 'text-primary' : 'text-danger'} mt-1">{game.me.score}</p>
                    </div>
                    <div class="d-flex">
                        <p class="col-4" style="color:grey;">{game.date}</p>
                        <p class="col-4 game-title text-light text-center">{game.gamemode.toUpperCase()}</p>
                        <p class="col-4 text-end" style="color:grey;">{game.hours}</p>
                    </div>
                </div>
            {/if}
        {/each}
    {:else}
        <div class="d-flex history-container justify-content-center align-items-center">
            <h5 class="" style="color:grey;">No match to Display</h5>
        </div>
    {/if}
</div>
<div class="d-flex justify-content-center mb-3">
    <button class="btn btn-light" on:click={() => {historyToDisplay == 'Shooter' ? historyToDisplay = 'pong' : historyToDisplay = 'Shooter'}}>{historyToDisplay == 'Shooter' ? 'Pong' : 'Shooter'} Games</button>
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