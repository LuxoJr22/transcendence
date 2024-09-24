import { writable, get } from 'svelte/store';
import { auth } from './auth';

export interface friendInterface {
    id: number;
    username: string;
    profile_picture: string;
}

export let friendList = writable<friendInterface>([]);

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
        friendList.set(data);
        return data;
    }
}

export async function declineFriendRequest(id: number){
    const { accessToken } = get(auth);

    if (!accessToken)
        return;

    const response = await fetch('/api/reject/' + id + '/', {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${accessToken}` },
    });

    if (response.ok)
    {
        const data = await response.json();
        console.log(data);
    }
}

export async function acceptFriendRequest(id: number){
    const { accessToken } = get(auth);

    if (!accessToken)
        return;

    const response = await fetch('/api/accept/' + id + '/', {
        method: 'PATCH',
        headers: { 'Authorization': `Bearer ${accessToken}` },
    });

    if (response.ok) {
        const newFriend = await response.json();
        friendList.update((currentList : friendInterface[]) => [...currentList, newFriend]);
        await fetchFriendList();
    }
}

export async function deleteFriend(id: number){
    const { accessToken } = get(auth);

    if (!accessToken)
        return;

    const response = await fetch('/api/remove/' + id + '/', {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${accessToken}` },
    });

    if (response.ok) {
        await fetchFriendList();
    }
}