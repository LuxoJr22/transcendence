<script lang="ts">
    import { updateUsername } from "$lib/stores/auth";

    let newUsername : string;
    let errorsMessage : string = '';

    function resetValue(){
        errorsMessage = '';
    }

    async function update(){
        const data = await updateUsername(newUsername);
        if (!data)
            errorsMessage = 'success';
        else
            errorsMessage = data.username;
    }
</script>

<div class="card card-body">
    <form on:submit|preventDefault="{update}">
        <input type="text" class="form-control" bind:value={newUsername}>
        <button class="btn btn-success my-2" type="submit" on:click={resetValue}>Confirm</button>
        {#if errorsMessage == 'success'}
            <div class="alert alert-success" role="alert">
                Username changed with success
            </div>
        {:else if errorsMessage}
        <div class="alert alert-danger" role="alert">
            {errorsMessage}
        </div>
        {/if}
    </form>
</div>