<script lang="ts">
    import { onMount } from "svelte";

    let currentUserId = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
    let listUserBlocked : any;
    let blocked = false

    onMount(async () => {
        await blockedUser();
        for (let i = 0; listUserBlocked[i]; i++){
            if (listUserBlocked[i].id == currentUserId){
                blocked = true;
                break;
            }
        }
        console.log(blocked);
    })

    async function blockedUser(){
        const accessToken = localStorage.getItem('access_token');
        const response = await fetch ('/api/blocked/', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${accessToken}` },
        })

        if (response.ok){
            listUserBlocked = await response.json();
        }
    }

    async function blockUser(){
        const accessToken = localStorage.getItem('access_token');
        let id = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
        const response = await fetch ('/api/block/', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
            body : JSON.stringify({"blocked" : id})
        })

        if (response.ok){
            listUserBlocked = await blockedUser;
            blocked = true;
        }
    }

    async function UnblockUser(){
        const accessToken = localStorage.getItem('access_token');
        let id = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
        const response = await fetch ('/api/unblock/' + id + '/', {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${accessToken}` }
        })

        if (response.ok){
            listUserBlocked = await blockedUser;
            blocked = false;
        }
    }
</script>

<div>
    {#if blocked}
        <div class="position-absolute bottom-0">
            <button class="btn btn-danger align-self-end" on:click={UnblockUser}><i class="bi bi-ban pe-2"></i>Unblock</button>
        </div>
    {:else}
        <div class="position-absolute bottom-0">
            <button class="btn btn-danger align-self-end" on:click={blockUser}><i class="bi bi-ban pe-2"></i>Block</button>
        </div>
    {/if}
</div>