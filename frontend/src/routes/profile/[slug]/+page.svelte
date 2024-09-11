<script lang='ts'>
    import { onMount } from 'svelte';

    const img = new URL('$lib/assets/sforesti.jpg', import.meta.url).href;
    import { auth, fetchUser } from '../../../stores/auth';
    import type { AuthState } from '../../../stores/auth';
    import SelfUser from './../selfUser.svelte';
    import type { Profile } from '../../../stores/user';
    import { profileData, profile } from '../../../stores/user';
    import OtherUser from '../otherUser.svelte';

    let victories = 15;
    let defeats = 3;
    let games = [];
    
    let currentUrl : string = window.location.href;
    let currentUser = currentUrl.substring(currentUrl.lastIndexOf('/') + 1);

    let state: AuthState;
    $: state = $auth;

    let user : Profile;
    $: user = $profile;
    
    onMount(async () => {
        if (localStorage.getItem('access_token')) {
            await fetchUser();
        }
        let token = localStorage.getItem('access_token');
        if (token)
            await profileData(currentUser, token);
        auth.subscribe((value : AuthState) =>{
            state = value
        });
        profile.subscribe((value : Profile) =>{
            user = value;
        });
        console.log(state.user?.profile_picture);
        console.log(user?.profile_picture);
    });

</script>

{#if currentUser == state.user?.username}
    <SelfUser />
{:else if user?.username == currentUser}
    <OtherUser />
{:else}
    <div class="col-12 h-100 d-flex justify-content-center" style="color:grey;">
        <h2 class='p-5'>Error<br>Profile not found</h2>
    </div>
{/if}
