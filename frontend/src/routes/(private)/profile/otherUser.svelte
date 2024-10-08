<script lang="ts">
    import { onMount } from 'svelte';
    import Pie from './pie.svelte';
    import type { Profile } from '$lib/stores/user';
    import { profileData, userData, profile } from '$lib/stores/user';

    export let userId;

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

    let victories = 15;
    let defeats = 3;
    let games = [];

    let user : Profile;
    $: user = $profile;

    onMount(async () => {
        await fetchHistoryMatches();
        await profileData(userId);
        profile.subscribe((value : Profile) =>{
            user = value;
        })
    });
    
    

    let winRate = new Array<number>();
    winRate[0] = 0;
    winRate[1] = 0;
    $: victories = winRate[0];
    $: defeats = winRate[1]; 
    let finish = false;
    /******************HISTORY******************/

    function calcWinRate(data: any){
        for (let i = 0; data[i] ; i++){
            if (data[i].winner == user.id)
                winRate[0] += 1;
            else
                winRate[1] += 1;
        }
        return (winRate)
    }

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
            console.log(game);
            gamesHistory.push(game);
        }
        return (gamesHistory);
    }

    export async function fetchHistoryMatches(){
        const response = await fetch("/api/pong/history/", {
            method: 'GET',
            headers:{
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            }
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data);
            gamesHistory = await parseHistoryMatches(data);
            winRate = calcWinRate(data);
            finish = true;
        }
    }
    
    /******************HandleFriend******************/

    let statusAddFriendRequest;

    async function addFriend() {
        const receiver = user.id;
        const response = await fetch('/api/send/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('access_token')}`},
            body: JSON.stringify({ receiver }),
        });
        statusAddFriendRequest = await response.json();
    }
    
    function handleGoto(e : Event, path : string) {
        e.preventDefault();
        window.location.href = path;
    }

</script>


<div class="container border rounded my-3">
    <div class="d-flex">
            <div class="flex-column col-3 border-end my-3">
                <div class="border-bottom mx-3 me-4 pb-3">
                    {#if user?.is_online}
                    <div class="d-flex justify-content-center align-items-end">
                        <img alt="user profile" src={user?.profile_picture} class="img-circle rounded-circle ms-2">
                        <span class="mt-2 badge rounded-pill bg-success">Online</span>
                    </div>
                    {:else}
                    <div class="d-flex justify-content-center align-items-end">
                        <img alt="user profile" src={user?.profile_picture} class="img-circle rounded-circle ms-2">
                        <span class="mt-2 badge rounded-pill bg-secondary">Offline</span>
                    </div>
                    {/if}
                </div>
                <div class="p-4">
                    <h5 class="text-light"><i class="bi-person pe-3"></i>{user?.username}</h5>
                </div>
            </div>
            <div class="align-self-end align-img-end mb-3">
                <button type="button" class="p-0 btn" on:click={addFriend}><i class="bi bi-person-add hover-effect" style="color: grey; font-size: 1.3em"></i></button>
            </div>
        <div class="flex-column col-4 border-end my-3 ">
            <div>
                <h2 class="text-light text-center p-3 title-profile">Win Rate</h2>
            </div>
            <div class="d-flex justify-content-center align-items-center" style="height:40%;">
                {#if finish}
                <Pie {victories} {defeats}></Pie>
                {/if}
            </div>
            <h2 class="text-center p-3 title-profile">Skin</h2>
        </div>
        <div class="justify-content-center flex-column col-5">
            <h2 class="text-light text-center p-3 title-profile">History</h2>
            <div class="flex-column history-container justify-content-top">
                {#if gamesHistory[0] != null}
                    {#each gamesHistory as game}
                    {#if game.winner != game.opponent.id}
                    <div class="row border border-primary rounded match my-1 bg-dark text-truncate">
                        <p class="col-4 text-center text-light h4 link" role="button" on:click={(event) => {handleGoto(event, "/profile/" + user.id)}}>{user.username}</p>
                        <p class="col-4 text-center text-light h4">{game.me.score} / {game.opponent.score}</p>
                        <p class="col-4 text-center text-light h4 link" role="button" on:click={(event) => {handleGoto(event, "/profile/" + game.opponent.id)}}>{game.opponent.username}</p>
                        <div class="d-flex">
                            <p class="col-4" style="color:grey;">{game.date}</p>
                            <p class="col-4 game-title text-light text-center">{game.gamemode.toUpperCase()}</p>
                            <p class="col-4 text-end" style="color:grey;">{game.hours}</p>
                        </div>
                    </div>
                    {:else}
                        <div class="row border border-danger rounded match my-1 bg-dark text-truncate">
                            <p class="col-4 text-center text-light h4 link" role="button" on:click={(event) => {handleGoto(event, "/profile/" + user.id)}}>{user.username}</p>
                            <p class="col-4 text-center text-light h4">{game.me.score} / {game.opponent.score}</p>
                            <p class="col-4 text-center text-light h4 link" role="button" on:click={(event) => {handleGoto(event, "/profile/" + game.opponent.id)}}>{game.opponent.username}</p>
                            <div class="d-flex">
                                <p class="col-4" style="color:grey;">{game.date}</p>
                                <p class="col-4 game-title text-light text-center">{game.gamemode.toUpperCase()}</p>
                                <p class="col-4 text-end" style="color:grey;">{game.hours}</p>
                            </div>
                        </div>
                    {/if}
                    {/each}
                {:else}
                    <div class="d-flex m-auto">
                        <h5 class="" style="color:grey;">No match to Display</h5>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>

    .img-circle{
        width: 80%;
        height: 80%;
        object-fit: cover;
        aspect-ratio: 1;
    }

    .title-profile {
        font-family: Nabla;
        font-size: 250%;
    }

    .align-img-end {
        transform: translateX(-200%);
    }

    .hover-effect:hover {
        opacity: 0.5;
    }

    .container {
        height: 70%;
    }

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
        font-size: 1.15vw;
    }
    .h3 {
        font-size: 1.3vw;
    }

    .game-title {
        font-weight: 800;
    }

    .my-bg-black {
        background-color: rgba(0, 0, 0, 0.4);
    }

    .link{
        text-decoration:none;
    }

    .link:hover {
        text-decoration: underline;
    }

</style>