<script lang='ts'>
    import { onMount } from 'svelte';
    import { auth, fetchUser } from '../../stores/auth';
    import type { AuthState } from '../../stores/auth';
    import { fetchFriendList, friendList, deleteFriend } from "../../stores/friendship";
    import type { friendInterface } from '../../stores/friendship';
    import { fetchChatMessages, messages } from '../../stores/chat';
    import type { Messages } from '../../stores/chat';
    import ChatBox from './ChatBox.svelte';

    let state: AuthState;
    state = $auth;

    let listOfFriend : friendInterface[];
    listOfFriend = $friendList;

    let chatMessages : Messages;
    chatMessages = $messages;

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
    let ws;
    async function createRoom(username : string){
        for (let i = 0 ; listOfFriend[i] ; i++)
        {
            if (username == listOfFriend[i].username){
            userSelected = i;
                    break ;
            }
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
                                        <button class="btn text-light friend-card bg-gradient border rounded" on:click={resetFriendSearch} on:click={createRoom(friend.username)} data-bs-dismiss="modal" aria-label="Close">
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
                <p class="text-light">suhh</p>
            {:else}
                <h4 class="d-flex justify-content-center align-items-center" style="color:grey;">You haven't discussions</h4>
            {/if}
        </div>
        <ChatBox index={userSelected}/>
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

    /* :global(.friend-container::-webkit-scrollbar-thumb) {
        border: 4px solid !important;
        border-radius: 10px !important;       
        background-clip: padding-box !important; 
    } */

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

    .modal-body {
        height: 22vh !important;
    }
</style>