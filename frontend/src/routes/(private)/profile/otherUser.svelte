<script lang="ts">
    import { onMount } from 'svelte';
    import Pie from './pie.svelte';
    import type { Profile } from '$lib/stores/user';
    import { profileData, userData, profile } from '$lib/stores/user';
    import History from '$lib/static/Profile/History/otherHistory.svelte';

    export let userId;
    let data : any;

    let user : Profile;
    $: user = $profile;

    onMount(async () => {
        await fetchHistoryMatches();
        await profileData(userId);
        profile.subscribe((value : Profile) =>{
            user = value;
        })
    });
    
    /******************HISTORY******************/
    
    let victories = 0;
    let defeats = 0; 
    let finish = false;

    function calcWinRate(data: any){
        for (let i = 0; data[i] ; i++){
            if (data[i].winner == user.id)
                victories += 1;
            else
                defeats += 1;
        }
    }

    export async function fetchHistoryMatches(){
        const response = await fetch("/api/pong/history/" + user?.id, {
            method: 'GET',
            headers:{
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            }
        });

        if (response.ok) {
            data = await response.json();
            calcWinRate(data);
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
                    <Pie victories={victories} defeats={defeats}></Pie>
                {/if}
            </div>
            <h2 class="text-center p-3 title-profile">Skin</h2>
        </div>
        <div class="justify-content-center flex-column col-5">
            <h2 class="text-light text-center p-3 title-profile">History</h2>
            {#if finish}
                <History data={data} user={user}/>
            {/if}
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