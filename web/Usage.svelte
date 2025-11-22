<script lang="ts">
    // create a mapping of date to number (is this the best structure?)
    import usageJson from "./data/daily_usage.json";
    import { onMount } from "svelte";
    import { DateTime } from "luxon";
    import Chart from "chart.js/auto";
    import "chartjs-adapter-luxon";

    let { start_date_datetime, end_date_datetime } = $props();
    console.log(start_date_datetime, end_date_datetime);

    let isUsageView = $state(true);

    const STANDING_CHARGE = 28.52; // p/day
    const UNIT_RATE_KWH = 6.03; // p/kWh
    const KWH_PER_M3 = 11.13541333;
    const UNIT_RATE_M3 = UNIT_RATE_KWH * KWH_PER_M3;

    function make_data(start: DateTime, end: DateTime) {
        let usage = new Map<DateTime, number>();
        for (const entry of usageJson) {
            const date = DateTime.fromISO(entry.date);
            if (date < start || date > end) {
                continue;
            }
            if (isUsageView) {
                usage.set(date, entry.usage);
            } else {
                usage.set(
                    date,
                    (entry.usage * UNIT_RATE_M3 + STANDING_CHARGE) / 100,
                );
            }
        }
        console.log(usage);
        return usage;
    }

    let chart: Chart;
    let usage = make_data(start_date_datetime, end_date_datetime);
    $effect(() => {
        console.log("updating usage data");
        usage = make_data(start_date_datetime, end_date_datetime);
        console.log(usage);
        if (chart) updateChart(usage);
    });

    function updateChart(usage: Map<DateTime, number>) {
        if (chart) {
            chart.data.labels = Array.from(usage.keys());
            chart.data.datasets[0].data = Array.from(usage.values());
            chart.options.scales.y.title.text = isUsageView
                ? "Usage (m³)"
                : "Cost (£)";
            chart.options.scales.y.ticks = isUsageView
                ? {}
                : {
                      callback: function (value) {
                          return value.toFixed(2);
                      },
                  };
            chart.update();
        }
    }

    let canvas: HTMLCanvasElement;
    onMount(() => {
        chart = new Chart(canvas, {
            type: "bar",
            data: {
                labels: Array.from(usage.keys()),
                datasets: [
                    {
                        data: Array.from(usage.values()),
                        borderColor: "rgba(75, 192, 192, 1)",
                        backgroundColor: "rgba(75, 192, 192, 0.2)",
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
        updateChart(usage);
    });
</script>

<input
    type="radio"
    id="usage"
    name="view"
    bind:group={isUsageView}
    value={true}
/>
<label for="usage">Usage</label>
<input
    type="radio"
    id="cost"
    name="view"
    bind:group={isUsageView}
    value={false}
/>
<label for="cost">Cost</label>
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
