<script>
  const img1 = new URL('$lib/assets/CanvaCarousel/Terrain1.png', import.meta.url).href
  const img2 = new URL('$lib/assets/CanvaCarousel/Terrain2.png', import.meta.url).href
  const img3 = new URL('$lib/assets/CanvaCarousel/Terrain3.png', import.meta.url).href
</script>


<button class="btn btn-dark mt-4" type="button" data-bs-toggle="offcanvas" data-bs-target="#staticBackdrop" aria-controls="staticBackdrop">
    Custom my games
</button>
<div class="offcanvas offcanvas-start" data-bs-backdrop="static" tabindex="-1" id="staticBackdrop" aria-labelledby="staticBackdropLabel">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="staticBackdropLabel">Custom your games</h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <div class="">
      <h5>IA</h5>
      <div class= "row">
        <div class="form-check col-3">
          <input class="btn-check" type="radio" name="IA" id="IA1">
          <label class="btn btn-secondary" for="IA1">
            Online
          </label>
        </div>
        <div class="form-check col-3">
          <input class="btn-check" type="radio" name="IA" id="IA2" checked>
          <label class="btn btn-secondary" for="IA2">
            Bot
          </label>
        </div>
      </div>
      <div class="mt-2 row">
        <h5>Power Up</h5>
        <div class="form-check col-3">
          <input class="btn-check" type="radio" name="PowerUp" id="PowerUp1">
          <label class="btn btn-secondary" for="PowerUp1">
            Classic
          </label>
        </div>
        <div class="form-check col-5">
          <input class="btn-check" type="radio" name="PowerUp" id="PowerUp2" checked>
          <label class="btn btn-secondary" for="PowerUp2">
            Power-Up
          </label>
        </div>
      </div>
      <div class="mt-2 row">
        <h5>Number of points</h5>
        <div class="form-check col-4">
          <input class="btn-check" type="radio" name="Points" id="Points1" checked>
          <label class="btn btn-secondary" for="Points1">
            3 points
          </label>
        </div>
        <div class="form-check col-3 ps-0 me-1">
          <input class="btn-check" type="radio" name="Points" id="Points2">
          <label class="btn btn-secondary" for="Points2">
            7 points
          </label>
        </div>
        <div class="form-check col-3 ms-1 ps-0 pe-0">
          <input class="btn-check" type="radio" name="Points" id="Points3" checked>
          <label class="btn btn-secondary" for="Points3">
            11 points
          </label>
        </div>
      </div>
      <div class="mt-2" style="width: 90%;">
        <h5>Choose your fields</h5>
        <div class="ms-4">
          <div id="carouselExampleIndicators" class="carousel slide">
            <div class="carousel-indicators">
              <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
              <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
              <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
            </div>
            <div class="carousel-inner">
              <div class="carousel-item active">
                <img src={img1} class="d-block w-100 mt-2" alt="...">
              </div>
              <div class="carousel-item">
                <img src={img2} class="d-block w-100 mt-2" alt="...">
              </div>
              <div class="carousel-item">
                <img src={img3} class="d-block w-100 mt-2" alt="...">
              </div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Next</span>
            </button>
          </div>
        </div>
        <div class="d-flex justify-content-center">
          <button type="button" class="btn btn-success btn-lg mt-4 ms-1 px-5">Play</button>
        </div>   
      </div>
    </div>
  </div>
</div>