<script lang="ts">
    import { onMount } from 'svelte';
    import { get } from 'svelte/store'
    import Pie from './pie.svelte';
    import { auth, updatePassword} from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth';
    import { fetchFriendList, friendList, deleteFriend } from "$lib/stores/friendship";
    import type { friendInterface } from '$lib/stores/friendship';
    import { userData } from '$lib/stores/user';
    import ImgOnline from '$lib/static/imgOnline.svelte';
    import ProfilePicture from '$lib/static/Profile/UpdateUserInformation/profilePicture.svelte';
    import Username from '$lib/static/Profile/UpdateUserInformation/username.svelte';
    import Email from '$lib/static/Profile/UpdateUserInformation/email.svelte';
    import Password from '$lib/static/Profile/UpdateUserInformation/password.svelte';
    import History from '$lib/static/Profile/History/selfHistory.svelte';

    let historyData : any;
    let fetchStatus = false;

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
    
    function handleGoto(e : Event, path : string) {
        e.preventDefault();
        window.location.href = path;
    }

    /******************HISTORY******************/
    
    let victories = 0;
    let defeats = 0; 

    function calcWinRate(data: any){
        for (let i = 0; data[i] ; i++){
            if (data[i].winner == state.user?.id)
                victories += 1;
            else
                defeats += 1;
        }
    }

    async function fetchHistoryMatches(){
        const response = await fetch("/api/pong/history/" + state.user?.id, {
            method: 'GET',
            headers:{
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            }
        });

        if (response.ok) {
            historyData = await response.json();
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
                <h5 class="text-light friend-title d-flex justify-content-center">Friends</h5>
            </div>
                <div class="mx-3 me-4 mb-5 friend-container">
                    {#each listOfFriend as friend}
                        <div class="border rounded d-flex align-items-center me-2 mb-2 my-bg-black">
                            <div class="d-flex ms-2 align-items-center">
                                <ImgOnline path={friend?.profile_picture_url} status={friend?.is_online} width=20% height=20% />
                                <p class="text-light ms-3 mt-3 link" style="font-size:100%;" role="button" on:click={(event) => {handleGoto(event, "/profile/" + friend.id)}}>{friend.username}</p>
                            </div>
                            <div class="d-flex">
                                <a class="btn" href="/chat/{friend.id}"><i class="bi bi-chat" style="color:white;"></i></a>
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
            </div>
            <div class="d-flex justify-content-center align-items-center" style="height:40%;">
                {#if fetchStatus}
                    <Pie victories={victories} defeats={defeats}></Pie>
                {/if}
            </div>
            <h2 class="text-center p-3 title-profile">Skin</h2>
        </div>
        <div class="justify-content-center flex-column col-5">
            <h2 class="text-light text-center p-3 title-profile">History</h2>
            {#if fetchStatus}
                <History state={state} data={historyData}/>
            {/if}
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
        font-family: Nabla;
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