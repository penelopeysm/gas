<script lang="ts">
    import readingsJson from "./readings.json";
    import Chart from "chart.js/auto";
    import "chartjs-adapter-date-fns";
    import { onMount } from "svelte";

    let time = $state("all");

    // create a mapping of date to number (is this the best structure?)
    let readings = new Map<Date, number>();
    for (const entry of readingsJson) {
        const date = new Date(entry.timestamp);
        const value = entry.reading;
        readings.set(date, value);
    }
    console.log(readings);

    let lineCanvas: HTMLCanvasElement;
    onMount(() => {
        Chart.defaults.font.size = 14;
        Chart.defaults.font.family = "'Commissioner', sans-serif";

        new Chart(lineCanvas, {
            type: "line",
            data: {
                labels: Array.from(readings.keys()),
                datasets: [
                    {
                        data: Array.from(readings.values()),
                        borderColor: "rgba(75, 192, 192, 1)",
                        backgroundColor: "rgba(75, 192, 192, 0.2)",
                        fill: true,
                        tension: 0.1,
                    },
                ],
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: "time",
                        title: {
                            display: true,
                            text: "Date",
                            font: {
                                size: 18,
                            },
                        },
                    },
                    y: {
                        title: {
                            display: true,
                            text: "Gas reading (m³)",
                            font: {
                                size: 18,
                            },
                        },
                    },
                },
                plugins: {
                    legend: {
                        display: false,
                    },
                },
            },
        });
    });
</script>

<div id="app">
    <main>
        <h1>Actual readings</h1>
        <canvas class="plot" bind:this={lineCanvas}></canvas>
    </main>
</div>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Commissioner:wght@100..900&display=swap");

    div#app {
        height: 100vh;
        width: 100vw;
        font-family: 'Commissioner', sans-serif;
    }

    main {
        width: 80%;
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .plot {
        max-height: 500px;
        background-color: #ffffff;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        padding: 16px;
    }
</style>
