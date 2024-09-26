import { writable, get } from 'svelte/store';
import { auth } from './auth';

interface Messages {
    sender: string;
    receiver: string;
    content: string;
}

export let messages = writable<Messages[]>([]);

export async function fetchChatMessages(id: number){
    const { accessToken } = get(auth);
    const response = await fetch('/api/messages/' + id + '/', {
    headers: {
        'Authorization': `Bearer ${accessToken}`,
    }
    });
    const data = await response.json();
    console.log(data);
    messages.set(data);
};

export async function updateMessages(messageChat : any){
    messages.update((msg : Messages[]) => [...msg, messageChat]);
}
