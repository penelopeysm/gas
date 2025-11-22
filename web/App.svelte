<script lang="ts">
    import { onMount } from "svelte";
    import Chart from "chart.js/auto";
    import Readings from "./Readings.svelte";
    import Usage from "./Usage.svelte";
    import { DateTime } from "luxon";

    let start_date = $state(DateTime.now().minus({ weeks: 2 }).toISODate());
    let end_date = $state(DateTime.now().toISODate());

    let start_date_datetime = $derived(DateTime.fromISO(start_date));
    let end_date_datetime = $derived(DateTime.fromISO(end_date));

    onMount(() => {
        Chart.defaults.font.size = 14;
        Chart.defaults.font.family = "'Commissioner', sans-serif";
    });
</script>

<div id="app">
    <main>
        <div id="date-picker">
            <div id="date-inputs">
                <div id="start-date-div">
                    <label for="start">Start date:</label>
                    <input
                        type="date"
                        id="start"
                        name="start-date"
                        bind:value={start_date}
                        min="2025-03-16"
                        max={end_date}
                    />
                </div>
                <div id="end-date-div">
                    <label for="end">End date:</label>
                    <input
                        type="date"
                        id="end"
                        name="end-date"
                        bind:value={end_date}
                        min={start_date}
                        max={DateTime.now().toISODate()}
                    />
                </div>
            </div>
            <div id="quick-buttons">
                Or select:
                <button
                    onclick={() => {
                        end_date = DateTime.now().toISODate();
                        start_date = DateTime.now()
                            .minus({ days: 7 })
                            .toISODate();
                    }}
                >
                    last 7d
                </button>
                <button
                    onclick={() => {
                        end_date = DateTime.now().toISODate();
                        start_date = DateTime.now()
                            .minus({ weeks: 2 })
                            .toISODate();
                    }}
                >
                    last 2w
                </button>
                <button
                    onclick={() => {
                        end_date = DateTime.now().toISODate();
                        start_date = DateTime.now()
                            .minus({ months: 1 })
                            .toISODate();
                    }}
                >
                    last 1m
                </button>
                <button
                    onclick={() => {
                        end_date = DateTime.now().toISODate();
                        start_date = DateTime.now()
                            .minus({ months: 6 })
                            .toISODate();
                    }}
                >
                    last 6m
                </button>
                <button
                    onclick={() => {
                        end_date = DateTime.now().toISODate();
                        start_date = "2025-03-16";
                    }}
                >
                    all time
                </button>
            </div>
        </div>

        <div id="graphs">
            <div>
                <h1>Daily usage / cost</h1>
                <p>
                    Each 'day' actually runs from 6 a.m. to 6 a.m. the next day
                    (this is to avoid inconsistencies based on my sleeping
                    time). Note that costs are only estimated; there are weird
                    oddities to do with conversion from m³ to kWh and also
                    tariff changes.
                </p>
                <Usage {start_date_datetime} {end_date_datetime} />
            </div>

            <div>
                <h1>Cumulative readings</h1>
                <Readings {start_date_datetime} {end_date_datetime} />
            </div>
        </div>
    </main>
</div>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Commissioner:wght@100..900&display=swap");

    div#app {
        height: 100vh;
        width: 100vw;
        font-family: "Commissioner", sans-serif;
    }

    main {
        width: 80%;
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    div#date-picker {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 1rem;
    }

    div#date-inputs {
        display: flex;
        gap: 3rem;

        label {
            margin-right: 0.5rem;
        }
        input {
            font-family: inherit;
            font-size: 1rem;
        }
    }

    div#quick-buttons {
        display: flex;
        align-items: center;
        gap: 0.5rem;

        button {
            font-family: inherit;
            font-size: 0.9rem;
            padding: 0.2rem 0.5rem;
            border: 1px solid #ccc;
            border-radius: 4px;
            background-color: #f9f9f9;
            cursor: pointer;
        }

        button:hover {
            background-color: #e0e0e0;
        }
    }

    div#graphs {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-top: 1rem;
    }
</style>
