<script lang='ts'>
    import { onMount } from 'svelte';
    import { auth, fetchUser } from '../../stores/auth';
    import type { AuthState } from '../../stores/auth';
    import { fetchFriendList, friendList, deleteFriend } from "../../stores/friendship";
    import type { friendInterface } from '../../stores/friendship';
    import { fetchChatMessages, messages, updateMessages } from '../../stores/chat';
    import type { Messages } from '../../stores/chat';
    import { beforeUpdate, afterUpdate } from 'svelte';
    let state: AuthState;
    state = $auth;

    let listOfFriend : friendInterface[];
    listOfFriend = $friendList;

    let chatMessages : Messages[];
    chatMessages = $messages;

    let newMessage = '';

    let friendSearch : string;
    function resetFriendSearch (){
        friendSearch = '';
    }
    
    onMount(async () => {
        if (localStorage.getItem('access_token')) {
            await fetchUser();
        }
        await fetchFriendList();
        auth.subscribe((value : AuthState) =>{
            state = value;
        });
        friendList.subscribe((value : friendInterface[]) => {
            listOfFriend = value;
        });
        messages.subscribe((value : Messages) => {
            chatMessages = value;
        });
    });
    
    let userSelected = -1;
    let ws : WebSocket;
    async function createRoom(username : string, id : number){
        
        for (let i = 0 ; listOfFriend[i] ; i++)
        {
            if (username == listOfFriend[i].username){
                userSelected = i;
                    break ;
            }
        }
        const token = localStorage.getItem('access_token');
        if (id)
            ws = new WebSocket('/ws/chat/' + id + '/?token=' + token);
        
            ws.onopen = function() {
            console.log('WebSocket connection opened');

            ws.onerror = function(error) {
                console.error('WebSocket error:', error);
            };
        };
        ws.onmessage = function (event){
            updateMessages(event.data);
            fetchChatMessages(listOfFriend[userSelected].id);
            
        };
        fetchChatMessages(listOfFriend[userSelected].id);
    }

    function sendMessage(){
        if (ws && ws.readyState === WebSocket.OPEN && newMessage.trim() !== '')
        {
            let message = newMessage;
            ws.send(JSON.stringify({message}));
            newMessage = '';
        }
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
                <button type="button" class="btn col-2 p-0" data-bs-toggle="modal" data-bs-target="#friendListModal"><i class="bi bi-plus" style="color:white; font-size:2em"></i></button>
                <div class="modal fade" id="friendListModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="friendListModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content text-light bg-dark">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="friendListModalLabel">Friends List</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" on:click={resetFriendSearch}></button>
                        </div>
                        <div class="d-flex justify-content-center">
                            <input class="form-control m-2 mt-4" placeholder="Find a friend to chat" bind:value={friendSearch} style="width:80%">
                        </div>
                        <div class="modal-body d-flex justify-content-center row row-cols-4 friend-container m-0 me-2 mb-2">
                            {#each listOfFriend as friend}
                                {#if friend.username.includes(friendSearch) || !friendSearch}
                                    <div class="col text-center p-0 m-2">
                                        <button class="btn text-light friend-card bg-gradient border rounded" on:click={resetFriendSearch} on:click={createRoom(friend.username, friend.id)} data-bs-dismiss="modal" aria-label="Close">
                                            <img src={friend.profile_picture_url} class="img-circle rounded-circle m-2" style="object-fit:cover; width:50%; height:50%;">
                                            <p class="">{friend.username}</p>
                                            <i class="bi bi-plus" style="font-size:2em"></i>
                                        </button>    
                                    </div>
                                {/if}
                            {/each}
                            {#if !listOfFriend[0]}
                                <p class="d-flex justify-content-center mt-3" style="color:grey;">Empty friend list</p>
                            {/if}
                        </div>
                        </div>
                    </div>
                </div>
            </div>
            {#if chatMessages[0]}
                <p>suh</p>
            {:else}
                <h4 class="d-flex justify-content-center align-items-center" style="color:grey;">You haven't discussions</h4>
            {/if}
        </div>
        <div class="col-9">
            <div class="d-flex m-4">
                {#if userSelected == -1}
                    <h4 style="color:grey">No discussion selectionned</h4>
                {:else}
                    <img class="rounded-circle m-2 img-circle" src={listOfFriend[userSelected]?.profile_picture_url}>
                    <h4 class="text-light m-4">{listOfFriend[userSelected]?.username}</h4>
                {/if}
            </div>
            {#if userSelected != -1}
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
                {#if userSelected != -1}
                <div class="d-flex justify-content-bottom justify-content-end me-2">
                    <form>
                        <input type="text" bind:value={newMessage} class="inputMessage">
                        <button class="btn btn-primary" on:click={sendMessage}>Send</button>
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
    }

    .friend-container{
        height: 20% !important;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: black grey;
    }

    .img-circle {
        width: 20%;
        overflow: hidden;
        object-fit: cover;
        aspect-ratio: 1;
    }

    .img-circle img {
        width: auto;
        height: auto;
    }

    .modal-body {
        height: 23vh !important;
    }

    .chat-box {
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: black grey;
        height: 45%;
    }

    .mycontainer{
        overflow: hidden;
    }

    .msgBox{
        white-space: normal;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 40%;
    }
</style>