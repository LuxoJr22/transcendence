<script lang="ts">
    import { fetchUser, type AuthState } from "$lib/stores/auth";

    interface twoFA {
		success: '',
		error : '',
		otp_secret : '',
		qr_code: ''
	}

    export let state : AuthState;

    let twoFA_data : twoFA;
    let otp_code = ''
	let displayInput = false;

    async function active_2FA(){
		let accessToken = localStorage.getItem('access_token');
		const response = await fetch('/api/2fa/enable/', {
			method: 'POST',
			headers: {'Authorization': `Bearer ${accessToken}`}
		});

		if (response.ok){
			twoFA_data = await response.json();
			console.log(twoFA_data);
		}
	}

	async function disable_2FA(){
		let accessToken = localStorage.getItem('access_token');
		const response = await fetch('/api/2fa/disable/', {
			method: 'POST',
			headers: {'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
			body: JSON.stringify({otp_code})
		});

		if (response.ok){
			twoFA_data = await response.json();
			await fetchUser();
			console.log(twoFA_data);
		}
		else
			twoFA_data = await response.json();
	}

	function displayInputOtp(){
		console.log('a');
		displayInput ? displayInput = false : displayInput = true;
	}
</script>
<div class="card-body">
    <h5 class="card-title">Settings</h5>
    <p class="card-text">Change your key binds, or active 2FA</p>
    <button type="button" class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#exampleModal" on:click={async () => {displayInput = false; await fetchUser()}}>
        Open
    </button>
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">Settings</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <button class="btn d-flex" type="button" data-bs-toggle="collapse" data-bs-target="#collapse2FA" aria-expanded="false" aria-controls="collapse2FA">
                    <h3>2FA</h3>
                    <i class="bi bi-caret-down-fill m-2"></i>
                </button>
                <div class="collapse" id="collapse2FA">
                    {#if state.user?.is_2fa_enabled}
                        {#if !displayInput}
                            <div class="d-flex m-2">
                                <button class="btn btn-primary" on:click={displayInputOtp}>Disable 2FA</button>
                            </div>
                        {:else if displayInput}
                            <div class="d-flex m-2">
                                <input type="text" bind:value="{otp_code}" required class="form-control col" placeholder="Enter code">
                                <button type="button" class="btn btn-primary ms-3 p-0 col-3" on:click={async () => {await disable_2FA();}}>Disable</button>
                            </div>
                        {/if}
                    {:else}
                        {#if !twoFA_data}
                            <div class="d-flex m-2">
                                <button class="btn btn-primary" on:click={async () => {await active_2FA();}}>Active 2FA</button>
                            </div>
                        {:else if twoFA_data && !twoFA_data.success}
                            <img src="data:image/png;base64,{twoFA_data.qr_code}" style="width:50%; height:50%">
                            <ol class="list-group list-group-numbered">
                                <li class="list-group-item d-flex justify-content-between align-items-start">
                                <div class="ms-2 me-auto">
                                    <div class="fw-bold">Step 1</div>
                                        Install a authenticator app
                                </div>
                                </li>
                                <li class="list-group-item d-flex justify-content-between align-items-start">
                                <div class="ms-2 me-auto">
                                    <div class="fw-bold">Step 2</div>
                                        Scan the QR code or enter this code in the apply: {twoFA_data.otp_secret}
                                </div>
                                </li>
                            </ol>
                        {/if}
                    {/if}
                </div>
                <button class="btn d-flex" type="button" data-bs-toggle="collapse" data-bs-target="#collapsePongKey" aria-expanded="false" aria-controls="collapsePongKey">
                        <h3>Pong Key Binds</h3>
                        <i class="bi bi-caret-down-fill m-2"></i>
                </button>
                <div class="collapse" id="collapsePongKey">
                    <ul>
                        <li class="h5">Forward: <button class="kbc-button"><input style="width: 20px; border:none; outline:none"></button></li>
                        <li class="h5">Back: <button class="kbc-button">S</button></li>
                        <li class="h5">Left: <button class="kbc-button">A</button></li>
                        <li class="h5">Right: <button class="kbc-button">D</button></li>
                        <li class="h5">Dash: <button class="kbc-button">SPACE</button></li>
                    </ul>
                </div>
                <button class="btn d-flex" type="button" data-bs-toggle="collapse" data-bs-target="#collapseShooterKey" aria-expanded="false" aria-controls="collapseShooterKey">
                    <h3>Shooter Key Binds</h3>
                    <i class="bi bi-caret-down-fill m-2"></i>
                </button>
                <div class="collapse" id="collapseShooterKey">
                    <ul>
                        <li class="h5">Forward: <button class="kbc-button">W</button></li>
                        <li class="h5">Back: <button class="kbc-button">S</button></li>
                        <li class="h5">Left: <button class="kbc-button">A</button></li>
                        <li class="h5">Right: <button class="kbc-button">D</button></li>
                        <li class="h5">Dash: <button class="kbc-button">SPACE</button></li>
                    </ul>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary">Save changes</button>
            </div>
        </div>
    </div>
</div>
</div>


<style>
    li {
		list-style: none;
	}

	.modal-body{
		height: 50vh !important;
		overflow-y: auto;
	}
</style>