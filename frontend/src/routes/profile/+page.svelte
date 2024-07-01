<script>
    import { onMount } from 'svelte';
    export let data; // Récupère les données exportées
    const img = new URL('$lib/assets/sforesti.jpg', import.meta.url).href;
    let users = [];
    users = data.users;
</script>
<style>
</style>

<div class="container border rounded">
    <div class="row py-2">
        <div class="col-3">
            <img src={img} class="img-fluid rounded">
        </div>
        <div class="col-3 text-light d-flex align-items-center">
         {#if users[1]}
            <p>@{users[2].pseudonyme}</p>
        {:else}
            <p>Loading...</p>
        {/if}
        </div>
    </div>
    <div class="row mx-1 my-2">  
        <div class="col-3">
            <button type="button" class="btn btn-success">Add-friend</button>
            <button type="button" class="btn btn-primary">Message</button>
            <button type="button" class="btn btn-danger">Block</button>
        </div>
    </div>
</div>