<script lang="ts">
    import { onMount } from 'svelte';
    const img = new URL('/assets/pong.png', import.meta.url).href
    const img1 = new URL('/assets/game2.png', import.meta.url).href
    import { refresh_token } from '$lib/stores/auth';
    import { goto } from '$app/navigation';

    //const create_tournament = document.getElementById("create_button");
    interface Dictionary<T> {
        [Key: string]: T;
    }

    var tournament_name : string

    let allTournament : Dictionary<string>[] = [];

    async function create_tournament() {
        const response = await fetch('api/tournament/create/', {
		method: 'POST',
		headers: {'Content-Type': 'application/json' ,'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
        body: JSON.stringify({ "name":`${tournament_name}`, 'nb_player':4, 'capacity': 4}),
		});
		const data = await response.json();
        if (response.ok)
		{
			goto(`/tournament/${data.name}`);
		}
    }

    async function fetchAllTournaments(){
        await refresh_token();
            const accessToken = localStorage.getItem('access_token');
            const response = await fetch('/api/tournament/list/', {
                headers : { 'Authorization': `Bearer ${accessToken}`}
            });

            if (response.ok){
                allTournament = await response.json();
            }
    }

    async function go_to_tournament(id : string){
        goto(`/tournament/${id}`);
    }

    onMount(async () => {
            await fetchAllTournaments()
    });
    
</script>

<div class="container">
    <div class="row mt-5">
        <div class="d-flex justify-content-center border-bottom">
            <button class="btn btn-primary mb-3" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasWithBothOptions" aria-controls="offcanvasWithBothOptions"><i class="bi-plus-square-fill" style="font-size: 1.6rem; color: cornflowerblue;"></i><p class="mb-1">New tournament</p></button>
        </div>
        <div class="modal-body d-flex justify-content-center row user-container m-0 me-2 mb-2">
            {#each allTournament as tournament}
                <div class="row p-0 m-2" role="button">
                    <button on:click={() => {go_to_tournament(tournament.name)}} class="btn text-light border rounded" aria-label="Close">
                        <!-- <div class="d-flex justify-content-center"></div> -->
                        <p class="d-inline">{tournament.name}</p>
                        <p class="d-inline">{tournament.participants.length}/{tournament.capacity}</p>
                        <!-- <i class="bi bi-plus pt-2" style="font-size:1.8em"></i> -->
                    </button>    
                </div>
            {/each}
            {#if !allTournament[0]}
                <p class="d-flex justify-content-center mt-3" style="color:grey;">Empty tournament list</p>
            {/if}
        </div>
        <form>
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
                        <button type="submit" class="btn btn-dark btn-lg mb-5 p-3" on:click={create_tournament}>Create Tournament</button>
                    {/if}
                </div>
            </div>
        </form>
    </div>
</div>

<style>
    .mybtn:hover {
        opacity: 0.7 !important;
        background-color: #212529 !important;
        cursor:not-allowed;
    }
</style>