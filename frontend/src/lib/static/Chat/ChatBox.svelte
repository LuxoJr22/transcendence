<script lang='ts'>
    import { fetchUser, type AuthState } from "$lib/stores/auth";
    import type { Messages } from "$lib/stores/chat";
    import { messages } from "$lib/stores/chat";
    import { beforeUpdate, afterUpdate, onMount } from 'svelte';
    import { goto } from '$app/navigation';

    export let roomId : string;
    export let state : AuthState;

    let chatMessages : Messages[];
    chatMessages = $messages;

    function joinPrivateGame(gamemode: string, match_id: string) {
        localStorage.setItem('game_id', match_id);
        goto(`/matchmaking/${gamemode}/private/`);
    }

    onMount(async () => {
        await fetchUser();
        messages.subscribe((value : Messages[]) => {
            chatMessages = value;
        });
    })

    let div : HTMLDivElement = 0;
    let autoscroll = false;
    beforeUpdate(() => {
        if (div){
            const scrollableDistance = div.scrollHeight - div.offsetHeight;
            autoscroll = div.scrollTop > scrollableDistance - 20;
        }
    });

    afterUpdate(() => {
        if (autoscroll && div) {
            div.scrollTo(0, div.scrollHeight);
        }
    });
</script>

{#if roomId == 'home'}
    <div class="d-flex position-absolute top-50" style="left:35%;">
            <h4 style="color:grey" class="">No discussion selectionned</h4>
    </div>
{:else}
    <div class="m-5 chat-box border rounded" bind:this={div}>
        {#each chatMessages as msg}
            <div class="d-flex justify-content-{msg.sender == state.user?.id ? 'end' : 'start'} text-center">
                <p class="col-auto border rounded bg-light p-2 m-2 msgBox">
                    {msg.content}
                    {#if msg.is_invitation && msg.is_over == false}
                        <button class="ms-2 btn btn-success btn-sm" on:click={() => joinPrivateGame(msg.gamemode, msg.match_id)}>Play</button>
                    {/if}
                </p>
            </div>
        {/each}
    </div>
{/if}

<style>
    .chat-box {
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: black grey;
        height: 75%;
        background-color: rgba(0, 0, 0, 0.2)
    }

    .msgBox{
        white-space: normal;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 40%;
    }
</style>