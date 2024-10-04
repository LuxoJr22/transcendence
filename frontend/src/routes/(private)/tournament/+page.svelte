<script lang="ts">
    const img = new URL('$lib/assets/pong.png', import.meta.url).href
    const img1 = new URL('$lib/assets/game2.png', import.meta.url).href

    //const create_tournament = document.getElementById("create_button");

    var tournament_name : string

    async function create_tournament() {
        console.log(tournament_name)
        const response = await fetch('api/tournament/create/', {
		method: 'POST',
		headers: {'Content-Type': 'application/json' ,'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
        body: JSON.stringify({ "name":`${tournament_name}`, 'nb_player':4}),
		});
		const data = await response.json();
        if (response.ok)
		{
			window.location.href = `/tournament/${data.id}`;
		}
    }


    /*let url = '/ws/tournament/pong/tournoi/?token=' + localStorage.getItem('access_token');
    const chatSocket = new WebSocket(url)


     chatSocket.onmessage = function(e) {
	
        let data = JSON.parse(e.data)

        if (data.event = "Match")
        {
            localStorage.setItem('game_id', data.game_id);
            window.location.href = 'matchmaking/pong/private';
        }
    }*/
    
</script>

<div class="container">
    <div class="row mt-5">
        <div class="d-flex justify-content-center border-bottom">
            <button class="btn btn-primary mb-3" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasWithBothOptions" aria-controls="offcanvasWithBothOptions"><i class="bi-plus-square-fill" style="font-size: 1.6rem; color: cornflowerblue;"></i><p class="mb-1">New tournament</p></button>
        </div>
        <div class="offcanvas offcanvas-start" data-bs-scroll="true" tabindex="-1" id="offcanvasWithBothOptions" aria-labelledby="offcanvasWithBothOptionsLabel">
            <div class="offcanvas-header">
                <h3 class="offcanvas-title" id="offcanvasWithBothOptionsLabel">Tournament Creation</h3>
                <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
            </div>
            <div class="offcanvas-body">
                <div>
                    <div class="mb-3">
                        <label for="formGroupExampleInput" class="form-label"><h4>Tournament's name</h4></label>
                        <input type="text" class="form-control" id="formGroupExampleInput" placeholder="Enter name" bind:value={tournament_name}>
                    </div>
                </div>
                <div class="">
                    <h4>Size of tournament</h4>
                    <div class="row mt-3">
                        <div class="col-4">
                            <input type="radio" class="btn-check" name="options" id="option1" autocomplete="off" checked>
                            <label class="btn btn-secondary" for="option1">4 players</label>
                        </div>
                        <div class="col-4">    
                            <input type="radio" class="btn-check" name="options" id="option2" autocomplete="off">
                            <label class="btn btn-secondary" for="option2">8 players</label>
                        </div>
                    </div>
                </div>
                <div class="mt-4">
                    <h4>Choose your game</h4>
                    <div id="carouselExampleIndicators" class="carousel slide">
                        <div class="carousel-indicators">
                            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
                            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
                        </div>
                        <div class="carousel-inner">
                            <div class="carousel-item active">
                                <img src={img} class="d-block w-100 mt-2" alt="...">
                            </div>
                            <div class="carousel-item">
                                <img src={img1} class="d-block w-100 mt-2" alt="...">
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
            </div>
            <div class="d-flex justify-content-center mb-4" >
                {#if tournament_name==undefined || tournament_name==""}
                    <button class="btn btn-dark btn-lg mb-5 p-3 mybtn" style="opacity:0.7" title="Insert a Tournament name">Create Tournament</button>
                {:else}
                    <button type="button" class="btn btn-dark btn-lg mb-5 p-3" on:click={create_tournament}>Create Tournament</button>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>
    .mybtn:hover {
        opacity: 0.7 !important;
        background-color: #212529 !important;
        cursor:not-allowed;
    }
</style>