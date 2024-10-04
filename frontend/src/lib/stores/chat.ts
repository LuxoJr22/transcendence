import { writable } from 'svelte/store';
import { refresh_token } from './auth';

interface Messages {
    sender: string;
    receiver: string;
    content: string;
    is_invitation: boolean;
    gamemode: string | null;
    match_id: number | null;
}

interface History{
    id: number;
    is_online: boolean;
    content: string;
    last_message:{
        sender: number;
        timestamp: string;
    }
    profile_picture_url: string;
    username: string;
}

export let messages = writable<Messages[]>([]);
export let history = writable<History[]>([]);

export async function fetchChatMessages(id: number){
    const accessToken = localStorage.getItem('access_token');;
    const response = await fetch('/api/chat/messages/' + id + '/', {
    headers: {
        'Authorization': `Bearer ${accessToken}`,
    }
    });
    const data = await response.json();
    console.log(data);
    messages.set(data);
};

export async function fetchLatestDiscussion(){
    refresh_token();
    const accessToken = localStorage.getItem('access_token');
    const response = await fetch('/api/chat/history/', {
    headers: {
        'Authorization': `Bearer ${accessToken}`,
    }
    });
    if (response.ok){
        const data = await response.json();
        history.set(data);
    }
};

export async function updateMessages(messageChat : any){
    messages.update((msg : Messages[]) => [...msg, messageChat]);
}