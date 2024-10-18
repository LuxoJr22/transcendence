<script lang='ts' >
    import { goto, afterNavigate } from '$app/navigation';
    import { onMount } from 'svelte';
    import {get} from 'svelte/store';
    import { auth, fetchUser, logout , refresh_token } from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth';
    import { acceptFriendRequest, declineFriendRequest } from '$lib/stores/friendship'
    import { fetchLatestDiscussion, messages } from '$lib/stores/chat';
    import Settings from '$lib/static/Profile/Settings.svelte';
    import { page } from '$app/stores'

    interface Notifications{
        type: string;
        message: string;
        date: number;
        tournament: string | null;
    }

    let keyBinds = [{up: 90, down: 83, left:81, right:68, charge:32}, {up: 90, down: 83, left:81, right:68, jump:32}]

    let notifications = new Array<Notifications>();
    let navBarNotifications = new Array<Notifications>();
    $: currentUrl = $page.url.pathname;
    let state: AuthState;
    $: $auth, state = $auth;

    function parseNotifications(data : any){
        notifications = notifications.filter(notif => Date.now() - notif.date < 5001);
        let tmp : Notifications = {
            type : data.type,
            message: data.message,
            date: Date.now(),
            tournament: data.type === 'tournament' ? data.tournament : null
        };
        notifications.unshift(tmp);
    }
    function addNotifications(data : any){
        navBarNotifications.push(data);
        return (navBarNotifications);
    }

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

    let wsOnline : WebSocket;
    onMount( async () => {
        await fetchUser();
        auth.subscribe((value : AuthState) =>{
            state = value;
        });
        if (state.accessToken != null)
            wsOnline = new WebSocket('/ws/status/?token=' + localStorage.getItem('access_token'));
        
        wsOnline.onmessage = async function (event) {
            parseNotifications(JSON.parse(event.data));
            console.log(JSON.parse(event.data));
            navBarNotifications = addNotifications(JSON.parse(event.data));
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

    function handleLogout() {
        if (wsOnline && wsOnline.readyState == WebSocket.OPEN)
            wsOnline.close(3000);
        logout();
        goto('/login');
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

    async function handleGoto(e : Event, path : string) {
        e.preventDefault();
        goto(path);
    }

    async function getKeyBinds(){
        const resp = await fetch('/api/pong/settings/' + state.user?.id + '/', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
        });
        const dat = await resp.json();
        if (resp.ok)
        {
            keyBinds[0] = dat.settings;
        }
        const resp1 = await fetch('/api/shooter/settings/' + state.user?.id + '/', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
        });
        const dat1 = await resp1.json();
        if (resp.ok){
            keyBinds[1] = dat1.settings;
        }
    }

</script>

 {#if $page.url.pathname != "/shooter"}
    <nav class="navbar">
        <div class="container-fluid container-size">
            <a href="/" class="navbar-item navbar-brand fs-1 layout-title text-warning-subtle ms-4 opacity">t r i p l u m</a>
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
                    {#each navBarNotifications as notif}
                        <div class="d-flex align-items-center p-2 m-2 mt-1 border rounded">
                            <p class="text-center">{ notif?.message }</p>
                        </div>
                    {/each}
                    {#if !requestsList[0] && !navBarNotifications[0]}
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
                        <li class="border border-2 rounded m-2 button-dropdown"><a class="dropdown-item text-start py-1 px-3" href='/chat/home'><i class="bi-chat pe-2" style="font-size: 1.3rem; color: grey;"></i>chat</a></li>
                        <li class="border border-2 rounded m-2 button-dropdown"><a class="dropdown-item text-start py-1 px-3" href={'/profile/' + state.user?.id}><i class="bi-person-fill pe-2" style="font-size: 1.3rem; color: grey;"></i>profile</a></li>
                        <li class="border border-2 rounded m-2 button-dropdown"><button class="dropdown-item text-start py-1 px-3" data-bs-toggle="modal" data-bs-target="#settingsModal" on:click={async () => await getKeyBinds()}><i class="bi bi-gear pe-2" style="font-size: 1.3rem; color: grey;"></i>settings</button></li>
                        <li class="border border-2 rounded m-2 button-dropdown"><a class="dropdown-item text-danger text-start py-1 px-3" href='/login' on:click={handleLogout}><i class="bi-box-arrow-right pe-2" style="font-size: 1.3rem; color: red;"></i>logout</a></li>
                    </ul>
                    <Settings state={state} twoFA_data={0} otp_code={''} keyBinds={keyBinds}/>
            </div>
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
                <div class="toast-body text-truncate" role="button" on:click={(event) => {
                    if (notif?.type === 'chat') {
                        handleGoto(event, '/chat/home');
                    } else if (notif?.type === 'tournament' && notif?.tournament) {
                        handleGoto(event, `/tournament/${notif?.tournament}/`);
                    }
                }}>
                    {notif?.message}
                </div>
            </div>
        {/each}
    </div>
{:else}
    <slot />
{/if}

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
        font-weight: 800;
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

    .dropdown {
        width: 30%;
    }

    .dropdown-item:active {
        background-color: transparent;
    }

</style>