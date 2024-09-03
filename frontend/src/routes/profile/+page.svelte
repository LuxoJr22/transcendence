<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import Pie from './pie.svelte';

    const img = new URL('$lib/assets/sforesti.jpg', import.meta.url).href;
    import { auth, fetchUser, logout, updateInformations, updateProfilePicture , updatePassword } from '../../stores/auth';
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
    let errorPicture = '';
    function handleFileChange(event: Event) {
            newProfilePicture = event.target.files[0]; // Assigne le fichier sélectionné
    }

    async function updateNewProfilePicture(){
        if (newProfilePicture)
            errorPicture = await updateProfilePicture(newProfilePicture);
        console.log(errorPicture);
    }

    /********updateEmailAndDisplayName********/

    let newDisplayName : string;
    let newEmail : string;
    let errorsMessage : string;
    let errorsEmail = false;
    let errorsDisplayName = false;

    function resetValue(){
        errorsMessage = '';
        errorsDisplayName = false;
        errorsEmail = false;
    }

    async function updateEmailAndDisplayName(){
        const data = await updateInformations((newEmail == '' ? state.user?.email : newEmail), (newDisplayName == '' ? state.user?.displayName : newDisplayName));
        console.log(data);
        if (!data)
        {
            errorsMessage = 'success';
            if (newEmail)
                errorsEmail = true;
            if (newDisplayName)
                errorsDisplayName = true;
        }
        else if (data.email)
        {
            errorsMessage = data.email;
            errorsEmail = true;
        }
        else if (data.display_name)
        {
            errorsMessage = data.display_name;
            errorsDisplayName = true;
        }
        else
            errorsMessage = '';
        console.log(errorsMessage);
        newEmail = '';
        newDisplayName = '';
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

    
</script>


<div class="container border rounded my-3 flex-fill">
    <div class="d-flex h-100">
        <div class="flex-column col-3 border-end my-3">
            <div class="border-bottom mx-3 me-4 pb-3">
                <a href="" type="button" data-bs-toggle="modal" data-bs-target="#pictureModal"><img src={state.user?.profile_picture} class="img-circle rounded-circle ms-2"></a>
                <div class="modal fade" id="pictureModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                      <div class="modal-content">
                        <form on:submit|preventDefault="{updateNewProfilePicture}">
                            <div class="modal-body">
                                <input type="file" on:change={handleFileChange}>
                            </div>
                            
                            {#if errorPicture == 'failed'}
                            <div class="alert alert-danger mx-3" role="alert">
                                An error has been occurred. Please check that the file is an image.
                            </div>
                            {:else if errorPicture == 'success'}
                            <div class="alert alert-success mx-3" role="alert">
                                Image successfully changed.
                            </div>
                            {/if}
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="submit" class="btn btn-success">Save changes</button>
                            </div>
                        </form>
                      </div>
                    </div>
                </div>
            </div>
            <div class="p-4">
                <h5 class="text-light"><i class="bi-person pe-3"></i>{state.user?.displayName}</h5>
                
                <h5 class="text-light"><i class="bi-person pe-3"></i>{state.user?.email}</h5>
            </div>
        </div>
        <div class="align-self-end align-img-end mb-3">
            <a href="" type="button" data-bs-toggle="modal" data-bs-target="#userDataModal" style="text-decoration: none"><i class="bi bi-pencil" style="color: grey; font-size: 1.3em"></i></a>
        </div>
        <div class="modal fade" id="userDataModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content">
                    <div class="modal-body">
                        <button class="btn btn-dark my-2" data-bs-toggle="collapse" data-bs-target="#collapseChangeDisplayName" aria-expanded="false" aria-controls="collapseExample" on:click={resetValue}>Change display name</button><br>
                        <div class="collapse" id="collapseChangeDisplayName">
                            <div class="card card-body">
                                <form on:submit|preventDefault="{updateEmailAndDisplayName}">
                                    <input type="text" class="form-control" bind:value={newDisplayName}>
                                    <button class="btn btn-success my-2" type="submit" on:click={resetValue}>Confirm</button>
                                    {#if errorsMessage == 'success' && errorsDisplayName}
                                        <div class="alert alert-success" role="alert">
                                            Display name changed with success
                                        </div>
                                    {:else if errorsMessage && errorsDisplayName == true}
                                    <div class="alert alert-danger" role="alert">
                                        {errorsMessage}
                                    </div>
                                    {/if}
                                </form>
                            </div>
                        </div>
                        <button class="btn btn-dark my-2" data-bs-toggle="collapse" data-bs-target="#collapseChangeEmail" aria-expanded="false" aria-controls="collapseExample" on:click={resetValue}>Change Email</button><br>
                        <div class="collapse" id="collapseChangeEmail">
                            <div class="card card-body">
                                <form on:submit|preventDefault="{updateEmailAndDisplayName}">
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
                                    <h4 class="py-3">New password</h4>
                                    <input type="text" class="form-control" bind:value={newPassword}>
                                    <h4 class="py-3">Current password</h4>
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
</style>