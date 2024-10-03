<script lang='ts'>
    import { onMount } from 'svelte';
    import { auth, refresh_token } from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth';
    import { fetchChatMessages, messages, updateMessages } from '$lib/stores/chat';
    import type { Messages } from '$lib/stores/chat';
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
    
    let latestDiscussion = [];

    async function fetchLatestDiscussion(){
        const accessToken = localStorage.getItem('access_token');
        const response = await fetch('/api/chat/history/', {
        headers: {
            'Authorization': `Bearer ${accessToken}`,
        }
        });
        if (response.ok){
            const data = await response.json();
            return (data);
        }
    };

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
        auth.subscribe((value : AuthState) =>{
            state = value;
        });
        messages.subscribe((value : Messages[]) => {
            chatMessages = value;
        });
        profile.subscribe((value : Profile) =>{
            user = value;
        });
        latestDiscussion = await fetchLatestDiscussion();
    });

    let ws : WebSocket;
    async function createRoom(username : string, id : number){
        await profileData(id);
        const token = localStorage.getItem('access_token');
        if (id)
            ws = new WebSocket('/ws/chat/' + id + '/?token=' + token);
        
            ws.onopen = function() {

            ws.onerror = function(error) {
                console.error('WebSocket error:', error);
            };
        };
        ws.onmessage = async function (event){
            updateMessages(event.data);
            latestDiscussion = await fetchLatestDiscussion();
            await fetchChatMessages(id);
            
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
        latestDiscussion = await fetchLatestDiscussion();
    }


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
                <button type="button" class="btn col-2 p-0" data-bs-toggle="modal" data-bs-target="#userListModal"><i class="bi bi-plus" style="color:white; font-size:2em"></i></button>
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
                                    <div class="col text-center p-0 m-2">
                                        <button class="text-center btn text-light bg-gradient border rounded" on:click={resetFriendSearch} on:click={createRoom(user.username, user.id)} data-bs-dismiss="modal" aria-label="Close">
                                            <div class="d-flex justify-content-center">
                                                <ImgOnline path={user?.profile_picture_url} status={user?.is_online} width=50% height=50% />
                                            </div>
                                            <p class="">{user.username}</p>
                                            <i class="bi bi-plus" style="font-size:2em"></i>
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
            {#if latestDiscussion[0]}
                <div class="mx-3 my-2 discussions-container">
                    {#each latestDiscussion as msg}
                        <div type="button" class="d-flex border rounded p-2 container my-2 user-container" style="width:100%; background-color: rgba(0, 0, 0, 0.2)" on:click={createRoom(msg.username, msg.id)}>
                            <ImgOnline path={msg?.profile_picture_url} status={msg?.is_online} width=20% height=15%/>
                            <div class="ms-5">
                                <div class="row">
                                    <h5 class='text-light text-truncate'>{msg.username}</h5>
                                </div>
                                <div class="row">
                                    <p class='ms-2 m-0 p-0 text-truncate' style="color:grey">
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
                {:else}
                <div class='d-flex img-circle'>
                    <img class="rounded-circle m-2" style="width:70%" src={user?.profile_picture}>
                </div>
                <h4 class="text-light m-4">{user?.username}</h4>
                {/if}
            </div>
            {#if user != null}
            <div class="m-5 chat-box border rounded" bind:this={div}>
                {#each chatMessages as msg}
                    {#if msg.sender == state.user?.id}
                        <div class="d-flex justify-content-end text-center">
                            <p class="col-auto border rounded bg-light p-2 m-2 msgBox">{msg.content}</p>
                        </div>
                    {:else}
                        <div class="d-flex justify-content-start text-center">
                            <p class="col-auto border rounded bg-light p-2 m-2 msgBox">{msg.content}</p>
                        </div>
                    {/if}
                {/each}
            </div>
            {/if}
            <div>
                {#if user != null}
                <div class="d-flex justify-content-bottom justify-content-end me-2">
                    <form class="sendBox mb-2">
                        <input type="text" bind:value={newMessage} class="">
                        <button class="btn btn-primary btn-sm" on:click={sendMessage}>Send</button>
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

    .img-circle {
        width: 20%;
        overflow: hidden;
        object-fit: cover;
    }

    .img-circle img {
        width: auto;
        height: auto;
        z-index: 1;
        aspect-ratio: 1;
        object-fit: cover;
    }

    .modal-body {
        height: 23vh !important;
    }

    .chat-box {
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: black grey;
        height: 45%;
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
    }
</style>