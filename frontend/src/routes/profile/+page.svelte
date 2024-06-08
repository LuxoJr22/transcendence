<script>
    const img = new URL('$lib/assets/sforesti.jpg', import.meta.url).href
</script>
<style>
    .circle-container {
        width: 300px;
        height: 300px;
        overflow: hidden;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .circle-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
</style>
<div class="circle-container">
    <img src={img} width=300>
</div>