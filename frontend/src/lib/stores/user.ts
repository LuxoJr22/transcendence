import { writable } from 'svelte/store';
import { refresh_token } from './auth';

export interface Profile {
   id: number;
   username: string;
   profile_picture: string;
   is_online:  boolean;
   skin: string
}

export const profile = writable<Profile>();

export async function profileData(id: number): Promise<void> {
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
         profile_picture: profileData.profile_picture_url,
         is_online: profileData.is_online,
         skin: profileData.skin
      });
   } else {
      console.error('Failed to fetch profile data:');
   }
}

export async function userData(id: number): Promise<void> {
   let accessToken = localStorage.getItem('access_token');

   const response = await fetch('/api/user/profile/' + id.toString() + '/', {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${accessToken}` },
   });
   
   if (response.ok) {
      const profileData = await response.json();
      return (profileData);
   } else {
      console.error('Failed to fetch profile data:');
   }
}