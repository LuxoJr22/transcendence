<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import Pie from './pie.svelte';

    const img = new URL('$lib/assets/sforesti.jpg', import.meta.url).href;
    import { auth, fetchUser, logout, updateInformations} from '../../stores/auth';
    import type { AuthState } from '../../stores/auth';

    let victories = 15;
    let defeats = 3;

    let valueToEdit = false;
    let newDisplayName = ''; let newEmail = '';
	let state: AuthState;
	$: $auth, state = $auth;

    auth.subscribe((value : AuthState) =>{
        state = value
    });

	onMount(async () => {
		if (localStorage.getItem('access_token')) {
			await fetchUser();
		}
	});
    
    function changeValueEditStatus() {
        valueToEdit = true;
    }

    async function updateUserValue(){
        const data = await updateInformations((newEmail == '' ? state.user?.email : newEmail), (newDisplayName == '' ? state.user?.displayName : newDisplayName));
        valueToEdit = false;
        newEmail = '';
        newDisplayName = '';
    }
</script>

<style>
    ul {
        list-style-type: none;
    }
    .responsive-img {
        object-fit: cover;
        width: 40vh;

        height: 40vh;
    }
</style>

<div class="container border rounded my-3" width="80vw" height="80vh">
    <div class="row py-3">
        <div class="col-3 d-flex align-items-center justify-content-center ms-2">
            <img src={img} class="img-fluid rounded-circle responsive-img">
        </div>
            {#if !valueToEdit}
            <div class="col-3 p-0 text-light d-flex align-items-center justify-content-center border-start border-end ms-5">
                <ul class="m-0 p-0">
                    <li class="py-2"><i class="bi bi-eye-fill pe-2" style="font-size: 1.2rem; color:grey"></i>{state.user?.displayName}</li>
                    <li class="py-2"><i class="bi bi-at pe-2" style="font-size: 1.2rem; color:grey"></i>{state.user?.email}</li>
                    <li class="d-flex flex-row-reverse mt-3"><button on:click={changeValueEditStatus} type="button" class="btn btn-light"><i class="bi bi-pencil" style="font-size:1rem; color:grey;"></i></button></li>
                    
                </ul>
            </div>
            {:else if valueToEdit}
            <div class="col-3 p-0 text-light d-flex align-items-center border-start border-end ms-5">
                <form on:submit|preventDefault="{updateUserValue}">
                    <ul>
                        <li class="py-2 pe-4"><input bind:value={newDisplayName} type="text" class="form-control" placeholder="Display name" aria-label="Display name"></li>
                        <li class="py-2 pe-4"><input bind:value={newEmail} type="text" class="form-control" placeholder="Email" aria-label="Email"></li>
                        <li class="py-2 ps-3"><button on:click={changeValueEditStatus} type="submit" class="btn btn-light"><i class="bi bi-check-lg pe-2" style="font-size:1rem; color: var(--bs-success);"></i>Confirm</button></li>
                    </ul>            
                </form>
            </div>
            {/if}
            <Pie {victories} {defeats}/>
    </div>
</div>