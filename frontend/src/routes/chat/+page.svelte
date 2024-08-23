<script>
    import { onMount } from 'svelte';

    let message = '';
    let messages = [];
    let socket;

    onMount(() => {
        socket = new WebSocket('/ws/chat/');

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            messages = [...messages, data.message];
        };

        socket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
    });

    function sendMessage() {
        socket.send(JSON.stringify({
            'message': message
        }));
        message = '';
    }
</script>

<style>
    /* Ton style CSS ici */
</style>

<div>
    <div>
        {#each messages as msg}
            <p style="color: white;">{msg}</p>
        {/each}
    </div>
    <input type="text" bind:value={message} on:keydown="{(e) => e.key === 'Enter' && sendMessage()}" />
    <button on:click={sendMessage}>Envoyer</button>
</div>
