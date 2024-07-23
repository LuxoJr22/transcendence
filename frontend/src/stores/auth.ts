import { user, isAuthenticated } from "./user";

export function login(access_token: string, refresh_token: string, user_data: any) {
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('user_data', JSON.stringify(user_data));
    user.set(user_data);
    isAuthenticated.set(true);
}

export function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
    user.set(null);
    isAuthenticated.set(false);
}

export function getAccessToken(): string | null {
    return localStorage.getItem('access_token');
}

export function getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
}
