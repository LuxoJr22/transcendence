<script lang="ts">
    import { goto } from '$app/navigation';

    interface Error {
        username : "",
        email : "",
        password : ""
    }

    let username = '';
    let email = '';
    let password = '';
    let errors : Error;

    async function register() {
        const response = await fetch('/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            goto('/login');
        } else {
            console.error(data);
            errors = data;
        }
    }

    let viewablePassword = false;

    function viewPassword(){
        viewablePassword ? viewablePassword = false : viewablePassword = true;
    }
</script>

<div class="container-fluid" style="height:100vh;">
    <div class="d-flex justify-content-center align-items-center" style="height:100%;">
        <form on:submit|preventDefault="{register}" class="p-5 border rounded">
            <ul class="p-0">
                <li>
                    <h5 class="text-light">Username</h5>
                    <input class="form-control" placeholder="Enter your username" bind:value={username}>
                </li>
                {#if errors?.username}
                <li class="pb-5 pt-0">
                    <div class="alert alert-danger p-2" role="alert">
                        {errors.username}
                    </div>
                </li>
                {/if}
                <li>
                    <h5 class="text-light {errors?.username ? 'pt-4' : ''}">Email</h5>
                    <input class="form-control"  placeholder="Enter your email" bind:value={email}>
                </li>
                {#if errors?.email}
                <li class="pb-5 pt-0">
                    <div class="alert alert-danger p-2" role="alert">
                        {errors.email}
                    </div>
                </li>
                {/if}
                <li>
                    <h5 class="text-light">Password</h5>
                    {#if !viewablePassword}
                        <div class="d-flex input-group">
                            <input type="password" bind:value="{password}" required class="form-control col-12" placeholder="Enter password">
                            <div class="hover-effect input-group-text" type="button" on:click={viewPassword}><i class="bi bi-eye" style="color:grey;"></i></div>
                        </div>
                    {:else}
                        <div class="d-flex input-group">
                            <input type="text" bind:value="{password}" required class="form-control col-12" placeholder="Enter password" autocomplete="off">
                            <div class="hover-effect input-group-text" type="button" on:click={viewPassword} ><i class="bi bi-eye-slash" style="color:grey;"></i></div>
                        </div>
                    {/if}
                </li>
                {#if errors?.password}
                <li class="pb-5 pt-0">
                    <div class="alert alert-danger p-2" role="alert">
                        {errors.password}
                    </div>
                </li>
                {/if}
            </ul>
            <div class="btn-group-vertical col-12" role="group" aria-label="Vertical button group">
                <button type="submit" class="btn btn-primary">Create my account</button>
            </div>
        </form>
    </div>
</div>


<style>

    li {
        padding-bottom: 10%;
        position: relative;
    }

    @keyframes alertDisplay {
        0% {
            opacity:0%;
            transform: translateY(-100%);
        }
        100% {
            opacity: 100%;
            transform: translateY(0%);
        }
    }

    .alert {
        position: absolute;
        animation-name: alertDisplay;
        animation-duration: 0.5s;
        animation-fill-mode: forwards;

    }

    .hover-effect:hover {
        opacity: 1;
    }
</style>