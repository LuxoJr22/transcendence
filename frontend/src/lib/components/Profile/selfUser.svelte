<script lang="ts">
    import { onDestroy, onMount } from 'svelte';
    import { page } from '$app/stores';
    import Pie from './pie.svelte';
    import { auth, getAccessToken } from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth';
    import { fetchFriendList, friendList, deleteFriend } from "$lib/stores/friendship";
    import type { friendInterface } from '$lib/stores/friendship';
    import ImgOnline from '$lib/components/imgOnline.svelte';
    import ProfilePicture from '$lib/components/Profile/UpdateUserInformation/profilePicture.svelte';
    import Username from '$lib/components/Profile/UpdateUserInformation/username.svelte';
    import Email from '$lib/components/Profile/UpdateUserInformation/email.svelte';
    import Password from '$lib/components/Profile/UpdateUserInformation/password.svelte';
    import History from '$lib/components/Profile/History/History.svelte';
    import Skin from '$lib/components/Profile/Skin.svelte';


    let historyData : any = [];
    let fetchStatus = false;

    let state: AuthState;
    $: state = $auth;

    let listOfFriend : friendInterface[];
    listOfFriend = $friendList;

    window.addEventListener("popstate",(event) => {
        let myModal = bootstrap.Modal.getInstance(document.getElementById('userDataModal'));
        if (myModal)
            myModal.hide();
    });

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

    /******************HISTORY******************/
    
    let victories = 0;
    let defeats = 0; 

    function calcWinRate(data: any){
        for (let i = 0; data[i] ; i++){
            if (data[i].winner == state.user?.id && (data[i].gamemode == 'pong_retro' || data[i].gamemode == 'pong') && data[i].type == 'normal')
                victories += 1;
            else if ((data[i].gamemode == 'pong_retro' || data[i].gamemode == 'pong') && data[i].type == 'normal')
                defeats += 1;
        }
    }

    async function fetchHistoryMatches(){
        const token = await getAccessToken();
        const response = await fetch("/api/pong/history/" + state.user?.id, {
            method: 'GET',
            headers:{
                'Authorization': `Bearer ${token}`,
            }
        });

        if (response.ok) {
            historyData = historyData.concat(await response.json());
        }

        const resp = await fetch("/api/shooter/history/" + state.user?.id, {
            method: 'GET',
            headers:{
                'Authorization': `Bearer ${token}`,
            }
        });

        if (resp.ok) {
            historyData = historyData.concat(await resp.json());
            
            
        }
        if (resp.ok || response.ok)
        {
            calcWinRate(historyData);
            fetchStatus = true;
        }
    }
</script>


<div class="container border rounded my-3">
    <div class="d-flex">
        <div class="flex-column col-3 border-end my-3">
            <div class="border-bottom mx-3 me-4 pb-3">
                <ProfilePicture state={state}/>
            </div>
            <div class="p-4 border-bottom mx-3 me-4 mb-4">
                <h5 class="text-light"><i class="bi-person pe-3"></i>{state.user?.username}</h5>
            </div>
            <div class="mb-3">
                <h5 class="friend-title d-flex justify-content-center">Friends</h5>
            </div>
                <div class="mx-3 me-4 mb-5 friend-container">
                    {#each listOfFriend as friend}
                        <div class="border rounded d-flex align-items-center me-2 mb-2 my-bg-black">
                            <div class="d-flex ms-2 align-items-center">
                                <ImgOnline user_id={friend?.id} path={friend?.profile_picture_url} status={friend?.is_online} width=25% height=25% />
                                <a class="text-light ms-3 mb-3 mt-3 link" style="font-size:100%;" role="button" href={"/profile/" + friend.id}>{friend.username}</a>
                            </div>
                            <div class="d-flex">
                                <a class="btn" href="/chat/{friend.id}"><i class="bi bi-chat" style="color:white;"></i></a>
                                <button class="btn" on:click={() => deleteFriend(friend.id)}><i class="bi bi-x-lg" style="color:red;"></i></button>
                            </div>
                        </div>
                    {/each}
                    {#if !listOfFriend[0]}
                        <p class="d-flex justify-content-center mt-3" style="color:grey;">Empty friend list</p>
                    {/if}
                </div>
        </div>
        <div class="align-self-end align-img-end mb-3">
            <button class="btn m-0 p-0" type="button" data-bs-toggle="modal" data-bs-target="#userDataModal" style="text-decoration: none"><i class="bi bi-pencil hover-effect" style="color: grey; font-size: 1.3em"></i></button>
        </div>
        <div class="modal fade" id="userDataModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content">
                    <div class="modal-body">
                        <button class="btn btn-dark my-2" data-bs-toggle="collapse" data-bs-target="#collapseChangeUsername" aria-expanded="false" aria-controls="collapseExample">Change username</button>
                        <div class="collapse" id="collapseChangeUsername">
                            <Username />
                        </div>
                        <button class="btn btn-dark my-2" data-bs-toggle="collapse" data-bs-target="#collapseChangeEmail" aria-expanded="false" aria-controls="collapseExample">Change Email</button>
                        <div class="collapse" id="collapseChangeEmail">
                            <Email />
                        </div>
                        <button class="btn btn-dark my-2" data-bs-toggle="collapse" data-bs-target="#collapseChangePassword" aria-expanded="false" aria-controls="collapseExample">Change password</button>
                        <div class="collapse" id="collapseChangePassword">
                            <Password />
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
                {#if victories != 0 || defeats != 0}
                <p class="text-light text-center" style="font-weight:800; font-size:20px;">{(victories / (defeats + victories) * 100).toFixed(1)}%</p>
                {/if}
            </div>
            <div class="d-flex justify-content-center align-items-center" style="height:30%;">
                {#if fetchStatus}
                    <Pie victories={victories} defeats={defeats}></Pie>
                {/if}
            </div>
            <h2 class="text-center p-3 title-profile">Skin</h2>
            <div class="d-flex justify-content-center">
                <Skin self={true}/>
            </div>
        </div>
        <div class="justify-content-center flex-column col-5">
            <h2 class="text-center p-4 m-1 title-profile">History</h2>
            {#if fetchStatus}
                <History state={state} data={historyData}/>
            {/if}
        </div>
    </div>
</div>

<style>

    @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');

    .title-profile {
        font-family: "Luckiest Guy", sans-serif;
        font-size: 250%;
        color: var(--bs-light-bg-subtle);
    }

    .align-img-end {
        transform: translateX(-200%);
    }

    .hover-effect:hover {
        opacity: 0.5;
    }

    .friend-container{
        width: 90%;
        height: 150px;
        min-height: 20%;
        max-height: 20%;
        overflow: auto !important;
        scrollbar-width: thin;
        scrollbar-color: black grey;
    }

    .friend-title{
        color: var(--bs-light-bg-subtle);
        font-family: "Luckiest Guy", sans-serif;
        font-size: 175%;
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