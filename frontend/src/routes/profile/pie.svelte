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
                'rgba(13, 110, 253, 1)',
                'rgba(220, 53, 69, 1)',
            ],
            borderColor: [
                'rgba(13, 170, 253, 1)',
                'rgba(255, 153, 125, 1)',
            ],
            borderWidth: 3
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

<canvas id="myChart"></canvas>
