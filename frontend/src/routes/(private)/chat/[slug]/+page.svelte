<script lang='ts'>
    import { onDestroy, onMount } from 'svelte';
    import { auth, refresh_token } from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth';
    import { fetchChatMessages, messages, updateMessages, fetchLatestDiscussion , history} from '$lib/stores/chat';
    import type { Messages, History } from '$lib/stores/chat';
    import { beforeUpdate, afterUpdate } from 'svelte';
    import { profileData, profile } from '$lib/stores/user';
    import type { Profile } from '$lib/stores/user';
    import ImgOnline from '../../../../lib/static/imgOnline.svelte' 

    let state: AuthState;
    state = $auth;

    let chatMessages : Messages[];
    chatMessages = $messages;

    let user : Profile;
    user = $profile;

    let allUser = new Array<Profile>();

    let newMessage = '';

    let latestDiscussion : History[];
    latestDiscussion = $history;

    let userSearch : string;
    function resetFriendSearch (){
        userSearch = '';
    }

    async function fetchAllUser(){
        await refresh_token();
        const accessToken = localStorage.getItem('access_token');
        const response = await fetch('/api/user/list/', {
            headers : { 'Authorization': `Bearer ${accessToken}`}
        });

        if (response.ok){
            allUser = await response.json();
        }

    }
    
    onMount(async () => {
        await fetchAllUser();
        await fetchLatestDiscussion();
        let userId = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
        if (userId != 'home'){
            await profileData(parseInt(userId));
        }
        auth.subscribe((value : AuthState) =>{
            state = value;
        });
        messages.subscribe((value : Messages[]) => {
            chatMessages = value;
        });
        profile.subscribe((value : Profile) =>{
            user = value;
        });
        history.subscribe((value: History[]) =>{
            latestDiscussion = value
        })
        if (userId == 'home')
            user = null;
        if (parseInt(userId) == state.user?.id || window.location.href == '/chat')
            window.location.href = '/chat/home/';
        else if (userId != 'home'){
            createRoom(parseInt(userId));
        }
    });

    let ws : WebSocket;

    function loadRoom(userId : number){
        window.location.href = '/chat/' + (userId.toString()) + '/'; 
    }

    async function createRoom(id : number){
        await profileData(id);
        const token = localStorage.getItem('access_token');
        if (ws && ws.readyState == WebSocket.OPEN)
            ws.close();
        if (id)
            ws = new WebSocket('/ws/chat/' + id + '/?token=' + token);
        
            ws.onopen = function() {

            ws.onerror = function(error) {
                console.error('WebSocket error:', error);
            };
        };
        ws.onmessage = async function (event){
            const data = JSON.parse(event.data);
            updateMessages(data);
            await fetchLatestDiscussion();
            await fetchChatMessages(id);
            if (data.match_id && data.sender == state.user?.username) {
                joinPrivateGame(data.gamemode, data.match_id);
            }           
        };
        await fetchChatMessages(id);
    }

    async function sendMessage(){
        if (ws && ws.readyState === WebSocket.OPEN && newMessage.trim() !== '')
        {
            let message = newMessage;
            ws.send(JSON.stringify({message}));
            newMessage = '';
        }
        await fetchLatestDiscussion();
    }

    async function inviteToPong(){
        if (ws && ws.readyState === WebSocket.OPEN){
            ws.send(JSON.stringify({
                'message': 'Pong invite',
                'invite_pong': true,
                'gamemode': 'pong'
            }));
        }
        await fetchLatestDiscussion();
    }

    async function inviteToPongRetro(){
        if (ws && ws.readyState === WebSocket.OPEN){
            ws.send(JSON.stringify({
            'message': 'Pong invite',
            'invite_pong': true,
            'gamemode': 'pong_retro'
            }));
        }
        await fetchLatestDiscussion();
}

    function joinPrivateGame(gamemode: string, match_id: string) {
        localStorage.setItem('game_id', match_id);
        window.location.href = `/matchmaking/${gamemode}/private/`;
    }

    onDestroy(() => {
        if (ws && ws.readyState == WebSocket.OPEN){
            ws.close();
        }
    });
    /****************autoScroll****************/

    let div;
    let autoscroll = false;
    beforeUpdate(() => {
        if (div){
            const scrollableDistance = div.scrollHeight - div.offsetHeight;
            autoscroll = div.scrollTop > scrollableDistance - 20;
        }
    });
    
    afterUpdate(() => {
		if (autoscroll) {
			div.scrollTo(0, div.scrollHeight);
		}
	});

</script>

