import { writable } from 'svelte/store';

export interface Profile {
   id: number;
   username: string;
   email: string;
   profile_picture: string;
}

export const profile = writable<Profile>();

export async function profileData(id: string, token: string): Promise<void> {
   const response = await fetch('/api/user/profile/' + parseInt(id) + '/', {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${token}` },
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