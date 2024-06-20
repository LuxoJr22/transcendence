<script>
    let password1 = "";
    let password2 = "";

    $: samePassword = (password1 === password2 || password2 === "");
</script>

<div class="container-fluid" style="height:100vh;">
    <div class="d-flex justify-content-center align-items-center" style="height:100%;">
        <div class="p-5 border rounded">
            <div class="mb-3">
                <label for="Pseudonyme" class="form-label text-light"><h5>Pseudonyme</h5></label>
                <input type="text" class="form-control" id="Pseudonyme" placeholder="Enter pseudonyme">
            </div>
            <div class="mb-3">
                <label for="password1" class="form-label text-light"><h5>Password</h5></label>
                <input bind:value={password1} type="password" class="form-control" id="password1" placeholder="Enter password">
            </div>
            <div class="mb-3">
                <label for="password2" class="form-label text-light"><h5>Confirm your password</h5></label>
                <input bind:value={password2} type="password" class="form-control" id="password2" placeholder="Enter password">
                {#if samePassword}
                    <p class="text-light">yesss</p>
                {:else}
                    <p class="text-light">Nooo</p>
                {/if}
            </div>
            <div class="btn-group-vertical col-12" role="group" aria-label="Vertical button group">
                <button type="button" class="m-1 btn btn-primary">Create my account</button>
            </div>
        </div>
    </div>
</div>