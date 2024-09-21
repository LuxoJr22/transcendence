import { writable, get } from 'svelte/store';
import { auth } from './auth';

interface requestsList {
    requester : {id: number, username: string, profile_picture: string};
    receiver : {id: number, username: string, profile_picture: string};
    status: boolean;
    date: string;
}

export const friendRequestsList = writable<requestsList>([]);

async function fetchFriendRequests(){

    const { accessToken } = get(auth);

	if (!accessToken)
		return;

	const response = await fetch('/api/requests/', {
		method: 'GET',
		headers: { 'Authorization': `Bearer ${accessToken}` },
	});
    
    if (response.ok){
        const data = await response.json();
        
    }
}