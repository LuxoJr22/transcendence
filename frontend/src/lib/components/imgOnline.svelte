<script>
    export let user_id;
    export let path;
    export let status;
    export let width;
    export let height;
</script>

<div class="icon-container" style="width:{width}; height:{height}">
    <img alt="avatar" src={path} class="rounded-circle align-items-center">
    <div id="status_{user_id}" class="status-circle {status ? 'online' : 'offline'}"></div>
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
        transform: translate(20%, -30%);
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