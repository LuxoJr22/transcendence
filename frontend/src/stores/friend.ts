import { get } from 'svelte/store';
import { auth } from './auth';

export async function fetchFriends(): Promise<void> {
	const { accessToken } = get(auth);

	if (!accessToken)
		return;

	const response = await fetch('/api/friends/', {
		method: 'GET',
		headers: { 'Authorization': `Bearer ${accessToken}` },
	});

	if (response.ok) {
		const data = await response.json();
		auth.update(state => ({
			...state,
			friends: data,
		}));
	} else {
		const data = await response.json();
		console.error(data);
	}
}
