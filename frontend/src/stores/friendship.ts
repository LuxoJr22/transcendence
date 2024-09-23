import { writable, get } from 'svelte/store';
import { auth } from './auth';

interface requestsList {
    requester : {id: number, username: string, profile_picture: string};
    receiver : {id: number, username: string, profile_picture: string};
    status: boolean;
    date: string;
}

export const friendRequestsList = writable<requestsList>([]);

export async function fetchFriendList(){
    const { accessToken } = get(auth);

    if (!accessToken)
        return;

    const response = await fetch('/api/friends/', {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${accessToken}` },
    });

    if (response.ok){

        
        const data = await response.json();
        friendList = data;
        console.log(data);
    }
}