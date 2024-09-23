<script>
    import CustomCanva from "$lib/static/customGameCanva.svelte"
    const img = new URL('$lib/assets/pong.png', import.meta.url).href
    const img1 = new URL('$lib/assets/game2.png', import.meta.url).href
</script>

<style>
  .container-game {
    width: 100%;
    display: flex;
  }

  .container-game img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .mycard {
    width: 42%;
  }
</style>

<div class="container-fluid">
  <div class="row">
    <div class="col-xl-6 col-12 d-flex mt-xxl-3 mt-5 ps-xl-4 pt-xl-5 justify-content-start align-items-start">
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
    <div class="container col-xl-6 col-12 mt-xl-5 pt-xl-5 ms-xl-0 ms-2 mb-xl-0 mb-5">
      <div class="pt-4">
        <div class="row mx-auto mb-3">
          <div class="card mycard me-3 ms-sm-5 ms-3 bg-warning-subtle">
            <div class="card-body">
              <h5 class="card-title">Online Mode</h5>
              <p class="card-text">Play online against other players.</p>
              <a href="/game" class="btn btn-dark mt-4">Play</a>
            </div>
          </div>
          <div class="card mycard bg-warning-subtle">
            <div class="card-body">
              <h5 class="card-title">Tournament</h5>
              <p class="card-text">Compete in tournaments and prove your skills.</p>
              <a href="/tournament" class="btn btn-dark">Create or Join</a>
            </div>
          </div>
        </div>
        <div class="row mx-auto">
          <div class="card mycard bg-warning-subtle me-3 ms-sm-5 ms-3">
            <div class="card-body">
              <h5 class="card-title">Custom Matches</h5>
              <p class="card-text">Create your own custom matches.</p>
              <CustomCanva/>
            </div>
          </div>
          <div class="card mycard bg-warning-subtle">
            <div class="card-body">
              <h5 class="card-title">Character Customization</h5>
              <p class="card-text">Personalize your character's appearance and style.</p>
              <a href="/selection" class="btn btn-dark">Custom my character</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
