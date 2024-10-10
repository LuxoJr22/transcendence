<script lang="ts">
    import { fetchUser, type AuthState } from "$lib/stores/auth";
    import { tick } from "svelte";

    interface twoFA {
		success: '',
		error : '',
		otp_secret : '',
		qr_code: ''
	}

    export let state : AuthState;

    export let twoFA_data : twoFA;
    let otp_code = ''
	let displayInput = false;

    async function getQrcode(){
		let accessToken = localStorage.getItem('access_token');
		const response = await fetch('/api/2fa/qrcode/', {
			method: 'POST',
			headers: {'Authorization': `Bearer ${accessToken}`}
		});

		if (response.ok){
			twoFA_data = await response.json();
			console.log(twoFA_data);
		}
	}

    async function enable_2FA(){
        let accessToken = localStorage.getItem('access_token');
		const response = await fetch('/api/2fa/enable/', {
			method: 'POST',
			headers: {'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
			body: JSON.stringify({otp_code})
		});

        if (response.ok){
			twoFA_data = await response.json();
			await fetchUser();
			console.log(twoFA_data);
		}
		else{
			let data = await response.json();
            twoFA_data.error = data.error;
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
            if (twoFA_data.success != '')
                twoFA_data = 0;
			await fetchUser();
		}
		else
			twoFA_data = await response.json();
	}

	function displayInputOtp(){
		console.log('a');
		displayInput ? displayInput = false : displayInput = true;
	}
</script>


<div class="modal fade" id="settingsModal" tabindex="-1" aria-labelledby="settingsModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="settingsModalLabel">Settings</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <h3 class="text-center">Key Binds</h3>
                <div class="d-flex">
                    <div class="col-6 mb-1 border-end">
                        <h5 class="text-center mb-3">Pong</h5>
                        <ul>
                            <li class="h5">Forward: <button class="kbc-button"><input style="width: 20px; border:none; outline:none"></button></li>
                            <li class="h5">Back: <button class="kbc-button">S</button></li>
                            <li class="h5">Left: <button class="kbc-button">A</button></li>
                            <li class="h5">Right: <button class="kbc-button">D</button></li>
                            <li class="h5">Dash: <button class="kbc-button">SPACE</button></li>
                        </ul>
                    </div>
                    <div class="col-6 mb-1">
                        <h5 class="text-center mb-3">Shooter</h5>
                        <ul>
                            <li class="h5">Forward: <button class="kbc-button">W</button></li>
                            <li class="h5">Back: <button class="kbc-button">S</button></li>
                            <li class="h5">Left: <button class="kbc-button">A</button></li>
                            <li class="h5">Right: <button class="kbc-button">D</button></li>
                            <li class="h5">Dash: <button class="kbc-button">SPACE</button></li>
                        </ul>
                    </div>
                </div>
                <h3 class="text-center">2FA</h3>
                {#if state.user?.is_2fa_enabled}
                    {#if !displayInput}
                        <div class="d-flex justify-content-center">
                            <button class="btn btn-primary" on:click={displayInputOtp}>Disable 2FA</button>
                        </div>
                    {:else if displayInput}
                        <div class="d-flex m-2">
                            <input type="text" bind:value="{otp_code}" required class="form-control col" placeholder="Enter code">
                            <button type="button" class="btn btn-primary ms-3 p-0 col-3" on:click={async () => {await disable_2FA();}}>Disable</button>
                        </div>
                        {#if twoFA_data && twoFA_data.error}
                            <div class="alert alert-danger">
                                {twoFA_data.error}
                            </div>
                        {/if}
                    {/if}
                {:else}
                    {#if !twoFA_data}
                        <div class="d-flex justify-content-center">
                            <button class="btn btn-primary" on:click={async () => {await getQrcode();}}>Active 2FA</button>
                        </div>
                    {:else if twoFA_data && !twoFA_data.success}
                        <div class="d-flex justify-content-center">
                            <img class="" src="data:image/png;base64,{twoFA_data.qr_code}" style="width:50%; height:50%">
                        </div>
                        <ol class="list-group text-center">
                            <li class="list-group-item">
                            <div class="ms-2 me-auto">
                                <div class="fw-bold">Step 1</div>
                                    Install a authenticator app
                            </div>
                            </li>
                            <li class="list-group-item">
                            <div class="ms-2 me-auto">
                                <div class="fw-bold">Step 2</div>
                                    Scan the QR code or enter this code in the application: <strong>{twoFA_data.otp_secret}</strong>
                                </div>
                            </li>
                            <li class="list-group-item">
                                <div class="ms-2 me-auto">
                                    <div class="fw-bold">Step 3</div>
                                    <p>Enter the code given by the application</p>
                                    <div class="d-flex m-2 ms-0">
                                        <input type="text" bind:value="{otp_code}" required class="form-control col" placeholder="Enter code">
                                        <button type="button" class="btn btn-primary ms-3 p-0 col-3" on:click={async () => {await enable_2FA();}}>Enable</button>
                                    </div>
                                    {#if twoFA_data.error}
                                        <div class="alert alert-danger">
                                            {twoFA_data.error}
                                        </div>
                                    {/if}
                                </div>
                            </li>
                        </ol>
                    {/if}
                {/if}
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary">Save changes</button>
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