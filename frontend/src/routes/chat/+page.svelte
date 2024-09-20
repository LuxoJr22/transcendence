<script lang='ts'>
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import { auth, fetchUser } from '../../stores/auth';
    import type { AuthState, User } from '../../stores/auth';
    import FriendsList from './FriendsList.svelte';
    import ChatBox from './ChatBox.svelte';

    let state: AuthState;
    $: state = $auth;

    let selectedFriend = writable<User | null>(null);

    onMount(async () => {
        const token = localStorage.getItem('access_token');
        if (token) {
            await fetchUser();
        }
        auth.subscribe((value : AuthState) =>{
            state = value
        });
    });

    const handleFriendSelected = (event) => {
        selectedFriend.set(event.detail.friend);
    };
</script>

<div class="chat-container">
    <div class="friends-list">
        <FriendsList on:friendSelected={handleFriendSelected} />
    </div>
    <div class="chat-box">
        {#if $selectedFriend}
            <ChatBox friend={$selectedFriend} />
        {:else}
        <p>Select a friend to start chatting</p>
        {/if}
    </div>
</div>