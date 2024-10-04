<script>
    import { onDestroy, onMount } from 'svelte';

    onMount(() => {
        console.log(window.location.href.substring(window.location.href.lastIndexOf('/') + 1));
        if (window.location.href.substring(window.location.href.lastIndexOf('/') + 1) == 'chat')
            window.location.href = '/chat/home';
    })
</script>