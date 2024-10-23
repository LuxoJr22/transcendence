import { writable } from 'svelte/store';

export interface User {
    id: number;
    username: string;
    email: string;
    profile_picture: string;
    is_2fa_enabled : boolean;
    skin: string;
}

export interface AuthState {
    isAuthenticated: boolean;
    user: User | null;
    accessToken: string
    refreshToken: string
}

const initialState: AuthState = {
    isAuthenticated: false,
    user: null,
    accessToken: '',
    refreshToken: '',
};

export const auth = writable<AuthState>(initialState);

export async function login(username: string, password: string): Promise<any> {
    const response = await fetch('/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (data.is_2fa_enabled){
        return ('2fa');
    }
    if (response.ok) {
        auth.set({
            isAuthenticated: true,
            user: {
                id: data.user.id,
                username: data.user.username,
                email: data.user.email,
                profile_picture: data.user.profile_picture_url,
                is_2fa_enabled : data.is_2fa_enabled
            },
            accessToken: data.access,
            refreshToken: data.refresh
        });
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        return ('success');
    } else {
        return (data);
    }
}

export async function login42(){
    let code = new URLSearchParams(window.location.search).get('code');
    let data = null;
    let response;
    if (code && code != ''){
        response = await fetch('/api/oauth42/callback/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code }),
        });

        data = await response.json();
        if (data.is_2fa_enabled){
            return (data);
        }
    }

    if (response && response.ok){
        auth.set({
            isAuthenticated: true,
            user: {
                id: data.user.id,
                username: data.user.username,
                email: data.user.email,
                profile_picture: data.user.profile_picture_url,
                is_2fa_enabled : data.is_2fa_enabled
            },
            accessToken: data.access,
            refreshToken: data.refresh
        });
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        return ('success');
    }
    else {
        return (data);
    }
}

export async function loginWithTwoFA(username: string, password: string, otp_code : string){
    const response = await fetch('/api/2fa/verify/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, otp_code }),
    });

    const data = await response.json();
    if (response.ok) {
        auth.set({
            isAuthenticated: true,
            user: {
                id: data.user.id,
                username: data.user.username,
                email: data.user.email,
                profile_picture: data.user.profile_picture_url,
                is_2fa_enabled : data.is_2fa_enabled
            },
            accessToken: data.access,
            refreshToken: data.refresh
        });
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        return ('success');
    } else {
        return (data);
    }
}

export async function updateUsername(username: string): Promise<any> {
    const accessToken = await getAccessToken();

    const response = await fetch('/api/user/update/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json',  'Authorization': `Bearer ${accessToken}` },
        body: JSON.stringify({ username }),
    });
    const data = await response.json();

    if (response.ok) {
        await fetchUser();
        return ;
    } else {
        return (data);
    }
}

export async function updateEmail(email: string): Promise<any> {
    const accessToken = await getAccessToken();

    const response = await fetch('/api/user/update/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json',  'Authorization': `Bearer ${accessToken}` },
        body: JSON.stringify({ email }),
    });
    const data = await response.json();

    if (response.ok) {
        await fetchUser();
        return ;
    } else {
        return (data);
    }
}

export async function updatePassword(password: string, current_password: string): Promise<any> {
    const accessToken = await getAccessToken();
    if (!accessToken)
        throw new Error('Username update failed');
    const response = await fetch('/api/user/update/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json',  'Authorization': `Bearer ${accessToken}` },
        body: JSON.stringify({ password, current_password }),
    });
   
    const data = await response.json();

    if (response.ok) {
        await fetchUser();
        return ('success');
    } else {
        return (data);
    }
}


export async function updateProfilePicture(profile_picture: File) {
    const accessToken = await getAccessToken();
    if (!accessToken) {
        throw new Error('Username update failed');
    }
    
    const formData = new FormData();
    formData.append('profile_picture', profile_picture);
    const response = await fetch('/api/user/update/', {
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
        },
        body: formData,
    });

    const data = await response.json();

    if (response.ok) {
        await fetchUser();
        return ('success');
    }
    else {
        return (data);
    }
}

export async function fetchUser(): Promise<any> {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
        logout();
        return;
    }

    const response = await fetch('/api/user/', {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${accessToken}` },
    });

    if (response.ok) {
        const user = await response.json();
        auth.update((state : any) => ({
            ...state,
            isAuthenticated: true,
            user: {
                id: user.id,
                username: user.username,
                email: user.email,
                profile_picture: user.profile_picture,
                is_2fa_enabled: user.is_2fa_enabled,
                skin: user.skin,
            },
            accessToken: localStorage.getItem('access_token'),
            refreshToken: localStorage.getItem('refresh_token')
        }));
        return ('success');
    }
    else if (response.status == 401){
        localStorage.setItem('access_token', '');
    }
}

function AccessTokenExpirated(){
    let token : string | null;
    let refresh_token : string | null;
    token = localStorage.getItem('access_token')
    refresh_token = localStorage.getItem('refresh_token')
    if (token == null || token == '')
        return (true);
    let content : string = token.split('.')[1].replaceAll('-', '+').replaceAll('_', '/');
    let expiration = window.atob(content);
    return ((JSON.parse(expiration).exp - 5) <= (Math.floor(Date.now() / 1000)));
}

export async function getAccessToken(){
    await fetchUser();
    await refresh_token();
    return (localStorage.getItem('access_token'));
}

export async function refresh_token(): Promise<any> {
    if (!AccessTokenExpirated())
        return ;
    let refreshToken = localStorage.getItem('refresh_token')
    if (refreshToken == null || refreshToken == ''){
        logout();
        return ;
    }
    const response = await fetch('/api/token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken }),
    });

    if (response.ok && refreshToken != null) {
        const data = await response.json();
        auth.update((state : any) => ({
            ...state,
            accessToken: data.access,
        }));
        localStorage.setItem('access_token', data.access);
        return (data.access);
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