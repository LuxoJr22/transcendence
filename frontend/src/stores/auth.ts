import { writable, get } from 'svelte/store';

interface User {
    id: number;
    username: string;
    displayName: string;
    email: string;
}

export interface AuthState {
    isAuthenticated: boolean;
    user: User | null;
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

    if (response.ok) {
        const data = await response.json();
        auth.set({
            isAuthenticated: true,
            user: {
                id: data.user.id,
                username: data.user.username,
                displayName: data.user.display_name,
                email: data.user.email,
            },
            accessToken: data.access,
            refreshToken: data.refresh,
        });

        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
    } else {
        throw new Error('Login failed');
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
                displayName: user.display_name,
                email: user.email,
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
