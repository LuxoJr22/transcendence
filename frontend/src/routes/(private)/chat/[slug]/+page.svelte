<script lang='ts'>
    import { onDestroy, onMount } from 'svelte';
    import { auth, refresh_token } from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth';
    import { fetchChatMessages, messages, updateMessages, fetchLatestDiscussion , history} from '$lib/stores/chat';
    import type { Messages, History } from '$lib/stores/chat';
    import { profileData, profile } from '$lib/stores/user';
    import type { Profile } from '$lib/stores/user';
    import ModalUser from '$lib/static/Chat/ModalUser.svelte';
    import LatestDiscussion from '$lib/static/Chat/LatestDiscussion.svelte';
    import PlayButton from '$lib/static/Chat/PlayButton.svelte';
    import ChatBox from '$lib/static/Chat/ChatBox.svelte';

    let state: AuthState;
    state = $auth;

    let user : Profile;
    user = $profile;


    let newMessage = '';

    let roomId;
    
    onMount(async () => {
        await fetchLatestDiscussion();
        roomId = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
        if (roomId != 'home'){
            await profileData(parseInt(roomId));
        }
        auth.subscribe((value : AuthState) =>{
            state = value;
        });

        profile.subscribe((value : Profile) =>{
            user = value;
        });
        if (roomId == 'home')
            user = null;
        if (parseInt(roomId) == state.user?.id || window.location.href == '/chat')
            window.location.href = '/chat/home/';
        else if (roomId != 'home'){
            createRoom(parseInt(roomId));
        }
    });

    let ws : WebSocket;

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

    function joinPrivateGame(gamemode: string, match_id: string) {
        localStorage.setItem('game_id', match_id);
        window.location.href = `/matchmaking/${gamemode}/private/`;
    }

    onDestroy(() => {
        if (ws && ws.readyState == WebSocket.OPEN){
            ws.close();
        }
    });

</script>

<div class="container flex-fill justify-content-center mycontainer">
    <div class="d-flex border rounded chat-container">
        <div class="col-3 border-end">
            <ModalUser roomId={roomId}/>
            <LatestDiscussion state={state} userSelected={user} roomId={roomId}/>
        </div>
        <div class="col-9 container">
            <ChatBox state={state} user={user} />
            <div>
                {#if user != null}
                <div class="d-flex justify-content-bottom justify-content-end me-2">
                    <form class="sendBox mb-2">
                        <input type="text" bind:value={newMessage} class="">
                        <button class="btn btn-primary btn-sm" on:click={sendMessage}>Send</button>
                        <PlayButton ws={ws} />
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

    .mycontainer{
        overflow: auto;
        height: 80vh;
    }

    .sendBox input {
        border-radius: 10px;
        height:110%;
    }
</style>