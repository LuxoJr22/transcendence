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
    <h5 class="offcanvas-title" id="staticBackdropLabel">Custom canvas</h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <div class="">
      <h5>IA</h5>
      <div class="form-check">
        <input class="form-check-input" type="radio" name="IA" id="IA1">
        <label class="form-check-label" for="IA1">
          Play online
        </label>
      </div>
      <div class="form-check">
        <input class="form-check-input" type="radio" name="IA" id="IA2" checked>
        <label class="form-check-label" for="IA2">
          Play Against Bot
        </label>
      </div>
      <div class="mt-2">
        <h5>Power Up</h5>
        <div class="form-check">
          <input class="form-check-input" type="radio" name="PowerUp" id="PowerUp1">
          <label class="form-check-label" for="PowerUp1">
            Classic
          </label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="radio" name="PowerUp" id="PowerUp2" checked>
          <label class="form-check-label" for="PowerUp2">
            Power-Up
          </label>
        </div>
      </div>
      <div class="mt-2">
        <h5>Number of points</h5>
        <div class="form-check">
          <input class="form-check-input" type="radio" name="Points" id="Points2" checked>
          <label class="form-check-label" for="Points2">
            3 points
          </label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="radio" name="Points" id="Points1">
          <label class="form-check-label" for="Points1">
            7 points
          </label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="radio" name="Points" id="Points2" checked>
          <label class="form-check-label" for="Points2">
            11 points
          </label>
        </div>
      </div>
      <div class="mt-2" style="width: 80%;">
        <h5>Choose your fields</h5>
        <div class="">
          <div id="carouselExampleIndicators" class="carousel slide">
            <div class="carousel-indicators">
              <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
              <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
              <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
            </div>
            <div class="carousel-inner">
              <div class="carousel-item active">
                <img src={img1} class="d-block w-100" alt="...">
              </div>
              <div class="carousel-item">
                <img src={img2} class="d-block w-100" alt="...">
              </div>
              <div class="carousel-item">
                <img src={img3} class="d-block w-100" alt="...">
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
        <button type="button" class="btn btn-success btn-lg">Play</button>
      </div>
    </div>
  </div>
</div>