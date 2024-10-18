<script lang="ts">
    import { onMount } from 'svelte';
    import Pie from './pie.svelte';
    import type { Profile } from '$lib/stores/user';
    import { profileData, userData, profile } from '$lib/stores/user';
    import History from '$lib/static/Profile/History/otherHistory.svelte';
    import Block from '$lib/static/Profile/Block.svelte';
    import { friendList, fetchFriendList, deleteFriend } from '$lib/stores/friendship';
    import type { friendInterface } from '$lib/stores/friendship';
    import Skin from '$lib/static/Profile/Skin.svelte';

    export let userId : string;
    let data : any = [];

    $: isFriendStatus = false;

    let user : Profile;
    $: user = $profile;

    let friends : friendInterface[];
    $: friends = $friendList;

    onMount(async () => {
        await fetchHistoryMatches();
        await profileData(parseInt(userId));
        await fetchFriendList();
        isFriendStatus = isFriend();
        profile.subscribe((value : Profile) =>{
            user = value;
        })
        friendList.subscribe((value : friendInterface[]) => {
            friends = value;
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
            data = data.concat(await response.json());
        }

        const resp = await fetch("/api/shooter/history/" + user?.id, {
            method: 'GET',
            headers:{
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            }
        });

        if (resp.ok) {
            data = data.concat(await resp.json());
            
            
        }
        if (resp.ok || response.ok)
        {
            calcWinRate(data);
            finish = true;
        }
    }
    
    /******************HandleFriend******************/

    interface Notifications {
        date: number,
        content: string
    }

    let notifications = new Array<Notifications>(1);

    function parseNotifications(data : any){
        notifications = notifications.filter(notif => Date.now() - notif.date < 5001);
        let tmp = '';
        if (data.receiver)
            tmp = "Friend request send with success";
        else if (data.non_field_errors)
            tmp = data.non_field_errors;
        let notif : Notifications = {
            date: Date.now(),
            content: tmp
        };
        notifications.unshift(notif);
    }

    let statusAddFriendRequest : any;

    async function addFriend() {
        const receiver = user.id;
        const response = await fetch('/api/send/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('access_token')}`},
            body: JSON.stringify({ receiver }),
        });
        statusAddFriendRequest = await response.json();
        parseNotifications(statusAddFriendRequest);
        const toastElList = document.querySelectorAll('.toast')
        const toastList = [...toastElList].map(toastEl => new bootstrap.Toast(toastEl, {
            animation: true,
            autohide: true,
            delay: 5000
        }))
        toastList.forEach(toast => toast.show());
        await fetchFriendList();
        isFriendStatus = isFriend();
    }

    async function delFriend() {
        await deleteFriend(parseInt(userId));
        await fetchFriendList();
        isFriendStatus = isFriend();
    }

    function isFriend(){
        for (let friend of friends){
            
            if (friend.id == parseInt(userId)){
                return (true);
            }
        }
        return (false);
    }
</script>


<div class="container border rounded my-3">
    <div class="d-flex">
            <div class="flex-column col-3 border-end my-3 position-relative">
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
                <Block />
            </div>
            <div class="align-self-end align-img-end mb-3">
                {#if isFriendStatus == true}
                    <button type="button" class="p-0 btn" on:click={delFriend}><i class="bi bi-person-dash hover-effect" style="color: grey; font-size: 1.3em"></i></button>
                {:else if isFriendStatus == false}
                    <button type="button" class="p-0 btn" on:click={addFriend}><i class="bi bi-person-add hover-effect" style="color: grey; font-size: 1.3em"></i></button>
                {/if}
                </div>
        <div class="flex-column col-4 border-end my-3 ">
            <div>
                <h2 class="text-light text-center p-3 title-profile">Win Rate</h2>
                {#if victories != 0 || defeats != 0}
                    <p class="text-light text-center" style="font-weight:800; font-size:20px;">{(victories / (defeats + victories) * 100).toFixed(1)}%</p>
                {/if}
            </div>
            <div class="d-flex justify-content-center align-items-center" style="height:30%;">
                {#if finish}
                    <Pie victories={victories} defeats={defeats}></Pie>
                {/if}
            </div>
            <h2 class="text-center text-light p-3 title-profile">Skin</h2>
            <div class="d-flex justify-content-center">
                <Skin self={false} userId={parseInt(userId)}/>
            </div>
        </div>
        <div class="justify-content-center flex-column col-5">
            <h2 class="text-light text-center p-4 m-1 title-profile">History</h2>
            {#if finish}
                <History data={data} user={user}/>
            {/if}
        </div>
    </div>
</div>

<div id="toast" class="d-flex flex-column toast-container position-fixed bottom-0 end-0 p-3">
    {#each notifications as notif}
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <strong class="me-auto">Notifications</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body text-truncate">
                {notif?.content}
            </div>
        </div>
    {/each}
</div>

<style>

    @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');

    .img-circle{
        width: 80%;
        height: 80%;
        min-width: 10.9vw;
        min-height: 22.6vh;
        object-fit: cover;
        aspect-ratio: 1;
    }

    .title-profile {
        font-family: 'Luckiest Guy';
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

</style>