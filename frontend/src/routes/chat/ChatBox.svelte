<script lang="ts">
    import type { friendInterface } from "../../stores/friendship";

    export let indexFriend : string;
    export let friendListCb : friendInterface;
</script>

<div class="d-flex m-4 row">
    <h4 class="text-light">{friendListCb[indexFriend]?.username}</h4>
</div>

<style>

</style>