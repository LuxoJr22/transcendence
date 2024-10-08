<script lang="ts">

import { updatePassword } from "$lib/stores/auth";

    let newPassword : string = '';
    let currentPassword : string = '';
    let errorsPassword : string = '';

    async function updateNewPassword() {
       const response : any = await updatePassword(newPassword, currentPassword);
        if (response.password)
        {
            errorsPassword = response.password;
        }
        else if (response.current_password)
        {
            errorsPassword = response.current_password;
        }
        else if (response == 'success')
        {
            errorsPassword = 'success';
        }
    }

</script>

<div class="card card-body">
    <form on:submit|preventDefault="{updateNewPassword}">
        <h5 class="py-3">New password</h5>
        <input type="password" class="form-control" bind:value={newPassword}>
        <h5 class="py-3">Current password</h5>
        <input type="password" class="form-control" bind:value={currentPassword}>
        {#if errorsPassword == 'success'}
            <div class="alert alert-success mt-2" role="alert">
                Password changed with success
            </div>
        {:else if errorsPassword}
            <div class="alert alert-danger mt-2" role="alert">
                {errorsPassword}
            </div>
        {/if}
        <button class="btn btn-success my-2" type="submit">Confirm</button>
    </form>
</div>