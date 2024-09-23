<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { createEventDispatcher } from 'svelte';
	import { auth } from '../../stores/auth';
	import type { User } from '../../stores/auth';
	import { fetchFriends } from '../../stores/friend';

	const dispatch = createEventDispatcher();

	export let friends = writable<User[]>([]);
	let selectedFriend: User | null = null;

	onMount(async () => {
		await fetchFriends();
		auth.subscribe((value) => {
			if (value.friends)
				friends.set(value.friends);
		});
	});

	const selectFriend = (friend: User) => {
		selectedFriend = friend;
		dispatch('friendSelected', { friend });
	};

</script>

<style>
	.friend-item {
		cursor: pointer;
		padding: 10px;
		border-bottom: 1px solid #ddd;
	}
	.friend-item:hover {
		background-color: #f0f0f0;
	}
</style>

<div>
	<h4>Friends</h4>
	<ul class="list-group">
	{#each $friends as friend}
		<li class="friend-item list-group-item" on:click={() => selectFriend(friend)}>
			<img src={friend.profile_picture} alt={friend.username} width="30" height="30" class="rounded-circle me-2">
			{friend.username}
		</li>
	{/each}
	</ul>
</div>
