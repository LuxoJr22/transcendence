<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    onMount(() => {
        if (window.location.href.substring(window.location.href.lastIndexOf('/') + 1) == 'chat')
            goto('/chat/home');
    })
</script>