<script lang="ts">;
    import { goto } from '$app/navigation';
    import { login , login42, loginWithTwoFA} from '$lib/stores/auth';
    import { onDestroy, onMount } from 'svelte';
    const logo42 = new URL('/assets/42_Logo.svg', import.meta.url).href

    let username = '';
    let password = '';
    let errorsLogin = false;
    let otp_code = '';
    let myModal : any = null;
    let errorTwoFA : any = ''
    let error42Login : any;
    let twoFaWith42 = false;

    function resetLoginErrors(){
        errorsLogin = false;
    }

    function displayModal(){
        var modalElement = document.getElementById('myModal');
        myModal = new bootstrap.Modal(modalElement);
        myModal.show()
    }

    async function handleLogin() {
        const response = await login(username, password);
        if (response == '2fa'){
            displayModal();
        }
        if (localStorage.getItem('access_token'))
            goto('/');
        else if (response != '2fa')
            errorsLogin = true;
    }

    onMount(async () => {
        const status = await login42();
        if (status?.is_2fa_enabled){
            displayModal();
            twoFaWith42 = true;
            username = status.username;
        }
        if (status == 'success'){
            goto('/');
        }
        else{
            goto('/login');
            error42Login = status?.error.replaceAll('[', '').replaceAll('\'', '').replaceAll(']', '');
        }
    })

    onDestroy(() => {
        if (myModal)
            myModal.hide();
    })

    async function handleTwoFA(){
        errorTwoFA = await loginWithTwoFA(username, password, otp_code);
        if (localStorage.getItem('access_token'))
            goto('/');
    }

    let viewablePassword = false;

    function viewPassword(){
        viewablePassword ? viewablePassword = false : viewablePassword = true;
    }
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
                        <div class="d-flex input-group">
                            <input type="password" bind:value="{password}" required class="form-control col-12" placeholder="Enter password">
                            <div class="input-group-text hover-effect" on:click={viewPassword}><i class="bi bi-eye" style="color:grey;"></i></div>
                        </div>
                    {:else}
                        <div class="d-flex input-group">
                            <input type="text" bind:value="{password}" required class="form-control col-12" placeholder="Enter password">
                            <div class="input-group-text hover-effect" on:click={viewPassword} ><i class="bi bi-eye-slash" style="color:grey;"></i></div>
                        </div>
                    {/if}
                </label>
            </div>
            {#if errorsLogin == true}
                <div class="alert alert-danger mx-3" role="alert">
                    Username or password incorrect.
                </div>
            {:else if error42Login}
                <div class="alert alert-danger mx-3" role="alert">
                    {error42Login}
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
          <div class="modal" id="myModal" tabindex="-1">
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title">Authentication with 2FA</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form on:submit|preventDefault={handleTwoFA}>
                    <p class="h5 ms-4 mt-2">2FA code</p>
                    <div class="ps-4 pe-5 ">
                        <input type="text" bind:value="{otp_code}" required class="form-control col-12 mb-2" placeholder="Enter code">
                    </div>
                    {#if errorTwoFA?.error}
                        <div class="alert alert-danger mx-3" role="alert">
                            {errorTwoFA?.error}
                        </div>
                    {:else if errorTwoFA == 'success'}
                        <div class="alert alert-success mx-3" role="alert">
                            success
                        </div>
                    {/if}
                    <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-primary" on:click={() => {errorTwoFA.error = ''}}>Login</button>
                    </div>
                </form>
              </div>
            </div>
          </div>
    </div>
</div>