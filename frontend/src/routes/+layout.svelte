<script>
    const img = new URL('$lib/assets/sforesti.jpg', import.meta.url).href
    const img1 = new URL('$lib/assets/img.webp', import.meta.url).href
</script>

<style>
    .layout-title {
        font-family: "Danfo", sans-serif;
    }
    :global(body) {
        background-color: var(--bs-dark);
    }
</style>
<nav class="navbar">
    <div class="container-fluid m-1">
        <a href="/" class="navbar-item navbar-brand text-light fs-1 layout-title ms-4">t r i p l u m</a>
        <a href="/profile" class="navbar-item navbar-brand text-light"><img src={img} class="border border rounded-circle m-1" width="30" height="30">Profile</a>
    </div>
</nav>

<slot />

<footer class="bg-secondary fixed-bottom text-center">
    <p class="text-center">Final project of 42 school's common core, Transcendence, by <a href="https://github.com/LuxoJr22/transcendence" target="_blank" class="text-light">Triplum</a></p>
</footer>