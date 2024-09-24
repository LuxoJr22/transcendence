import { writable, get } from 'svelte/store';
import { auth } from './auth';

interface Messages {
    sender: string;
    receiver: string;
    content: string;
}

export const messages = writable<Messages>([]);

export async function fetchChatMessages(username: string){
    const { accessToken } = get(auth);
    const response = await fetch('/api/messages/' + username + '/', {
    headers: {
        'Authorization': `Bearer ${accessToken}`,
    }
    });
    const data = await response.json();
    messages.set( (msg : Messages[]) => [...msg, data]);
};