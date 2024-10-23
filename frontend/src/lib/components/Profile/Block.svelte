<script lang="ts">
    import { getAccessToken, refresh_token } from "$lib/stores/auth";
    import { onMount } from "svelte";

    let currentUserId = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
    let listUserBlocked : any;
    let blocked = false

    onMount(async () => {
        const token = await getAccessToken();
		if (token == null)
			return ;
        await blockedUser();
        for (let i = 0; listUserBlocked[i]; i++){
            if (listUserBlocked[i].id == currentUserId){
                blocked = true;
                break;
            }
        }
    })

    async function blockedUser(){
        const accessToken = await getAccessToken();
        const response = await fetch ('/api/blocked/', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${accessToken}` },
        })

        if (response.ok){
            listUserBlocked = await response.json();
        }
    }

    async function blockUser(){
        const accessToken = await getAccessToken();
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
        const accessToken = await getAccessToken();
        let id = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
        const response = await fetch ('/api/unblock/' + id + '/', {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${accessToken}` }
        })

        if (response.ok){
            listUserBlocked = await blockedUser;
            blocked = false;
        }
        else if (response.status == 401)
            refresh_token();
    }
</script>

<div>
    {#if blocked}
        <div class="position-absolute bottom-0">
            <button class="btn bg-black text-light align-self-end opacity" on:click={UnblockUser}><i class="bi bi-ban pe-2"></i>Unblock</button>
        </div>
    {:else}
        <div class="position-absolute bottom-0">
            <button class="btn bg-black text-light align-self-end opacity" on:click={blockUser}><i class="bi bi-ban pe-2"></i>Block</button>
        </div>
    {/if}
</div>

<style>
    .opacity:hover {
        opacity: 0.5;
    }
</style> 