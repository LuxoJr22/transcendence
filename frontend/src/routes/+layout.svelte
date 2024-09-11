<script lang="ts">
    import { onMount } from 'svelte';
    import { auth, fetchUser, logout } from '../stores/auth';
    import type { AuthState } from '../stores/auth';

	let state: AuthState;
	$: $auth, state = $auth;

	onMount(async () => {
		if (localStorage.getItem('access_token')) {
			await fetchUser();
		}
		auth.subscribe((value : AuthState) =>{
        state = value
    });
	});

	const handleLogout = () => {
		logout();
	};
</script>

<nav class="navbar">
    <div class="container-fluid">
        <a href="/" class="navbar-item navbar-brand fs-1 layout-title text-warning-subtle ms-4 opacity">t r i p l u m</a>
        {#if state.isAuthenticated}
            <div class="dropdown">
                <a href="/" class="navbar-item navbar-brand text-primary-subtle opacity dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    <img src={state.user?.profile_picture} alt="User profile" class="border border rounded-circle mb-1 me-1 responsive-img" width="30" height="30">{state.user?.username}
                </a>
                <ul class="dropdown-menu" style="min-width: 0;">
                    <li><a class="dropdown-item text-start py-1 px-4" href={"/profile/" + state.user?.username}><i class="bi-person-fill pe-2" style="font-size: 1.3rem; color: grey;"></i>profile</a></li>
                    <li><a class="dropdown-item text-danger text-start py-1 px-4" href="/" on:click={handleLogout}><i class="bi-box-arrow-right pe-2" style="font-size: 1.3rem; color: red;"></i>logout</a></li>
                </ul>
            </div>
        {:else}
            <a href="/login" class="btn btn-light mb-4" >Login</a>
        {/if}
    </div>
</nav>

<slot />

<!-- <footer class="bg-secondary fixed-bottom text-center">
    <p class="text-center">Final project of 42 school's common core, Transcendence, by <a href="https://github.com/LuxoJr22/transcendence" target="_blank" class="text-light">Triplum</a></p>
</footer> -->


<style>
    .layout-title {
        font-family: "Nabla", sans-serif;
    }

    .opacity:hover {
        opacity: 0.5;
    }
/* 
    :global(body) {
        background-color: var(--bs-dark);
    } */
    .text-warning-subtle {
        color: var(--bs-warning-bg-subtle);
    }

    .text-primary-subtle {
        color: var(--bs-primary-bg-subtle);
    }

    .responsive-img {
        object-fit: cover;
    }

    .dropdown-menu-addon {
        position: fixed;
        right: 0;
        top: auto;
        transform: translateX(-100%);
    }

</style>