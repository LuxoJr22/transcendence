import { writable } from 'svelte/store';

interface User {
    id: number;
    username: string;
}

export const isAuthenticated = writable<boolean>(false);
export const user = writable<User | null>(null);

export function getUser() {
    const user_data = localStorage.getItem('user_data');
    if (user_data)
        user.set(JSON.parse(user_data));
}
