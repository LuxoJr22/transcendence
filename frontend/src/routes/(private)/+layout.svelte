<script lang='ts' >
    import { afterNavigate , goto } from '$app/navigation';
    import { onDestroy, onMount } from 'svelte';
    import {get} from 'svelte/store';
    import { auth, fetchUser, logout , refresh_token } from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth';
    import { acceptFriendRequest, declineFriendRequest } from '$lib/stores/friendship'
    import { fetchLatestDiscussion, messages } from '$lib/stores/chat';
    import { profileData } from '$lib/stores/user';

    interface Notifications{
        type: String;
        message: String;
        date: number;
    }

    let notifications = new Array<Notifications>();

	let state: AuthState;
	$: $auth, state = $auth;

    function parseNotifications(data : any){
        notifications = notifications.filter(notif => Date.now() - notif.date < 5001);
        
        let tmp : Notifications = {
            type : data.type,
            message: data.message,
            date: Date.now()
        };
        notifications.unshift(tmp);
    }

	afterNavigate(async () => {
        const status = await fetchUser();
		auth.subscribe((value : AuthState) =>{
            state = value;
        });
		let token = localStorage.getItem('access_token');
        if (!token || token === '')
            window.location.href = '/login';
	});

    let wsOnline : WebSocket;
    onMount( async () => {
        await fetchUser();
        if (state.accessToken != null)
            wsOnline = new WebSocket('/ws/status/?token=' + localStorage.getItem('access_token'));
        
        wsOnline.onmessage = async function (event) {
        parseNotifications(JSON.parse(event.data));
        await fetchLatestDiscussion();
        if (window.location.href.search('/chat/') == -1){
            const toastElList = document.querySelectorAll('.toast')
            const toastList = [...toastElList].map(toastEl => new bootstrap.Toast(toastEl, {
                animation: true,
                autohide: true,
                delay: 5000
            }))
            toastList.forEach(toast => toast.show());
        }
    }
    });

    onDestroy(() =>{
        if (wsOnline.readyState == 1){
            wsOnline.close(0);
        }
    });

	async function handleLogout() {
		logout();
        window.location.href = '/login';
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

</script>

<nav class="navbar">
    <div class="container-fluid container-size">
        <a href="/" class="navbar-item navbar-brand fs-1 layout-title text-warning-subtle ms-4 opacity">t r i p l u m</a>
        {#if state.isAuthenticated}
        <div class="row">
            <div class="dropdown col-3">
                <button class="btn" style="text-decoration:none; color:white;" type="button" data-bs-toggle="dropdown" aria-expanded="false" on:click={fetchFriendRequests}>
                <i class="bi bi-bell"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-end">
                {#each requestsList as request, i}
                    {#if request.receiver.id == state.user?.id}
                    <div class="d-flex align-items-center p-2 m-2 mt-1 border rounded">
                        <p class="dropdown-item mb-0" style="">{request.requester.username} sent you a friend request</p>
                        <button class="btn p-0 m-0" style="" on:click={() => acceptFriendRequest(request.id)}>
                            <i class="bi bi-person-check-fill p-2" style="color:green; font-size:1.3rem;"></i>
                        </button>
                        <button class="btn p-0 m-0" on:click={() => declineFriendRequest(request.id)}>
                            <i class="bi bi-person-fill-x p-2" style="color:red; font-size:1.3rem;"></i>
                        </button>
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
                <ul class="dropdown-menu ms-2" style="min-width: 0;">
                    <li class="border border-2 rounded m-2 button-dropdown"><a class="dropdown-item text-start py-1 px-4" href="/chat/home/"><i class="bi-chat pe-2" style="font-size: 1.3rem; color: grey;"></i>chat</a></li>
                    <li class="border border-2 rounded m-2 button-dropdown"><a class="dropdown-item text-start py-1 px-4" href={"/profile/" + state.user?.id}><i class="bi-person-fill pe-2" style="font-size: 1.3rem; color: grey;"></i>profile</a></li>
                    <li class="border border-2 rounded m-2 button-dropdown"><a class="dropdown-item text-danger text-start py-1 px-4" href="/" on:click={handleLogout}><i class="bi-box-arrow-right pe-2" style="font-size: 1.3rem; color: red;"></i>logout</a></li>
                </ul>
            </div>
        </div>
        {:else}
            <a href="/login" class="btn btn-light mb-4" >Login</a>
        {/if}
    </div>
</nav>

<slot />


<div id="toast" class="toast-container position-fixed bottom-0 end-0 p-3">
    {#each notifications as notif}
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <strong class="me-auto">Notifications</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body text-truncate">
                {notif?.message}
            </div>
        </div>
    {/each}
</div>


<!-- <footer class="bg-secondary fixed-bottom text-center">
    <p class="text-center">Final project of 42 school's common core, Transcendence, by <a href="https://github.com/LuxoJr22/transcendence" target="_blank" class="text-light">Triplum</a></p>
</footer> -->


<style>

    .toast-container{
        height: 20%;
        overflow: auto;
        display: flex;
        flex-direction: column-reverse;
        scrollbar-width: thin;
        scrollbar-color: black grey;
    }

    .layout-title {
        font-family: "Nabla", sans-serif;
    }

    .opacity:hover {
        opacity: 0.5;
    }

    .text-warning-subtle {
        color: var(--bs-warning-bg-subtle);
    }

    .text-primary-subtle {
        color: var(--bs-primary-bg-subtle);
    }

    .responsive-img {
        object-fit: cover;
    }

    .container-size{
        width: 98%;
    }
    
    .button-dropdown{
        box-shadow: 1px 2px #a2a4a5;
    }

    @keyframes buttonPush {
        0% {
            box-shadow: 1px 2px #a2a4a5;
            transform:translateY(0);
        }
        100% {
            box-shadow: 2px 5px #a2a4a5;
            transform:translateY(-5px);
        }
    }

    .button-dropdown:hover{
        animation-name: buttonPush;
        animation-duration: 0.5s;
        animation-fill-mode: forwards;
    }

</style>