import { writable } from 'svelte/store';
import { getAccessToken } from './auth';

export interface friendInterface {
    id: number;
    username: string;
    profile_picture_url: string;
    is_online: boolean;
}

export let friendList = writable<friendInterface[]>([]);

export async function fetchFriendList(){
    const accessToken = await getAccessToken();

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
    const accessToken = await getAccessToken();

    if (!accessToken)
        return;

    const response = await fetch('/api/reject/' + id + '/', {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${accessToken}` },
    });

    if (response.ok)
    {
        const data = await response.json();
    }
}

export async function acceptFriendRequest(id: number){
    const accessToken = await getAccessToken();

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
    const accessToken = await getAccessToken();

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