<script lang="ts">
    import { onMount } from 'svelte';
    import {get} from 'svelte/store';
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

    /******************Friendship********************/
    let requestsList = '' ;
    async function fetchFriendRequests(){
        const { accessToken } = get(auth);

        if (!accessToken)
            return;

        const response = await fetch('/api/requests/', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${accessToken}` },
        });

        if (response.ok){
            const data = await response.json();
            requestsList = data;
        }
    }
    
    async function declineFriendRequest(id: number){
        const { accessToken } = get(auth);

        if (!accessToken)
            return;

        const response = await fetch('/api/reject/' + id + '/', {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${accessToken}` },
        });

        if (response.ok)
        {
            const data = await response.json();
            console.log(data);
        }
    }
    
    async function acceptFriendRequest(id: number){
        const { accessToken } = get(auth);

        if (!accessToken)
            return;

        const response = await fetch('/api/accept/' + id + '/', {
            method: 'PATCH',
            headers: { 'Authorization': `Bearer ${accessToken}` },
        });

        const data = await response.json();
        console.log(data);

        if (response.ok)
        {
            const data = await response.json();
            console.log(data);
        }
    }

</script>

<nav class="navbar">
    <div class="container-fluid">
        <a href="/" class="navbar-item navbar-brand fs-1 layout-title text-warning-subtle ms-4 opacity">t r i p l u m</a>
        {#if state.isAuthenticated}
        <div class="row">
            <div class="dropdown col-3">
                <a class="btn" style="text-decoration:none; color:white;" type="button" data-bs-toggle="dropdown" aria-expanded="false" on:click={fetchFriendRequests}>
                <i class="bi bi-bell"></i>
                </a>
                <ul class="dropdown-menu dropdown-menu-end">
                {#each requestsList as request, i}
                    {#if request.receiver.id == state.user?.id}
                    <div class="d-flex align-items-center p-2 m-2 mt-1 border rounded">
                        <p class="dropdown-item mb-0" style="">{request.requester.username} sent you a friend request</p>
                        <a href="#" class="" style="" on:click={() => acceptFriendRequest(request.id)}>
                            <i class="bi bi-person-check-fill p-2" style="color:green; font-size:1.3rem;"></i>
                        </a>
                        <a href="#" class="" style="" on:click={() => declineFriendRequest(request.id)}>
                            <i class="bi bi-person-fill-x p-2" style="color:red; font-size:1.3rem;"></i>
                        </a>
                    </div>
                    {/if}
                {/each}
                {#if !requestsList[0]}
                <div class="d-flex justify-content-center">
                    <p class="mt-2"style="color:grey;">No notifications</p>              
                </div>
                {/if}
                </ul>
            </div>
            <div class="dropdown col-4">
                <a href="/" class="navbar-item navbar-brand text-primary-subtle opacity dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    <img src={state.user?.profile_picture} alt="User profile" class="border rounded-circle mb-1 me-1 responsive-img" width="30" height="30">{state.user?.username}
                </a>
                <ul class="dropdown-menu ms-3" style="min-width: 0;">
                    <li><a class="dropdown-item text-start py-1 px-4" href={"/profile/" + state.user?.id}><i class="bi-person-fill pe-2" style="font-size: 1.3rem; color: grey;"></i>profile</a></li>
                    <li><a class="dropdown-item text-danger text-start py-1 px-4" href="/" on:click={handleLogout}><i class="bi-box-arrow-right pe-2" style="font-size: 1.3rem; color: red;"></i>logout</a></li>
                </ul>
            </div>
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

</style>