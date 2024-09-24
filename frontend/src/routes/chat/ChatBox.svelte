<script lang="ts">
    import type { friendInterface } from "../../stores/friendship";
    import { fetchFriendList, friendList } from "../../stores/friendship";
    import { fetchChatMessages, messages } from '../../stores/chat';
    import type { Messages } from '../../stores/chat';
    import { onMount } from "svelte";

    export let index : number;

    let listOfFriend : friendInterface[] | null;
    $: listOfFriend = $friendList;

    let message : Messages;
    $: message = $messages;

    let newMessage = '';
    let ws : WebSocket;



    onMount ( async () =>{
        //await fetchFriendList();
        const token = localStorage.getItem('access_token');
        const username = listOfFriend[index]?.username;
        if (username)
            ws = new WebSocket('/ws/chat/' + username + '/?token=' + token);

        ws.onmessage = function (event){
            console.log(event.data);
        };
        await fetchChatMessages(username);
    });

    function sendMessage(){
        if (ws && ws.readyState === WebSocket.OPEN)
            ws.send(newMessage);
    }
</script>

<div class="">
    <div class="d-flex m-4">           
            <img class="rounded-circle m-2 img-circle" src={listOfFriend[index]?.profile_picture_url}>
            <h4 class="text-light m-4">{listOfFriend[index]?.username}</h4>
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

<style>
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
</style>