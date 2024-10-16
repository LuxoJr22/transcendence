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
        hours: String
    }

    let gamesHistory = new Array<Game>();
    export let data : any;
    export let user : Profile;

    onMount(async () => {
        gamesHistory = await parseHistoryMatches(data);
    })

    async function parseHistoryMatches(data : any){
        for (let i = 0; data[i] ; i++){
            let player1 : any = await userData(data[i].player1 != user.id ? data[i].player1 : data[i].player2);
            let scoreMe = 0;
            let scoreOpponent = 0;
            if (data[i].player1 == user.id){
                scoreMe = data[i].score1;
                scoreOpponent = data[i].score2; 
            }
            else {
                scoreMe = data[i].score2;
                scoreOpponent = data[i].score1;
            }
            let game = {
                me: {
                    score: scoreMe,
                },
                opponent: {
                    id: player1.id,
                    username: player1.username,
                    score: scoreOpponent,
                    profile_picture_url : player1.profile_picture_url
                },
                gamemode: data[i].gamemode,
                type: data[i].type,
                winner: data[i].winner,
                date: data[i].match_date.substring(0, 10),
                hours: data[i].match_date.substring(11, 16)
            }
            gamesHistory.push(game);
        }
        return (gamesHistory);
    }

</script>

<div class="flex-column history-container mb-5 justify-content-top">
    {#if gamesHistory[0] != null}
        {#each gamesHistory as game}
            <div class="row border {game.winner != game.opponent.id ? 'border-primary' : 'border-danger'} rounded match my-1 bg-dark text-truncate">
                <p class="col-4 text-center text-light h4 mt-1">{user.username}</p>
                <p class="col-4 text-center h4 {game.winner != game.opponent.id ? 'text-primary' : 'text-danger'} mt-1">{game.me.score} / {game.opponent.score}</p>
                <a class="col-4 text-center text-light h4 link mt-1" href={"/profile/" + game.opponent.id}>{game.opponent.username}</a>
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