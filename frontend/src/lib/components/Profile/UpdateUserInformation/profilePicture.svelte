<script lang="ts">
    import { updateProfilePicture } from "$lib/stores/auth";

    export let state;

    window.addEventListener("popstate",(event) => {
        let myModal = bootstrap.Modal.getInstance(document.getElementById('pictureModal'));
        if (myModal)
            myModal.hide();
    });

    let newProfilePicture : File;
    let error : any;
    function handleFileChange(event: any) {
        newProfilePicture = event.target.files[0];
    }

    function resetErrors() {
        error = '';
    }

    async function updateNewProfilePicture(){
        if (newProfilePicture == null){
            return ;
        }
        if (newProfilePicture.size > 10 * 1024 * 1024) {
            error = "File too large"
            return ;
        }
        if (newProfilePicture) {
            try {
                error = await updateProfilePicture(newProfilePicture);
            } catch (e) {
                error = e;
                return;
            }
        }
        if (error && error != 'success')
            error = error.profile_picture;
    }
</script>

<div class="d-flex justify-content-center align-items-center">
    <button class="btn" type="button" data-bs-toggle="modal" data-bs-target="#pictureModal"><img alt="user profile" src={state.user?.profile_picture} class="img-circle rounded-circle hover-effect ms-2"></button>
</div>
<div class="modal fade" id="pictureModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <form on:submit|preventDefault="{updateNewProfilePicture}">
            <div class="modal-body">
                <input type="file" on:change={handleFileChange}>
            </div>
            {#if error != 'success' && error}
            <div class="alert alert-danger mx-3" role="alert">
                {error}
            </div>
            {:else if error == 'success'}
            <div class="alert alert-success mx-3" role="alert">
                Image successfully changed.
            </div>
            {/if}
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" on:click={resetErrors}>Close</button>
                <button type="submit" class="btn btn-success" on:click={resetErrors}>Save changes</button>
            </div>
        </form>
      </div>
    </div>
</div>

<style>
    .img-circle {
        width: 80%;
        height: 80%;
        min-width: 10.9vw;
        min-height: 22.6vh;
        object-fit: cover;
        aspect-ratio: 1;
    }

    .hover-effect:hover {
        opacity: 0.5;
    }
</style>