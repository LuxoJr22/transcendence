import { writable } from 'svelte/store'

export const user = writable(null);

export async function fetchUserData() {
    const token = localStorage.getItem('access_token');
    
    if (token) {
        try {
            const response = await fetch('/api/user/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                user.set(data);
            } else {
                console.error('Failed to fetch user data');
            }
        } catch (error) {
            console.error('Error fetching user data:', error);
        }
    }
}
