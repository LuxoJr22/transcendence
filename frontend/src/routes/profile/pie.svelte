<script>
    import { onMount, onDestroy } from 'svelte';
    import { Chart } from 'chart.js/auto';

    let chart;

    export let victories = 0;
    export let defeats = 0;


    const data = {
        labels: ['Victory', 'Defeat'],
        datasets: [{
            data: [victories, defeats],
            backgroundColor: [
                'rgba(75, 192, 192, 0.2)',
                'rgba(255, 159, 64, 0.2)',
            ],
            borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 159, 64, 1)',
            ],
            borderWidth: 1
        }]
    };

    const options = {
        responsive: true,
    };

    onMount(() => {
        const ctx = document.getElementById('myChart').getContext('2d');
        chart = new Chart(ctx, {
            type: 'pie',
            data,
            options
        });
    });

    onDestroy(() => {
        if (chart) {
            chart.destroy();
        }
    });
</script>

<div style="width: 35vw; height: 35vh;">
    <canvas id="myChart"></canvas>
</div>