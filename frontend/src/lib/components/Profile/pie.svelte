<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { Chart } from 'chart.js/auto';

    let chart : any;

    export let victories = 0;
    export let defeats = 0;

    const data = {
        labels: ['Victory (%)', 'Defeat (%)'],
        datasets: [{
            data: [(victories / (defeats + victories) * 100).toFixed(1), (defeats / (defeats + victories) * 100).toFixed(1)],
            borderColor: [
                '#f8f9fa',
                '#f8f9fa'
                
            ],
            backgroundColor: [
                'rgba(13, 110, 253, 1)',
                'rgba(220, 53, 69, 1)',
            ],
            borderWidth: 3
        }]
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                display: false
            }
        },
    };

    onMount(() => {
        if (victories != 0 || defeats != 0)
        {
            const canvas : any = document.getElementById('myChart');
            const ctx = canvas.getContext('2d');
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
