<script lang="ts">
    import { auth, fetchUser, type AuthState } from "$lib/stores/auth";
    import { onMount } from "svelte";
    import { keyboardMap } from "./keyMap"

    interface twoFA {
		success: '',
		error : '',
		otp_secret : '',
		qr_code: ''
	}

    interface Dictionary<T> {
        [Key: string]: T;
    }

    interface keySelected {
        index: number,
        key: string
    }

    export let state : AuthState;

    state = $auth;

    export let twoFA_data : twoFA | null;
    export let otp_code : string;
    let waitingForKey = false;
    let keySelected : keySelected = {index: 0, key: ''};
	let displayInput = false;
    export let keyBinds : Array<Dictionary<number>> = [];

    onMount(async () => {
        await fetchUser();
        auth.subscribe((value : AuthState) =>{
            state = value;
        });
    })

    async function getQrcode(){
		let accessToken = localStorage.getItem('access_token');
		const response = await fetch('/api/2fa/qrcode/', {
			method: 'POST',
			headers: {'Authorization': `Bearer ${accessToken}`}
		});

		if (response.ok){
			twoFA_data = await response.json();
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
		}
		else{
			let data = await response.json();
            twoFA_data!.error = data.error;
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
            if (twoFA_data?.success != '')
                twoFA_data = null;
			await fetchUser();
		}
		else
			twoFA_data = await response.json();
	}

	function displayInputOtp(){
		displayInput ? displayInput = false : displayInput = true;
	}

    async function getKeyBinds(){
        const resp = await fetch('/api/pong/settings/' + state.user?.id + '/', {
		    method: 'GET',
		    headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
		});
		const dat = await resp.json();
		if (resp.ok)
		{
			keyBinds[0] = dat.settings;
		}
        const resp1 = await fetch('/api/shooter/settings/' + state.user?.id + '/', {
		    method: 'GET',
		    headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
		});
		const dat1 = await resp1.json();
		if (resp.ok)
		{
			keyBinds[1] = dat1.settings;
		}
    }
    
    document.addEventListener("keydown", onDocumentKeyDown, false);

    function onDocumentKeyDown(event : KeyboardEvent){
        var keycode = event.which;
        if (waitingForKey){
            keyBinds[keySelected.index][keySelected.key] = keycode;
            waitingForKey = false;
        }
    }

    function updateBinds(i : number, name : string){
        keySelected.index = i;
        keySelected.key = name;
        waitingForKey = true;
    }

    async function saveBinds(){

        const response = await fetch('/api/user/settings/update/', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json',  'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
            body: JSON.stringify({ 'pong' : keyBinds[0],  'shooter' : keyBinds[1] })
        })

        const data = await response.json();

        if (response.ok){
        }
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
                            <li class="h5">Forward: <button class="kbc-button" on:click={() => updateBinds(0, 'up')}>{keyboardMap[keyBinds[0].up]}</button></li>
                            <li class="h5">Back: <button class="kbc-button" on:click={() => updateBinds(0, 'down')}>{keyboardMap[keyBinds[0].down]}</button></li>
                            <li class="h5">Left: <button class="kbc-button" on:click={() => updateBinds(0, 'left')}>{keyboardMap[keyBinds[0].left]}</button></li>
                            <li class="h5">Right: <button class="kbc-button" on:click={() => updateBinds(0, 'right')}>{keyboardMap[keyBinds[0].right]}</button></li>
                            <li class="h5">Dash: <button class="kbc-button" on:click={() => updateBinds(0, 'charge')}>{keyboardMap[keyBinds[0].charge]}</button></li>
                        </ul>
                    </div>
                    <div class="col-6 mb-1">
                        <h5 class="text-center mb-3">Shooter</h5>
                        <ul>
                            <li class="h5">Forward: <button class="kbc-button" on:click={() => updateBinds(1, 'up')}>{keyboardMap[keyBinds[1].up]}</button></li>
                            <li class="h5">Back: <button class="kbc-button" on:click={() => updateBinds(1, 'down')}>{keyboardMap[keyBinds[1].down]}</button></li>
                            <li class="h5">Left: <button class="kbc-button" on:click={() => updateBinds(1, 'left')}>{keyboardMap[keyBinds[1].left]}</button></li>
                            <li class="h5">Right: <button class="kbc-button" on:click={() => updateBinds(1, 'right')}>{keyboardMap[keyBinds[1].right]}</button></li>
                            <li class="h5">Jump: <button class="kbc-button" on:click={() => updateBinds(1, 'jump')}>{keyboardMap[keyBinds[1].jump]}</button></li>
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
                    {:else if twoFA_data}
                        <div class="d-flex justify-content-center">
                            <img class="" alt="2fe_qr_code" src="data:image/png;base64,{twoFA_data.qr_code}" style="width:50%; height:50%">
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
                <button type="button" class="btn btn-primary" on:click={saveBinds}>Save changes</button>
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