import { writable, get } from 'svelte/store';

export interface User { // AAAA
    id: number;
    username: string;
    email: string;
    profile_picture: string;
}

export interface AuthState {
    isAuthenticated: boolean;
    user: User | null;
	friends: User[]; // AAAA
    accessToken: string | null;
    refreshToken: string | null;
}

const getTokenFromLocalStorage = (key: string): string | null => {
    const token = localStorage.getItem(key);
    return token ? token : null;
};

const initialState: AuthState = {
    isAuthenticated: false,
    user: null,
    accessToken: getTokenFromLocalStorage('access_token'),
    refreshToken: getTokenFromLocalStorage('refresh_token'),
};

export const auth = writable<AuthState>(initialState);

export async function login(username: string, password: string): Promise<void> {
    const response = await fetch('/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    console.log(data);

    if (response.ok) {
        auth.set({
            isAuthenticated: true,
            user: {
                id: data.user.id,
                username: data.user.username,
                email: data.user.email,
                profile_picture: data.user.profile_picture_url,

            },
            accessToken: data.access,
            refreshToken: data.refresh,
        });

        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        return ('success');
    } else {
        return (data);
    }
}

export async function updateInformations(email: string, username: string): Promise<void> {
    const { accessToken } = get(auth);
    if (!accessToken) {
        throw new Error('Username update failed');
        return;
    }
    const response = await fetch('/api/user/update/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json',  'Authorization': `Bearer ${accessToken}` },
        body: JSON.stringify({ email, username }),
    });
    const data = await response.json();

    if (response.ok) {
        fetchUser();
        return ;
    } else {
        return (data);
    }
}

export async function updatePassword(password: string, current_password: string): Promise<void> {
    const { accessToken } = get(auth);
    if (!accessToken) {
        throw new Error('Username update failed');
        return;
    }
    const response = await fetch('/api/user/update/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json',  'Authorization': `Bearer ${accessToken}` },
        body: JSON.stringify({ password, current_password }),
    });
    
   
    const data = await response.json();

    if (response.ok) {
        fetchUser();
        return ('success');
    } else {
        return (data);
    }
}


export async function updateProfilePicture(profile_picture: File) {
    
    const { accessToken } = get(auth);
    if (!accessToken) {
        throw new Error('Username update failed');
        return;
    }
    
    const formData = new FormData();
    formData.append('profile_picture', profile_picture);
    const response = await fetch('/api/user/update/', {
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: formData,
    });

    const data = await response.json();

    if (response.ok) {
        fetchUser();
        return ('success');
    }
    else {
        return (data);
    }
}

export async function fetchUser(): Promise<void> {
    const { accessToken } = get(auth);

    if (!accessToken) {
        return;
    }

    const response = await fetch('/api/user/', {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${accessToken}` },
    });

    if (response.ok) {
        const user = await response.json();
        auth.update(state => ({
            ...state,
            isAuthenticated: true,
            user: {
                id: user.id,
                username: user.username,
                email: user.email,
                profile_picture: user.profile_picture,
            }
        }));
    } else if (response.status === 401) {
        await refresh_token();
    }
}

export async function refresh_token(): Promise<void> {
    const { refreshToken } = get(auth);

    const response = await fetch('/api/token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refresh_token }),
    });

    if (response.ok) {
        const data = await response.json();
        auth.update(state => ({
            ...state,
            access_token: data.access,
        }));

        localStorage.setItem('access_token', data.access);
    } else {
        logout();
    }
}

export function logout(): void {
    auth.set({
        isAuthenticated: false,
        user: null,
        accessToken: null,
        refreshToken: null,
    });

    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}
