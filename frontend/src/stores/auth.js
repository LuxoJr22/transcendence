import { writable } from 'svelte/store';

export const isAuth = writable(false);

export function checkAuth() {
	const token = localStorage.getItem('access_token');
	
	if (token) {
		isAuth.set(true);
	} else {
		isAuth.set(false);
	}
}
