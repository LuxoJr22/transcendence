<script>
    const img = new URL('$lib/assets/pong.png', import.meta.url).href
    const img1 = new URL('$lib/assets/game2.png', import.meta.url).href
</script>

<style>
  .container-game {
  width: 50%;
  display: flex;
}

  .container-game img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .mycard {
    width: 10%;
    height: 5%;

  }
</style>

<div class="container-fluid d-flex mt-5 ps-5 pt-5 justify-content-start">
  <div id="carouselExample" class="carousel slide container-game">
    <div class="carousel-inner">
      <div class="carousel-item active">
        <img src={img} class="d-block" alt="">
      </div>
      <div class="carousel-item">
        <img src={img1} class="d-block" alt="">
      </div>
    </div>
    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</div>

