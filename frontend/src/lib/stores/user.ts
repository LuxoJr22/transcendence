import { writable } from 'svelte/store';
import { refresh_token } from './auth';

export interface Profile {
   id: number;
   username: string;
   email: string;
   profile_picture: string;
}

export const profile = writable<Profile>();

export async function profileData(id: number): Promise<void> {
   await refresh_token()

   let accessToken = localStorage.getItem('access_token');

   const response = await fetch('/api/user/profile/' + id.toString() + '/', {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${accessToken}` },
   });
   
   if (response.ok) {
      const profileData = await response.json();
      profile.set({
         id: profileData.id,
         username: profileData.username,
         email: profileData.email,
         profile_picture: profileData.profile_picture_url,
      });
   } else {
      console.error('Failed to fetch profile data:');
   }
}