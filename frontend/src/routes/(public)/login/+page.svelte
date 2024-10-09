<script lang="ts">;
    import { goto } from '$app/navigation';
    import { login , login42, auth} from '$lib/stores/auth';
    import type { AuthState } from '$lib/stores/auth'
    import { onMount } from 'svelte';

    let username = '';
    let password = '';
    let errorsLogin = false;

    function resetLoginErrors(){
        errorsLogin = false;
    }

    async function handleLogin() {
        const response = await login(username, password);
        if (localStorage.getItem('access_token'))
            goto('/');
        else
            errorsLogin = true;
    }

    onMount(async () => {
        const status = await login42();
        if (status == 'success'){
            window.location.href= '/';
        }
    })

    let viewablePassword = false;

    function viewPassword(){
        viewablePassword ? viewablePassword = false : viewablePassword = true;
    }

    const logo42 = new URL('$lib/assets/42_Logo.svg', import.meta.url).href
</script>

<div class="container-fluid" style="height:100vh;">
    <div class="d-flex justify-content-center align-items-center" style="height:100%;">
        <form on:submit|preventDefault="{handleLogin}" class="p-5 border rounded">
            <div class="mb-3">
                <label for="Pseudo" class="form-label text-light container-fluid">
                    <h5>Pseudo</h5>
                    <input type="text" bind:value="{username}" class="form-control" id="Pseudo" placeholder="Enter pseudo">
                </label>
            </div>
            <div class="mb-3">
                <label for="Password" class="form-label text-light container-fluid">
                    <h5>Password</h5>
                    {#if !viewablePassword}
                        <div class="d-flex">
                            <input type="password" bind:value="{password}" required class="form-control col-12" placeholder="Enter password">
                            <a class="mt-1 ms-2 hover-effect" type="button" on:click={viewPassword}><i class="bi bi-eye" style="color:grey;"></i></a>
                        </div>
                    {:else}
                        <div class="d-flex">
                            <input type="text" bind:value="{password}" required class="form-control col-12" placeholder="Enter password">
                            <a class="mt-1 ms-2 hover-effect" type="button" on:click={viewPassword} ><i class="bi bi-eye-slash" style="color:grey;"></i></a>
                        </div>
                    {/if}
                </label>
            </div>
            {#if errorsLogin == true}
            <div class="alert alert-danger mx-3" role="alert">
                Username or password incorrect.
            </div>
            {/if}
            <div>
                <p class="text-light">Don't have an account? <a href="/register">Register now</a></p>
            </div>
            <div class="btn-group-vertical col-12" role="group" aria-label="Vertical button group">
                <button type="submit" class="m-1 btn btn-primary" on:click={resetLoginErrors}>Login</button>
                <a href="api/oauth42/" type="button" class="m-1 btn btn-light">Login with <img src={logo42} alt="42 school logo" class="ms-1" style="height:1.5rem;"/></a>
            </div>
        </form>
    </div>
</div>