<script lang='ts'>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { auth, fetchUser } from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth';
    import SelfUser from '$lib/static/Profile/selfUser.svelte';
    import type { Profile } from '$lib/stores/user';
    import { profileData, profile } from '$lib/stores/user';
    import OtherUser from '$lib/static/Profile/otherUser.svelte';

    $: currentUser = $page.params.id;

    $: {
        fetchUser();
        profileData(parseInt(currentUser));
    }

    let state: AuthState;
    $: state = $auth;

    let user : Profile;
    $: user = $profile;

    onMount(async () => {
        await profileData(parseInt(currentUser));
        await fetchUser();
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
    <OtherUser userId={currentUser} />
{:else}
    <div class="col-12 h-100 d-flex justify-content-center" style="color:grey;">
        <h2 class='p-5'>Error<br>Profile not found</h2>
    </div>
{/if}
