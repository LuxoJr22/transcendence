<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { get } from 'svelte/store'
    import Pie from './pie.svelte';
    import { auth, fetchUser, updateInformations, updateProfilePicture , updatePassword } from '../../stores/auth';
    import type { AuthState } from '../../stores/auth';

    let victories = 15;
    let defeats = 3;
    let games = [];

    let state: AuthState;
    $: $auth, state = $auth;

    onMount(async () => {
        if (localStorage.getItem('access_token')) {
            await fetchUser();
        }
        await fetchHistoryMatches();
        await fetchFriendList();
        truncHistory();
        auth.subscribe((value : AuthState) =>{
            state = value
        });
    });
    
    

    /******************HISTORY******************/

    export async function fetchHistoryMatches(){
        const response = await fetch("/data/data.json", {
            method: 'GET'
        });

        if (response.ok) {
            games = await response.json();
        }
    }
    
    let actualPage = 1;
    let nbrGame = 0;
    let firstGame = 0;
    let GameToDisplay = [];
    let i = 0;

    function prevButton(){
        firstGame -= 5;
        truncHistory();
    }

    function nextButton(){
        firstGame += 5;
        truncHistory();
    }

    function truncHistory(){    
        let y = 0;
        for (let i = firstGame; i < firstGame + 5; i++)
        {
            GameToDisplay[y] = games[i];
            y ++;
        }
    }
    
    /******************updateUserData******************/


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
        console.log(data);
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
        console.log(errorsMessage);
        newEmail = '';
        newUsername = '';
    }
    
    /********updatePassword********/

    let newPassword : string;
    let currentPassword : string;
    let errorsPassword : string;

    async function updateNewPassword() {
       const response = await updatePassword(newPassword, currentPassword);
       console.log(response)
        if (response.password)
        {
            errorsPassword = response.password;
        }
        else if (response.current_password)
        {
            console.log('a');
            errorsPassword = response.current_password;
        }
        else if (response == 'success')
        {
            errorsPassword = 'success';
        }
    }

    /******************friend******************/

    let friendList = '';

    export async function fetchFriendList(){
        const { accessToken } = get(auth);

        if (!accessToken)
            return;

        const response = await fetch('/api/friends/', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${accessToken}` },
        });

        if (response.ok){
            const data = await response.json();
            friendList = data;
            console.log(data);
        }
    }
</script>


<div class="container border rounded my-3 flex-fill">
    <div class="d-flex h-100">
        <div class="flex-column col-3 border-end my-3">
            <div class="border-bottom mx-3 me-4 pb-3">
                <a href="" type="button" data-bs-toggle="modal" data-bs-target="#pictureModal"><img src={state.user?.profile_picture} class="img-circle rounded-circle hover-effect ms-2"></a>
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
            <div class="mx-3 me-4 friend-container">
                {#each friendList as friend}
                    <div class="border rounded d-flex mt-2 me-2">
                        <img src={friend.profile_picture_url} class="img-circle rounded-circle m-2" style="object-fit:cover; width:15%; height:20%;">
                        <div class="d-flex">
                            <p class="text-light ms-2 mt-3" style="font-size:100%;">{friend.username}</p>
                            <button class="btn"><i class="bi bi-x-lg" style="color:red;"></i></button>
                        </div>
                    </div>
                {/each}
                {#if !friendList[0]}
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
                <h2 class="text-light text-center p-3 title-profile">Win Rate</h2>
            </div>
            <div style="height:100%;">
                <Pie {victories} {defeats}></Pie>
            </div>
        </div>
        <div class=" flex-column col-5 my-3">
            <div>
                <h2 class="text-light text-center p-3 title-profile">History</h2>
                {#each GameToDisplay as game}
                    {#if game.won}
                    <div class="d-flex alert bg-primary mx-3 my-2 ms-4 my-text-black">
                        <div class="col text-center">
                            {game.user}     
                        </div>
                        <div class="col text-center">
                            {game.score}     
                        </div>
                        <div class="col text-center">
                            {game.opponent}     
                        </div>
                    </div>
                    {:else if !game.won}
                    <div class="d-flex alert bg-danger mx-3 my-2 ms-4 my-text-black">
                        <div class="col text-center">
                            {game.user}     
                        </div>
                        <div class="col text-center">
                            {game.score}     
                        </div>
                        <div class="col text-center">
                            {game.opponent}     
                        </div>
                    </div>
                    {/if}
                {/each}
                <div class="d-flex justify-content-center mt-5">
                <button class="btn btn-light m-1" on:click={prevButton}>Prev</button>
                <button class="btn btn-light m-1" on:click={nextButton}>Next</button>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .img-circle {
        width: 90%;
        overflow: hidden;
        object-fit: cover;
        aspect-ratio: 1;
    }

    .img-circle img {
        width: auto;
        height: auto;
        transform: translateX(-50%);
    }

    .title-profile {
        font-family: Nabla;
        font-size: 250%;
    }

    .my-text-black{
        color : rgb(255, 255, 255);
    }

    .bg-defeats {
        background-color: rgb(112, 78, 163);
    }
    .align-img-end {
        transform: translateX(-200%);
    }

    .hover-effect:hover {
        opacity: 0.5;
    }

    .friend-container{
        width: 90%;
        height: 30%;
        overflow: auto;
        scrollbar-width: thin;
        scrollbar-color: black grey;
    }

    div::-webkit-scrollbar-thumb {
        border: 4px solid;
        border-radius: 10px;       
        background-clip: padding-box; 
    }

    .friend-title{
        font-family: Nabla;
        font-size: 175%;
    }
</style>