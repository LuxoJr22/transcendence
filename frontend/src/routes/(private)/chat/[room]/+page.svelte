<script lang='ts'>
    import { onDestroy, onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores'
    import { auth} from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth';
    import { fetchChatMessages, fetchLatestDiscussion } from '$lib/stores/chat';
    import ModalUser from '$lib/components/Chat/ModalUser.svelte';
    import LatestDiscussion from '$lib/components/Chat/LatestDiscussion.svelte';
    import PlayButton from '$lib/components/Chat/PlayButton.svelte';
    import ChatBox from '$lib/components/Chat/ChatBox.svelte';

    $: roomId = $page.params.room;
    let ws : WebSocket;
    let state: AuthState;
    
    state = $auth;
    let newMessage : String = '';
    let messageInput: HTMLTextAreaElement;
    var input: HTMLElement
    var box: HTMLElement 

    $: {
        roomId;
        fetchLatestDiscussion();
        roomId = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
        auth.subscribe((value : AuthState) =>{
            state = value;
        });
        if (roomId != 'home'){
            createRoom(parseInt(roomId));
        }
    }

    
    
    window.onresize = function(event){
        let wid = box?.getBoundingClientRect().width
        if (wid && input)
            input.style.width = (wid -  185) + "px"
	}

    onMount(async () => {
        await fetchLatestDiscussion();
        roomId = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
        auth.subscribe((value : AuthState) =>{
            state = value;
        });
        if (parseInt(roomId) == state.user?.id || window.location.href == '/chat')
            goto('/chat/home/');
        else if (roomId != 'home'){
            createRoom(parseInt(roomId));
        }
    });



    async function createRoom(id : number){
        await fetchChatMessages(id);
        input = document.getElementById("input")!
        box = document.getElementById("box")!
        let wid = box!.getBoundingClientRect().width

        if (input)
            input.style.width = (wid -  185) + "px"
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
            await fetchLatestDiscussion();
            await fetchChatMessages(id);
        };
    }

    async function sendMessage(){
        if (ws && ws.readyState === WebSocket.OPEN && newMessage.trim() !== '')
        {
            let message = newMessage.replaceAll('\n', '<br>');
            ws.send(JSON.stringify({message}));
            newMessage = '';
            messageInput.focus();
        }
        await fetchLatestDiscussion();
    }

    document.addEventListener('keydown', async (event:KeyboardEvent) => {
        if (event.code == 'Enter' && !event.shiftKey){
            await sendMessage();
            newMessage = '';
        }
    });

    onDestroy(() => {
        if (ws && ws.readyState == WebSocket.OPEN){
            ws.close();
        }
    });

</script>

<div class="container flex-fill justify-content-center mycontainer">
    <div class="d-flex border rounded chat-container">
        <div class="col-3 border-end">
            <ModalUser />
            <LatestDiscussion state={state} roomId={roomId}/>
        </div>
        <div id="box" class="col-9 container position-relative">
            <ChatBox state={state} roomId={roomId} />
            <div>
                {#if roomId != 'home'}
                <div class="d-flex justify-content-end">
                    <form class="sendBox" on:submit|preventDefault={sendMessage}>
                        <div class="d-flex justify-content-end">
                            <textarea id="input" placeholder="Enter a message" bind:this={messageInput} bind:value={newMessage} class="col-10 p-1 me-2"></textarea>
                            <button class="btn btn-primary btn-sm me-1" type="submit">Send</button>
                            <PlayButton ws={ws} />
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

    .mycontainer{
        overflow: auto;
        height: 80vh;
    }

    .sendBox textarea {
        border-radius: 10px;
        width: 46.5vw;
        height: 35px;
        resize: none;
        overflow: hidden;
    }
    
</style>