<div class="container flex-fill justify-content-center mycontainer">
    <div class="d-flex border rounded chat-container">
        <div class="col-3 border-end">
            <div class="d-flex m-4 row">
                <h4 class="text-light col-10 mt-2 text-truncate">Discussions</h4>
                <button type="button" class="btn col-2 p-0" data-bs-toggle="modal" data-bs-target="#userListModal"><i class="bi bi-plus" style="color:white; font-size:2em" on:click={async () => {await fetchAllUser()}}></i></button>
                <div class="modal fade" id="userListModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="userListModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content text-light bg-dark">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="userListModalLabel">Friends List</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" on:click={resetFriendSearch}></button>
                        </div>
                        <div class="d-flex justify-content-center">
                            <input class="form-control m-2 mt-4" placeholder="Find a user to chat" bind:value={userSearch} style="width:80%">
                        </div>
                        <div class="modal-body d-flex justify-content-center row row-cols-4 user-container m-0 me-2 mb-2">
                            {#each allUser as user}
                                {#if user.username.includes(userSearch) || !userSearch}
                                    <div class="col text-center p-0 m-2" role="button">
                                        <button class="text-center btn text-light bg-gradient border rounded" on:click={resetFriendSearch} on:click={loadRoom(user.id)} data-bs-dismiss="modal" aria-label="Close">
                                            <div class="d-flex justify-content-center">
                                                <ImgOnline path={user?.profile_picture_url} status={user?.is_online} width=50% height=50% />
                                            </div>
                                            <p class="text-center">{user.username}</p>
                                            <i class="bi bi-plus pt-2" style="font-size:1.8em"></i>
                                        </button>    
                                    </div>
                                {/if}
                            {/each}
                            {#if !allUser[0]}
                                <p class="d-flex justify-content-center mt-3" style="color:grey;">Empty user list</p>
                            {/if}
                        </div>
                        </div>
                    </div>
                </div>
            </div>
            {#if latestDiscussion && latestDiscussion[0]}
                <div class="mx-3 my-2 discussions-container">
                    {#each latestDiscussion as msg}
                        {#if user?.id == msg.id}
                            <div type="button" class="d-flex border opacity-50 rounded p-2 container my-2 user-container" style="width:100%; background-color: rgba(0, 0, 0, 0.2);" on:click={loadRoom(msg.id)}>
                                <div class="d-flex align-items-center" style="flex-shrink: 0; width: 20%; height: 15%;">
                                    <ImgOnline path={msg?.profile_picture_url} status={msg?.is_online} width=100% height=100%/>
                                </div>
                                <div class="ms-5">
                                    <div class="row">
                                        <a title="profile page" href="/profile/{msg?.id}" class='text-light text-truncate h5 link' on:click={(event) => event.stopPropagation()}>{msg.username}</a>
                                    </div>
                                    <div class="row">
                                        <p class='ms-2 m-0 p-0 text-truncate' style="color:grey;">
                                            {#if msg.last_message.sender == state.user?.id}
                                                Me:
                                            {:else}
                                                {msg.username}:  
                                            {/if}
                                                {msg.last_message.content}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        {:else}
                            <div type="button" class="d-flex border rounded p-2 container my-2 user-container" style="width:100%; background-color: rgba(0, 0, 0, 0.2);" on:click={loadRoom(msg.id)}>
                                <div class="d-flex align-items-center" style="flex-shrink: 0; width: 20%; height: 15%;">
                                    <ImgOnline path={msg?.profile_picture_url} status={msg?.is_online} width=100% height=100%/>
                                </div>
                                <div class="ms-5">
                                    <div class="row">
                                        <a title="profile page" href="/profile/{msg?.id}" class='text-light text-truncate h5 link' on:click={(event) => event.stopPropagation()}>{msg.username}</a>
                                    </div>
                                    <div class="row">
                                        <p class='ms-2 m-0 p-0 text-truncate' style="color:grey;">
                                            {#if msg.last_message.sender == state.user?.id}
                                                Me:
                                            {:else}
                                                {msg.username}:  
                                            {/if}
                                                {msg.last_message.content}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        {/if}
                    {/each}
                </div>
            {:else}
                <h4 class="d-flex justify-content-center align-items-center" style="color:grey;">You haven't discussions</h4>
            {/if}
        </div>
        <div class="col-9 container">
            <div class="d-flex m-4">
                {#if user == null}
                    <h4 style="color:grey">No discussion selectionned</h4>
                {/if}
            </div>
            {#if user != null}
            <div class="m-5 chat-box border rounded" bind:this={div}>
                {#each chatMessages as msg}
                    <div class="d-flex justify-content-{msg.sender == state.user?.id ? 'end' : 'start'} text-center">
                        <p class="col-auto border rounded bg-light p-2 m-2 msgBox">
                            {msg.content}
                            {#if msg.is_invitation}
                                <button class="ms-2 btn btn-success btn-sm" on:click={() => joinPrivateGame(msg.gamemode, msg.match_id)}>Play</button>
                            {/if}
                        </p>
                    </div>
                {/each}
            </div>
            {/if}
            <div>
                {#if user != null}
                <div class="d-flex justify-content-bottom justify-content-end me-2">
                    <form class="sendBox mb-2">
                        <input type="text" bind:value={newMessage} class="">
                        <button class="btn btn-primary btn-sm" on:click={sendMessage}>Send</button>
                    <div class="btn-group p-0">
                        <button type="button" class="btn btn-success btn-sm dropdown-toggle " data-bs-toggle="dropdown" aria-expanded="false">Play</button>
                        <ul class="dropdown-menu">
                            <li>
                                <button class="dropdown-item" on:click={inviteToPong}>Pong Invitation</button>                                
                            </li>
                            <li>
                                <button class="dropdown-item" on:click={inviteToPongRetro}>Pong Retro Invitation</button>
                            </li>
                        </ul>
                      </div>
                    </form>
                </div>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>
    .chat-container {
        width: 100%;
        height: 90%;
        overflow-y: auto;
    }

    .user-container{
        height: 20% !important;
        overflow-y: auto;
        overflow-x: hidden;
        scrollbar-width: thin;
        scrollbar-color: black grey;
    }

    .discussions-container {
        max-height: 80%;
        overflow-y: auto;
    }

    .modal-body {
        height: 23vh !important;
    }

    .chat-box {
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: black grey;
        height: 75%;
        background-color: rgba(0, 0, 0, 0.2)
    }

    .mycontainer{
        overflow: auto;
        height: 80vh;
    }

    .msgBox{
        white-space: normal;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 40%;
    }
    .sendBox input {
        border-radius: 10px;
        height:110%;
    }

    .link{
        text-decoration:none;
    }

    .link:hover {
        text-decoration: underline;
    }
</style>