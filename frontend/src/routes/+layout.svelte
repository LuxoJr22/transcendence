<script>
    const img = new URL('$lib/assets/sforesti.jpg', import.meta.url).href
    const img1 = new URL('$lib/assets/img.webp', import.meta.url).href
</script>

<style>
    .layout-title {
        font-family: "Bungee", sans-serif;
    }

    .opacity:hover {
        opacity: 0.5;
    }
/* 
    :global(body) {
        background-color: var(--bs-dark);
    } */
    .text-warning-subtle {
        color: var(--bs-warning-bg-subtle);
    }

    .text-primary-subtle {
        color: var(--bs-primary-bg-subtle);
    }

    .responsive-img {
        object-fit: cover;
    }

    .dropdown-menu-addon {
        position: fixed;
        right: 0;
        top: auto;
        transform: translateX(-100%);
    }

</style>
<nav class="navbar">
    <div class="container-fluid">
        <a href="/" class="navbar-item navbar-brand fs-1 layout-title text-warning-subtle ms-4 opacity">t r i p l u m</a>
        <div class="dropdown">
            <a href="/" class="navbar-item navbar-brand text-primary-subtle opacity dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-expanded="false"><img src={img} class="border border rounded-circle mb-1 me-1 responsive-img" width="30" height="30">sforesti</a>
            <ul class="dropdown-menu" style="min-width: 0;">
              <li><a class="dropdown-item text-start ps-2" href="/profile"><i class="bi-gear pe-2" style="font-size: 1.3rem; color: grey;"></i>settings</a></li>
              <li><a class="dropdown-item text-danger text-start ps-2" href="#"><i class="bi-box-arrow-right pe-2" style="font-size: 1.3rem; color: red;"></i>logout</a></li>
            </ul>
          </div>
        
    </div>
</nav>

<slot />

<!-- <footer class="bg-secondary fixed-bottom text-center">
    <p class="text-center">Final project of 42 school's common core, Transcendence, by <a href="https://github.com/LuxoJr22/transcendence" target="_blank" class="text-light">Triplum</a></p>
</footer> -->