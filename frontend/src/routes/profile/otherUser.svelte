<script lang="ts">
    import { onMount } from 'svelte';
    import Pie from './pie.svelte';

    const img = new URL('$lib/assets/sforesti.jpg', import.meta.url).href;
    
    import type { Profile } from '../../stores/user';
    import { profileData, profile } from '../../stores/user';

    let victories = 15;
    let defeats = 3;
    let games = [];

    let user : Profile;
    $: user = $profile;

    onMount(async () => {
        await fetchHistoryMatches();
        truncHistory();  
        profile.subscribe((value : Profile) =>{
            user = value;
        })
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
    
    /******************HandleFriend******************/

    async function addFriend() {
        const receiver = user[currentUser]?.id;
        const response = await fetch('/api/send/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('access_token')}`},
            body: JSON.stringify({ receiver }),
        });
    }

</script>


<div class="container border rounded my-3 flex-fill">
    <div class="d-flex h-100">
            <div class="flex-column col-3 border-end my-3">
                <div class="border-bottom mx-3 me-4 pb-3">
                    <img src={user?.profile_picture} class="img-circle rounded-circle hover-effect ms-2">
                </div>
                <div class="p-4">
                    <h5 class="text-light"><i class="bi-person pe-3"></i>{user?.username}</h5>
                </div>
            </div>
            <div class="align-self-end align-img-end mb-3">
                <a href="" type="button" style="text-decoration: none" on:click={addFriend}><i class="bi bi-person-add hover-effect" style="color: grey; font-size: 1.3em"></i></a>
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