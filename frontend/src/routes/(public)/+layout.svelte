<script lang="ts">
    import { auth, fetchUser, logout } from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation'

    let state: AuthState;
	$: $auth, state = $auth;

    onMount (async () => {
        await fetchUser();
        auth.subscribe((value : AuthState) =>{
            state = value;
        });
        if (state.accessToken != null)
            goto('/');
    })
</script>

<div>
    <slot />
</div>