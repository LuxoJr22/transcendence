<script lang='ts'>
    import { onMount } from 'svelte';
    import { auth } from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth';
    import SelfUser from './../selfUser.svelte';
    import type { Profile } from '$lib/stores/user';
    import { profileData, profile } from '$lib/stores/user';
    import OtherUser from '../otherUser.svelte';

    let victories = 15;
    let defeats = 3;
    let games = [];
    
    let currentUrl : string = window.location.href;
    let currentUser :string = currentUrl.substring(currentUrl.lastIndexOf('/') + 1);

    let state: AuthState;
    $: state = $auth;

    let user : Profile;
    $: user = $profile;
    
    auth.subscribe((value : AuthState) =>{
        state = value
    });

    onMount(async () => {
        await profileData(parseInt(currentUser));
        auth.subscribe((value : AuthState) =>{
            state = value
        });
        profile.subscribe((value : Profile) =>{
            user = value;
        });
    });

</script>

{#if parseInt(currentUser) == state.user?.id}
    <SelfUser />
{:else if user?.id == parseInt(currentUser)}
    <OtherUser />
{:else}
    <div class="col-12 h-100 d-flex justify-content-center" style="color:grey;">
        <h2 class='p-5'>Error<br>Profile not found</h2>
    </div>
{/if}
