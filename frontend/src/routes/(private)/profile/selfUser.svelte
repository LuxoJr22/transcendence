<script lang="ts">
    import { onMount } from 'svelte';
    import { get } from 'svelte/store'
    import Pie from './pie.svelte';
    import { auth, fetchUser, updateInformations, updateProfilePicture , updatePassword, refresh_token } from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth';
    import { fetchFriendList, friendList, deleteFriend } from "$lib/stores/friendship";
    import type { friendInterface } from '$lib/stores/friendship';
    import { userData } from '$lib/stores/user';

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

    let state: AuthState;
    state = $auth;

    let listOfFriend : friendInterface[];
    listOfFriend = $friendList; 

    onMount(async () => {
        await fetchHistoryMatches();
        await fetchFriendList();
        auth.subscribe((value : AuthState) =>{
            state = value;
        });
        friendList.subscribe((value : friendInterface[]) => {
            listOfFriend = value;
        });
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
            if (data[i].winner == state.user?.id)
                winRate[0] += 1;
            else
                winRate[1] += 1;
        }
        return (winRate)
    }

    async function parseHistoryMatches(data : any){
        for (let i = 0; data[i] ; i++){
            let player1 : any = await userData(data[i].player1 == state.user?.id ? data[i].player1 : data[i].player2);
            let player2 : any = await userData(data[i].player1 != state.user?.id ? data[i].player1 : data[i].player2);
            let game = {
                me: {
                    id: player1.id,
                    username: player1.username,
                    score: 5,
                    profile_picture_url : player1.profile_picture_url
                },
                opponent: {
                    id: player2.id,
                    username: player2.username,
                    score: 5,
                    profile_picture_url : player2.profile_picture_url
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
            console.log(winRate);
        }
    }
    let firstGame = 0;
    let i = 0;

    function prevButton(){
        firstGame -= 5;
    }

    function nextButton(){
        firstGame += 5;
    }

    /********updateProfilePicture********/

    let newProfilePicture : File;
    let errorPicture;
    function handleFileChange(event: Event) {
            newProfilePicture = event.target.files[0]; // Assigne le fichier sélectionné
    }

    function resetErrorsPicture() {
        errorPicture = '';
    }

    async function updateNewProfilePicture(){
        if (newProfilePicture)
        {
            errorPicture = await updateProfilePicture(newProfilePicture);
        }
        if (errorPicture && errorPicture != 'success')
            errorPicture = errorPicture.profile_picture;
    }

    /********updateEmailAndUsername********/

    let newUsername : string;
    let newEmail : string;
    let errorsMessage : string;
    let errorsEmail = false;
    let errorsUsername = false;

    function resetValue(){
        errorsMessage = '';
        errorsUsername = false;
        errorsEmail = false;
    }

    async function updateEmailAndUsername(){
        const data = await updateInformations((newEmail == '' ? state.user?.email : newEmail), (newUsername == '' ? state.user?.username : newUsername));
        if (!data)
        {
            errorsMessage = 'success';
            if (newEmail)
                errorsEmail = true;
            if (newUsername)
                errorsUsername = true;
        }
        else if (data.email)
        {
            errorsMessage = data.email;
            errorsEmail = true;
        }
        else if (data.username)
        {
            errorsMessage = data.username;
            errorsUsername = true;
        }
        else
            errorsMessage = '';
        newEmail = '';
        newUsername = '';
    }
    
    /********updatePassword********/

    let newPassword : string;
    let currentPassword : string;
    let errorsPassword : string;

    async function updateNewPassword() {
       const response : any = await updatePassword(newPassword, currentPassword);
        if (response.password)
        {
            errorsPassword = response.password;
        }
        else if (response.current_password)
        {
            errorsPassword = response.current_password;
        }
        else if (response == 'success')
        {
            errorsPassword = 'success';
        }
    }

</script>


<div class="container border rounded my-3">
    <div class="d-flex">
        <div class="flex-column col-3 border-end my-3">
            <div class="border-bottom mx-3 me-4 pb-3">
                <div class="d-flex justify-content-center align-items-center">
                    <a href="" type="button" data-bs-toggle="modal" data-bs-target="#pictureModal"><img src={state.user?.profile_picture} class="img-circle rounded-circle hover-effect ms-2"></a>
                </div>
                <div class="modal fade" id="pictureModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                      <div class="modal-content">
                        <form on:submit|preventDefault="{updateNewProfilePicture}">
                            <div class="modal-body">
                                <input type="file" on:change={handleFileChange}>
                            </div>
                            {#if errorPicture != 'success' && errorPicture}
                            <div class="alert alert-danger mx-3" role="alert">
                                {errorPicture}
                            </div>
                            {:else if errorPicture == 'success'}
                            <div class="alert alert-success mx-3" role="alert">
                                Image successfully changed.
                            </div>
                            {/if}
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" on:click={resetErrorsPicture}>Close</button>
                                <button type="submit" class="btn btn-success" on:click={resetErrorsPicture}>Save changes</button>
                            </div>
                        </form>
                      </div>
                    </div>
                </div>
            </div>
            <div class="p-4 border-bottom mx-3 me-4 mb-4">
                <h5 class="text-light"><i class="bi-person pe-3"></i>{state.user?.username}</h5>
            </div>
            <div class="mb-3">
                <h5 class="text-light friend-title d-flex justify-content-center">Friends</h5>
            </div>
                <div class="mx-3 me-4 mb-5 friend-container">
                    {#each listOfFriend as friend}
                        <div class="border rounded d-flex me-3 mb-2 my-bg-black">
                            <img src={friend.profile_picture_url} class="img-circle rounded-circle m-2" style="object-fit:cover; width:15%; height:20%;">
                            <div class="d-flex">
                                <p class="text-light ms-2 mt-3" style="font-size:100%;">{friend.username}</p>
                                <button class="btn" on:click={deleteFriend(friend.id)}><i class="bi bi-x-lg" style="color:red;"></i></button>
                            </div>
                        </div>
                    {/each}
                    {#if !listOfFriend[0]}
                        <p class="d-flex justify-content-center mt-3" style="color:grey;">Empty friend list</p>
                    {/if}
                </div>
        </div>
        <div class="align-self-end align-img-end mb-3">
            <a href="" type="button" data-bs-toggle="modal" data-bs-target="#userDataModal" style="text-decoration: none"><i class="bi bi-pencil hover-effect" style="color: grey; font-size: 1.3em"></i></a>
        </div>
        <div class="modal fade" id="userDataModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content">
                    <div class="modal-body">
                        <button class="btn btn-dark my-2" data-bs-toggle="collapse" data-bs-target="#collapseChangeUsername" aria-expanded="false" aria-controls="collapseExample" on:click={resetValue}>Change username</button>
                        <div class="collapse" id="collapseChangeUsername">
                            <div class="card card-body">
                                <form on:submit|preventDefault="{updateEmailAndUsername}">
                                    <input type="text" class="form-control" bind:value={newUsername}>
                                    <button class="btn btn-success my-2" type="submit" on:click={resetValue}>Confirm</button>
                                    {#if errorsMessage == 'success' && errorsUsername}
                                        <div class="alert alert-success" role="alert">
                                            Username changed with success
                                        </div>
                                    {:else if errorsMessage && errorsUsername == true}
                                    <div class="alert alert-danger" role="alert">
                                        {errorsMessage}
                                    </div>
                                    {/if}
                                </form>
                            </div>
                        </div>
                        <button class="btn btn-dark my-2" data-bs-toggle="collapse" data-bs-target="#collapseChangeEmail" aria-expanded="false" aria-controls="collapseExample" on:click={resetValue}>Change Email</button>
                        <div class="collapse" id="collapseChangeEmail">
                            <div class="card card-body">
                                <form on:submit|preventDefault="{updateEmailAndUsername}">
                                    <input type="text" class="form-control" bind:value={newEmail}>
                                    <button class="btn btn-success my-2" type="submit" on:click={resetValue}>Confirm</button>
                                    {#if errorsMessage == 'success' && errorsEmail == true}
                                        <div class="alert alert-success" role="alert">
                                            Email changed with success
                                        </div>
                                    {:else if errorsMessage && errorsEmail == true}
                                    <div class="alert alert-danger" role="alert">
                                        {errorsMessage}
                                    </div>
                                    {/if}
                                </form>
                            </div>
                        </div>
                        <button class="btn btn-dark my-2" data-bs-toggle="collapse" data-bs-target="#collapseChangePassword" aria-expanded="false" aria-controls="collapseExample">Change password</button>
                        <div class="collapse" id="collapseChangePassword">
                            <div class="card card-body">
                                <form on:submit|preventDefault="{updateNewPassword}">
                                    <h5 class="py-3">New password</h5>
                                    <input type="text" class="form-control" bind:value={newPassword}>
                                    <h5 class="py-3">Current password</h5>
                                    <input type="text" class="form-control" bind:value={currentPassword}>
                                    {#if errorsPassword == 'success'}
                                    <div class="alert alert-success" role="alert">
                                        Password changed with success
                                    </div>
                                    {:else if errorsPassword}
                                    <div class="alert alert-danger" role="alert">
                                        {errorsPassword}
                                    </div>
                                    {/if}
                                    <button class="btn btn-success my-2" type="submit">Confirm</button>
                                </form>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
              </div>
            </div>
        </div>
        <div class="flex-column col-4 border-end my-3 ">
            <div>
                <h2 class="text-center p-3 title-profile">Win Rate</h2>
            </div>
            <div class="d-flex justify-content-center" style="height:40%;">
                {#if finish}
                    <Pie victories={victories} defeats={defeats}></Pie>
                {/if}
            </div>
            <h2 class="text-center p-3 title-profile">Skin</h2>
        </div>
        <div class="justify-content-center flex-column col-5">
            <h2 class="text-light text-center p-3 title-profile">History</h2>
            <div class="d-flex flex-column history-container my-bg-black border rounded justify-content-top">
                {#if gamesHistory[0] != null}
                    {#each gamesHistory as game}
                    {#if game.winner != game.opponent.id}
                        <div class="row border rounded match my-1 bg-dark col-12 text-truncate">
                            <p class="text-center text-primary h3 m-0 p-0">Win</p>
                            <p class="col-4 text-center text-light h4">Me</p>
                            <p class="col-4 text-center text-light h4">{game.me.score} / {game.opponent.score}</p>
                            <p class="col-4 text-center text-light h4">{game.opponent.username}</p>
                            <div class="d-flex">
                                <p class="col-5" style="color:grey;">{game.date}</p>
                                <p class="col-2 game-badge text-center">{game.gamemode.toUpperCase()}</p>
                                <p class="col-5 text-end" style="color:grey;">{game.hours}</p>
                            </div>
                        </div>
                    {:else}
                        <div class="row border rounded match my-1 bg-dark col-12 text-truncate">
                            <p class="text-center text-danger h3 m-0 p-0">Lose</p>
                            <p class="col-4 text-center text-light h4">Me</p>
                            <p class="col-4 text-center text-light h4">{game.me.score} / {game.opponent.score}</p>
                            <p class="col-4 text-center text-light h4">{game.opponent.username}</p>
                            <div class="d-flex">
                                <p class="col-5" style="color:grey;">{game.date}</p>
                                <p class="col-2 game-badge text-center">{game.gamemode.toUpperCase()}</p>
                                <p class="col-5 text-end" style="color:grey;">{game.hours}</p>
                            </div>
                        </div>
                    {/if}
                    {/each}
                {:else}
                    <div class="d-flex align-items-center">
                        <h5 class="" style="color:grey;">No match to Display</h5>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>

    .img-circle {
        width: 80%;
        height: 80%;
        object-fit: cover;
        aspect-ratio: 1;
    }

    .title-profile {
        font-family: Nabla;
        font-size: 250%;
    }

    .my-text-black{
        color : rgb(255, 255, 255);
    }

    .align-img-end {
        transform: translateX(-200%);
    }

    .hover-effect:hover {
        opacity: 0.5;
    }

    .friend-container{
        width: 90%;
        height: 20%;
        max-height: 20%;
        overflow: auto !important;
        scrollbar-width: thin;
        scrollbar-color: black grey;
    }

    .friend-title{
        font-family: Nabla;
        font-size: 175%;
    }
    .container {
        height: 70%;
    }
    .history-container{
        width: 22vw;
        height: 45vh;
        min-height: 60%;
        margin: 0 auto;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: black grey;
    }
    .match {
        width: 90%;
        height: 25%;
        margin: auto;
    }

    .game-badge {
        border: 1px solid rgba(255, 255, 255, 0.3); /* Bord plus subtil */
        border-radius: 2px;
        background: linear-gradient(145deg, rgb(214, 213, 170), rgb(241, 255, 52));
        box-shadow: 1px 1px 4px rgb(241, 255, 49);
        font-weight: 800;
    }

    .my-bg-black {
        background-color: rgba(0, 0, 0, 0.4);
    }
</style>