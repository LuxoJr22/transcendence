<script>
    const img = new URL('$lib/assets/Capture.PNG', import.meta.url).href
    const img1 = new URL('$lib/assets/img.webp', import.meta.url).href

    let gameName = "otherGame";

    function whatGame(){
      if (gameName === "otherGame")
        gameName = "pong"
      else
        gameName = "otherGame"
    };
</script>

<div class="container">
  <div class="row"> 
    <div class="col text-end">
      <p class="text-light">otherGame</p>
    </div>
    <div class="col-auto">
      <div class="form-check form-switch">
        <input on:click={whatGame} class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault">
      </div>
    </div>
    <div class="col text-start">
      <p class="text-light">Pong</p>
    </div>
  </div>
</div>

{#if gameName === "otherGame"}
  <p class="text-light">Je suis le other game</p>
{:else}
  <div class="container-fluid">
    <h2 class="text-light p-2">Type de partie</h2>
    <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
      <input type="radio" class="btn-check" name="btnradio" id="btnradio1" autocomplete="off" checked>
      <label class="btn btn-outline-primary" for="btnradio1">Online</label>
    
      <input type="radio" class="btn-check" name="btnradio" id="btnradio2" autocomplete="off">
      <label class="btn btn-outline-primary" for="btnradio3">Tournament</label>
    </div>
    <h2 class="text-light p-2">Type d'adversaire</h2>
  </div>
{/if}