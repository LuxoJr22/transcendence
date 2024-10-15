<script lang="ts">
    import type { AuthState } from "$lib/stores/auth";
    import { goto } from "$app/navigation"
    import ImgOnline from "../imgOnline.svelte";
    import { history } from "$lib/stores/chat";
    import type { History } from "$lib/stores/chat";
    import { onMount } from "svelte";

    export let state : AuthState;
    export let roomId : string;
    let latestDiscussion : History[];
    
    latestDiscussion = $history;

    onMount(() => {
        history.subscribe((value: History[]) =>{
            latestDiscussion = value
        })
    })

    function loadRoom(roomId : number){
        window.location.href = '/chat/' + (roomId.toString()) + '/'; 
    }
</script>

{#if latestDiscussion && latestDiscussion[0]}
    <div class="mx-3 my-2 discussions-container">
        {#each latestDiscussion as msg}
                <div type="button" class="d-flex border {(parseInt(roomId) != msg.id && roomId != 'home') ? 'opacity-50' : ''} rounded p-2 container my-2 user-container" style="width:100%; background-color: rgba(0, 0, 0, 0.2);" on:click={loadRoom(msg.id)}>
                    <div class="d-flex align-items-center" style="flex-shrink: 0; width: 20%; height: 15%;">
                        <ImgOnline path={msg?.profile_picture_url} status={msg?.is_online} width=100% height=100%/>
                    </div>
                    <div class="ms-5">
                        <div class="row">
                            <a title="profile page" href="/profile/{msg?.id}" class='text-light text-truncate h5 link' on:click={(event) => event.stopPropagation()}>{msg.username}</a>
                        </div>
                        <div class="row">
                            <p class='ms-2 m-0 p-0 text-truncate' style="color:grey;">
                                {#if msg.last_message.sender == state.user?.id}
                                    Me:
                                {:else}
                                    {msg.username}:  
                                {/if}
                                    {msg.last_message.content}
                            </p>
                        </div>
                    </div>
                </div>
        {/each}
    </div>
{:else}
    <h4 class="d-flex justify-content-center align-items-center" style="color:grey;">Not any discussion</h4>
{/if}

<style>
    .link{
        text-decoration:none;
    }

    .link:hover {
        text-decoration: underline;
    }

    .user-container{
        height: 20% !important;
        overflow-y: auto;
        overflow-x: hidden;
        scrollbar-width: thin;
        scrollbar-color: black grey;
    }

    .discussions-container {
        max-height: 80%;
        overflow-y: auto;
    }
</style>
