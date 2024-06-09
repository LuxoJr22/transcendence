<script>
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
    width: 40%;
  }
</style>

<div class="container-fluid">
  <div class="row">
    <div class="col-6 d-flex mt-5 ps-5 pt-5 justify-content-start align-items-start">
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
    <div class="container col-6 mt-5 pt-5">
      <div class="row mx-auto">
        <div class="card mycard">
          <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
          </div>
        </div>
        <div class="card mycard">
          <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
          </div>
        </div>
      </div>
      <div class="row mx-auto">
        <div class="card mycard">
          <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
          </div>
        </div>
        <div class="card mycard">
          <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
