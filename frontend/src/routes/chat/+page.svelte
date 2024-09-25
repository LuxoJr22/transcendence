<script lang='ts'>
    import { onMount } from 'svelte';
    import { auth, fetchUser } from '../../stores/auth';
    import type { AuthState } from '../../stores/auth';
    import { fetchFriendList, friendList, deleteFriend } from "../../stores/friendship";
    import type { friendInterface } from '../../stores/friendship';
    import { fetchChatMessages, messages, updateMessages } from '../../stores/chat';
    import type { Messages } from '../../stores/chat';
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
        fetchChatMessages(state.user?.id);
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
            let msg : Messages;
            console.log(event.data);
            updateMessages(event.data);
            fetchChatMessages(listOfFriend[userSelected].id);
            console.log('suh2');
        };
    }

    function sendMessage(){
        if (ws && ws.readyState === WebSocket.OPEN && newMessage.trim() !== '')
        {
            console.log('suh')
            let message = newMessage;
            ws.send(JSON.stringify({message}));
        }
    }

</script>

<div class="container flex-fill justify-content-center">
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
                <div>
                    {#each chatMessages as msg}
                        <p class="text-light">{msg.content}</p>
                    {/each}
                </div>
            {:else}
                <h4 class="d-flex justify-content-center align-items-center" style="color:grey;">You haven't discussions</h4>
            {/if}
        </div>
        <div class="">
            <div class="d-flex m-4">           
                <img class="rounded-circle m-2 img-circle" src={listOfFriend[userSelected]?.profile_picture_url}>
                <h4 class="text-light m-4">{listOfFriend[userSelected]?.username}</h4>
            </div>
        </div>
        <div class="d-flex flex-column-reverse m-5">
            <div>
        
            </div>
            <div>
                <input type="text" bind:value={newMessage} class="">
                <button class="btn btn-primary" on:click={sendMessage}></button>
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
        overflow-y: scroll;
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
        height: 22vh !important;
    }
</style>