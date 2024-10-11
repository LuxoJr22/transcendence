<script lang="ts">
    import { refresh_token } from "$lib/stores/auth";
    import type { Profile } from "$lib/stores/user";
    import { onMount } from "svelte";
    import ImgOnline from "../imgOnline.svelte";
    
    let allUser = new Array<Profile>();
    let userSearch : string;
    export let roomId;
    
    function resetFriendSearch (){
        userSearch = '';
    }

    async function fetchAllUser(){
        await refresh_token();
        const accessToken = localStorage.getItem('access_token');
        const response = await fetch('/api/user/list/', {
            headers : { 'Authorization': `Bearer ${accessToken}`}
        });

        if (response.ok){
            allUser = await response.json();
        }

    }

    function loadRoom(roomId : number){
        window.location.href = '/chat/' + (roomId.toString()) + '/'; 
    }

    onMount(async () => {
        await fetchAllUser();
    })

</script>

<div class="d-flex m-4 row">
    <h4 class="text-light col-10 mt-2 text-truncate">Discussions</h4>
    <button type="button" class="btn col-2 p-0" data-bs-toggle="modal" data-bs-target="#userListModal"><i class="bi bi-plus" style="color:white; font-size:2em" on:click={async () => {await fetchAllUser()}}></i></button>
    <div class="modal fade" id="userListModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="userListModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content text-light bg-dark">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="userListModalLabel">Friends List</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" on:click={resetFriendSearch}></button>
            </div>
            <div class="d-flex justify-content-center">
                <input class="form-control m-2 mt-4" placeholder="Find a user to chat" bind:value={userSearch} style="width:80%">
            </div>
            <div class="modal-body d-flex justify-content-center row row-cols-4 user-container m-0 me-2 mb-2">
                {#each allUser as user}
                    {#if user.username.includes(userSearch) || !userSearch}
                        <div class="col text-center p-0 m-2" role="button">
                            <button class="text-center btn text-light bg-gradient border rounded" on:click={resetFriendSearch} on:click={loadRoom(user.id)} data-bs-dismiss="modal" aria-label="Close">
                                <div class="d-flex justify-content-center">
                                    <ImgOnline path={user?.profile_picture_url} status={user?.is_online} width=50% height=50% />
                                </div>
                                <p class="text-center">{user.username}</p>
                                <i class="bi bi-plus pt-2" style="font-size:1.8em"></i>
                            </button>    
                        </div>
                    {/if}
                {/each}
                {#if !allUser[0]}
                    <p class="d-flex justify-content-center mt-3" style="color:grey;">Empty user list</p>
                {/if}
            </div>
            </div>
        </div>
    </div>
</div>

<style>
    .modal-body {
        height: 23vh !important;
    }

    .user-container{
        height: 20% !important;
        overflow-y: auto;
        overflow-x: hidden;
        scrollbar-width: thin;
        scrollbar-color: black grey;
    }
</style>