<script lang="ts">
	let currentUrl : string = window.location.href;
	let gamemode = currentUrl.substring(currentUrl.lastIndexOf('/') + 1);
	console.log(gamemode)
</script>