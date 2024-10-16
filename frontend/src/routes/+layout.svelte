<script lang='ts'>
    import { page } from '$app/stores';
    import { goto, afterNavigate } from '$app/navigation'
    import { auth, logout, refresh_token } from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth';

    let state : AuthState;
    $: state,  state = $auth;

    $: currentUrl = $page.url.pathname;

    afterNavigate(async () => {
        let token = localStorage.getItem('access_token');
        if (currentUrl != '/login' && currentUrl != '/register' && !token){
            await refresh_token();
            let tmp = localStorage.getItem('access_token');
            if (!tmp){
                logout();
                goto('/login');
            }
        }
    })
</script>

<slot />