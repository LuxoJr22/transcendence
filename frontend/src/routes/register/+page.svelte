<script>
    import { goto } from '$app/navigation';

    let username = '';
    let email = '';
    let password = '';
    let errors = '';

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
            console.log('User creation success');
            goto('/login');
        } else {
            console.error(data);
            errors = data;
        }
    }
</script>

<div class="container-fluid" style="height:100vh;">
    <div class="d-flex justify-content-center align-items-center" style="height:100%;">
        <form on:submit|preventDefault="{register}" class="p-5 border rounded">
            <div class="mb-3">
                <label class="form-label text-light">
                    <h5>Pseudo</h5>
                    <input type="text" bind:value="{username}" required class="form-control" placeholder="Enter pseudo">
                </label>
            </div>
            {#if errors.username} 
                <div class="alert alert-danger d-flex align-items-center mt-1 p-2" role="alert">                      
                    <div>
                        {errors.username[0]}
                    </div>
                </div>
            {/if}
            <div class="mb-3">
                <label class="form-label text-light">
                    <h5>Email</h5>
                    <input type="text" bind:value="{email}" class="form-control" placeholder="Enter email">
                    
                </label>
            </div>
            {#if errors.email} 
                <div class="alert alert-danger d-flex align-items-center mt-1 p-2" role="alert">                       
                    <div>
                        <p>{errors.email[0]}</p>
                    </div>
                </div>
            {/if}
            <div class="mb-3">
                <label class="form-label text-light">
                    <h5>Password</h5>
                    <input type="password" bind:value="{password}" required class="form-control" placeholder="Enter password">
                </label>
            </div>
            {#if errors.password} 
                <div class="alert alert-danger d-flex align-items-center mt-1 p-2" role="alert">                       
                    <div>
                        {errors.password[0]}
                    </div>
                </div>
            {/if}
            <div class="btn-group-vertical col-12" role="group" aria-label="Vertical button group">
                <button type="submit" class="m-1 btn btn-primary">Create my account</button>
            </div>
        </form>
    </div>
</div>
