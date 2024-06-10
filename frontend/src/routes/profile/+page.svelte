<script>
    const img = new URL('$lib/assets/sforesti.jpg', import.meta.url).href
</script>
<style>
</style>

<div class="container border rounded">
    <div class="row py-2">
        <div class="col-3">
            <img src={img} class="img-fluid rounded">
        </div>
        <div class="col-3 text-light d-flex align-items-center">
            <p>@sforesti</p>
        </div>
    </div>
    <div class="row mx-1 my-2">  
        <div class="col-3">
            <button type="button" class="btn btn-success">Add-friend</button>
            <button type="button" class="btn btn-primary">Message</button>
            <button type="button" class="btn btn-danger">Block</button>
        </div>
    </div>
</div>