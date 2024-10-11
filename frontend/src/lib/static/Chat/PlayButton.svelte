<script lang="ts">
    import { fetchLatestDiscussion } from "$lib/stores/chat";

    export let ws : WebSocket;

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
</script>

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