<script>
    export let path;
    export let status;
    export let width;
    export let height;
</script>

<div class="icon-container" style="width:{width}; height:{height}">
    <img src={path} class="rounded-circle m-2 align-items-center">
    {#if status}
        <div class="status-circle online">
        </div>
    {:else}
        <div class="status-circle offline">
        </div>
    {/if}
</div>

<style>
    .icon-container {
        position: relative;
        object-fit: cover;
    }

    .icon-container img {
        height: 100%;
        width: 100%;
        border-radius: 50%;
        object-fit: cover;
        aspect-ratio: 1;
    }

    .status-circle {
        width: 15px;
        height: 15px;
        border-radius: 50%;
        transform: translateY(-35%);
        background-color: grey;
        border: 2px solid white;
        bottom: 0;
        right: 0;
        position: absolute;
    }

    .status-circle.offline {
        background-color: grey;
        border: 2px solid white;
    }
    .status-circle.online {
        background-color: green;
        border: 2px solid white;
    }
</style>