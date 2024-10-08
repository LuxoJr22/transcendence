<script lang="ts">
    import { updateEmail } from "$lib/stores/auth";

    let newEmail : string;
    let errorsMessage : string = '';

    function resetValue(){
        errorsMessage = '';
    }

    async function update(){
        const data = await updateEmail(newEmail);
        if (!data){
            errorsMessage = 'success';
        }
        else
            errorsMessage = data.email;
    }
</script>

<div class="card card-body">
    <form on:submit|preventDefault="{update}">
        <input type="text" class="form-control" bind:value={newEmail}>
        <button class="btn btn-success my-2" type="submit">Confirm</button>
        {#if errorsMessage == 'success'}
            <div class="alert alert-success" role="alert">
                Email changed with success
            </div>
        {:else if errorsMessage}
        <div class="alert alert-danger" role="alert">
            {errorsMessage}
        </div>
        {/if}
    </form>
</div>