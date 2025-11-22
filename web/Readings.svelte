<script lang="ts">
    // create a mapping of date to number (is this the best structure?)
    import readingsJson from "./data/readings.json";
    import { onMount } from "svelte";
    import { DateTime } from "luxon";
    import Chart from "chart.js/auto";
    import "chartjs-adapter-luxon";

    let { start_date_datetime, end_date_datetime } = $props();

    let readings = new Map<DateTime, number>();
    for (const entry of readingsJson) {
        const date = DateTime.fromISO(entry.datetime);
        const value = entry.reading;
        readings.set(date, value);
    }
    console.log(readings);

    let chart: Chart;
    $effect(() => {
        updateChart(start_date_datetime, end_date_datetime);
    });

    function updateChart(start: DateTime, end: DateTime) {
        console.log("updating reading chart range");
        if (chart) {
            chart.options.scales.x.min = start.toJSDate();
            chart.options.scales.x.max = end.toJSDate();
            console.log(chart.options.scales.x);
            chart.update();
        }
    }

    let canvas: HTMLCanvasElement;
    onMount(() => {
        chart = new Chart(canvas, {
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
                        time: {
                            minUnit: "day",
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
        updateChart(start_date_datetime, end_date_datetime);
    });
</script>

<canvas class="plot" bind:this={canvas}></canvas>

<style>
    .plot {
        max-height: 500px;
        background-color: #ffffff;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        padding: 16px;
    }
</style>
