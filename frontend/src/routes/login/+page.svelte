<script lang="ts">;
    import { goto } from '$app/navigation';
    import { login } from '../../stores/auth';

    let username = '';
    let password = '';
    let errorsLogin = false;

    function resetLoginErrors()
    {
        errorsLogin = false;
    }

    async function handleLogin() {
        const response = await login(username, password);
        if (response == 'success')
            goto('/');
        else
        {
            errorsLogin = true;
        }
    }

    const logo42 = new URL('$lib/assets/42_Logo.svg', import.meta.url).href
</script>

<div class="container-fluid" style="height:100vh;">
    <div class="d-flex justify-content-center align-items-center" style="height:100%;">
        <form on:submit|preventDefault="{handleLogin}" class="p-5 border rounded">
            <div class="mb-3">
                <label for="formGroupExampleInput" class="form-label text-light container-fluid">
                    <h5>Pseudo</h5>
                    <input type="text" bind:value="{username}" class="form-control" id="formGroupExampleInput" placeholder="Enter pseudo">
                </label>
            </div>
            <div class="mb-3">
                <label for="formGroupExampleInput" class="form-label text-light container-fluid">
                    <h5>Password</h5>
                    <input type="password" bind:value="{password}" class="form-control" id="formGroupExampleInput" placeholder="Enter password">
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
                <a href="https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-695587cb7aebd8ec53be9fd30a29b6ddc80fb47b198a9b1601abfc4a9792217b&redirect_uri=http%3A%2F%2Fc3r2p3%3A8080%2F&response_type=code" type="button" class="m-1 btn btn-light">Login with <img src={logo42} alt="" class="ms-1" style="height:1.5rem;"/></a>
            </div>
        </form>
    </div>
</div>