<script lang="ts">
	import { onMount } from 'svelte';
	import { writable, get } from 'svelte/store';
	import { auth } from '../../stores/auth';
	import type { User } from '../../stores/auth';
	
	export let friend: User;

	type Message = {
		sender: string;
		receiver: string;
		content: string;
	};

	let messages = writable<Message[]>([]);
	let newMessage = '';
	
	let ws;
	
	onMount(() => {
		const token = localStorage.getItem('access_token');

		ws = new WebSocket(`/ws/chat/${friend.username}/?token=${token}`);

		fetchMessages();

		ws.onmessage = (event) => {
		const data = JSON.parse(event.data);
		messages.update((msgs) => [...msgs, data]);
		};
	});
	
	const fetchMessages = async () => {
		const { accessToken } = get(auth);
		const response = await fetch(`/api/messages/${friend.username}/`, {
		headers: {
			'Authorization': `Bearer ${accessToken}`,
		}
		});
		const data = await response.json();
		messages.set(data.map((msg: any) => ({
			sender: msg.sender,
			receiver: msg.receiver,
			content: msg.content,
		})));
	};
	
	const sendMessage = () => {
		if (newMessage.trim() !== '') {
			ws.send(JSON.stringify({ message: newMessage }));
			newMessage = '';
		}
	};
</script>

<style>
	.chat-box {
		height: 80vh;
		overflow-y: scroll;
		border: 1px solid #ddd;
	}
	.chat-message {
		margin: 10px;
	}
	.chat-message.sent {
		text-align: right;
	}
</style>

<div class="chat-box">
	{#each $messages as message}
		<div class="chat-message {message.sender === $auth.user?.username ? 'sent' : 'received'}">
			<p style="color: white;">{message?.sender}: {message?.content}</p>
		</div>
	{/each}
	</div>
	
	<div class="chat-input">
	<input
		type="text"
		bind:value={newMessage}
		class="form-control"
		placeholder="Type a message..."
	/>
	<button on:click={sendMessage} class="btn btn-primary">Send</button>
</div>
