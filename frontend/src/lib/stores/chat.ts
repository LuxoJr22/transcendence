import { writable } from 'svelte/store';
import { refresh_token } from './auth';

interface Messages {
    sender: string;
    receiver: string;
    content: string;
}

export let messages = writable<Messages[]>([]);

export async function fetchChatMessages(id: number){
    await refresh_token();
    const accessToken = localStorage.getItem('access_token');;
    const response = await fetch('/api/messages/' + id + '/', {
    headers: {
        'Authorization': `Bearer ${accessToken}`,
    }
    });
    const data = await response.json();
    messages.set(data);
};

export async function updateMessages(messageChat : any){
    messages.update((msg : Messages[]) => [...msg, messageChat]);
}
