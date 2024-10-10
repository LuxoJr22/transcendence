<script>
    import { onMount, onDestroy } from 'svelte';
    import { Chart } from 'chart.js/auto';

    let chart;

    export let victories = 0;
    export let defeats = 0;

    const data = {
        labels: ['Victory (%)', 'Defeat (%)'],
        datasets: [{
            data: [(victories / (defeats + victories) * 100).toFixed(1), (defeats / (defeats + victories) * 100).toFixed(1)],
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
        plugins: {
            legend: {
                position: 'bottom',
            }
        },
    };

    onMount(() => {
        if (victories != 0 || defeats != 0)
        {
            const ctx = document.getElementById('myChart').getContext('2d');
            chart = new Chart(ctx, {
                type: 'pie',
                data,
                options
            });
        }
    });

    onDestroy(() => {
        if (chart) {
            chart.destroy();
        }
    });
</script>

{#if victories != 0 || defeats != 0}
    <canvas id="myChart"></canvas>
{:else}
    <h5 class="text-center" style="color:grey;">No matchs played</h5>
{/if}
