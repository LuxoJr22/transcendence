<script>
    const img = new URL('$lib/assets/sforesti.jpg', import.meta.url).href
</script>
<style>
    .circle-container {
        width: 300px; /* La taille désirée du cercle */
        height: 300px; /* La taille désirée du cercle */
        overflow: hidden; /* Cache le surplus de l'image */
        border-radius: 50%; /* Pour rendre le conteneur circulaire */
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .circle-container img {
        width: 100%;
        height: 100%;
        object-fit: cover; /* Pour que l'image remplisse le conteneur sans distorsion */
    }
</style>
<div class="circle-container">
    <img src={img} width=300>
</div>