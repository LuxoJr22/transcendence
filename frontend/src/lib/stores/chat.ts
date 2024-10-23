import { writable } from 'svelte/store';
import { getAccessToken, refresh_token } from './auth';

export interface Messages {
    sender: string;
    receiver: string;
    content: string;
    is_invitation: boolean;
    gamemode: string | null;
    match_id: string | null;
    is_over: boolean;
}

export interface History{
    id: number;
    is_online: boolean;
    content: string;
    last_message:{
        sender: number;
        timestamp: string;
        content: string;
    }
    profile_picture_url: string;
    username: string;
}

export let messages = writable<Messages[]>([]);
export let history = writable<History[]>([]);

async function checkPongMatch(match_id: string) {
    const token = await getAccessToken();
    const response = await fetch(`/api/pong/match/${match_id}`, {
        headers: {
            'Authorization': `Bearer ${token}`,
        }
    });
    const data = await response.json();
    return !(data.winner === null);
}

export async function fetchChatMessages(id: number){
    const accessToken = await getAccessToken();
    const response = await fetch('/api/chat/messages/' + id + '/', {
        headers: {
            'Authorization': `Bearer ${accessToken}`,
        }
    });
    const data = await response.json();
    if (data[0]){
        for (let message of data)
            if (message.is_invitation)
                message.is_over = await checkPongMatch(message.match_id);
        messages.set(data);
    }
};

export async function fetchLatestDiscussion(){
    const accessToken = await getAccessToken();
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
