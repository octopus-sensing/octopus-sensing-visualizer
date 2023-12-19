import { Chart } from 'chart.js'

import type { Charts } from './types'

export const charts: Charts = {
    gsr: null,
    ppg: null,
    eeg: null,
    deltaBand: null,
    thetaBand: null,
    alphaBand: null,
    betaBand: null,
    gammaBand: null,
    powerBands: null,
    gsrPhasic: null,
    gsrTonic: null,
    hr: null,
    hrv: null,
    breathingRate: null,
}

export function makeLineChart(id: string, color: string, autoSkipPadding = 100): Chart {
    const canvas = document.getElementById(id) as HTMLCanvasElement
    const ctx = canvas.getContext('2d')

    if (!ctx) {
        throw new Error('Context of the Canvas is null!')
    }

    return new Chart(ctx, {
        type: 'line',
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: {
                tooltip: { enabled: false },
                legend: { display: false },
            },
            scales: {
                x: {
                    ticks: {
                        autoSkip: true,
                        autoSkipPadding: autoSkipPadding,
                    },
                },
            },
        },

        data: {
            labels: [],
            datasets: [
                {
                    label: id,
                    data: [],
                    fill: true,
                    borderColor: color,
                    pointStyle: 'circle',
                    pointRadius: 0.4,
                },
            ],
        },
    })
}

export function makeBarChart(id: string, color: string): Chart {
    const canvas = document.getElementById(id) as HTMLCanvasElement
    const ctx = canvas.getContext('2d')

    if (!ctx) {
        throw new Error('Context of the Canvas is null!')
    }

    return new Chart(ctx, {
        type: 'bar',

        data: {
            labels: [],
            datasets: [
                {
                    label: id,
                    data: [],
                    borderColor: color,
                    backgroundColor: color,
                },
            ],
        },
    })
}

export function updateChart(chart: Chart, data: Array<number | null>, time: number): void {
    if (!chart.data.datasets) {
        throw new Error("in updateChart: 'chart.data.datasets' is undefined! Should never happen!")
    }
    chart.data.datasets[0].data = data

    const labels = Array(data.length)
    for (let idx = 0; idx < data.length; idx++) {
        labels[idx] = (idx / 128 + time).toFixed(2)
    }
    chart.data.labels = labels

    // 'none': disables update animation
    chart.update('none')
}

export function clearCharts(): void {
    let key: keyof Charts
    for (key in charts) {
        if (charts[key] === charts.eeg) {
            if (charts.eeg != null) {
                charts.eeg.forEach((channelChart) => updateChart(channelChart, [], 0))
            }
        } else {
            if (charts[key] != null) {
                const chart = charts[key] as Chart
                updateChart(chart, [], 0)
            }
        }
    }
}

export function createCharts(enabledGraphs: Array<string>): void {
    if (enabledGraphs.some((x) => x == 'gsr')) {
        const gsrChart = makeLineChart('gsr', '#44d7a3')
        charts.gsr = gsrChart
    }

    if (enabledGraphs.some((x) => x == 'ppg')) {
        const ppgChart = makeLineChart('ppg', '#d74493')
        charts.ppg = ppgChart
    }

    if (enabledGraphs.some((x) => x == 'eeg')) {
        const eegCharts = Array(16)
        for (let idx = 0; idx < 16; idx++) {
            const id = 'eeg-' + idx
            eegCharts[idx] = makeLineChart(id, '#44a3d7')
        }
        charts.eeg = eegCharts
    }

    if (enabledGraphs.some((x) => x == 'delta_band')) {
        const deltaChart = makeLineChart('delta_band', '#44a3d7')
        charts.deltaBand = deltaChart
    }

    if (enabledGraphs.some((x) => x == 'theta_band')) {
        const thetaChart = makeLineChart('theta_band', '#44a3d7')
        charts.thetaBand = thetaChart
    }

    if (enabledGraphs.some((x) => x == 'alpha_band')) {
        const alphaChart = makeLineChart('alpha_band', '#44a3d7')
        charts.alphaBand = alphaChart
    }

    if (enabledGraphs.some((x) => x == 'beta_band')) {
        const betaChart = makeLineChart('beta_band', '#44a3d7')
        charts.betaBand = betaChart
    }

    if (enabledGraphs.some((x) => x == 'gamma_band')) {
        const gammaChart = makeLineChart('gamma_band', '#44a3d7')
        charts.gammaBand = gammaChart
    }

    if (enabledGraphs.some((x) => x == 'power_bands')) {
        const powerBandsCahrt = makeBarChart('power_bands', '#44a3d7')
        charts.powerBands = powerBandsCahrt
    }

    if (enabledGraphs.some((x) => x == 'gsr_phasic')) {
        const phasicChart = makeLineChart('gsr_phasic', '#44d7a3')
        charts.gsrPhasic = phasicChart
    }

    if (enabledGraphs.some((x) => x == 'gsr_tonic')) {
        const tonicChart = makeLineChart('gsr_tonic', '#44d7a3')
        charts.gsrTonic = tonicChart
    }

    if (enabledGraphs.some((x) => x == 'hr')) {
        const hr = makeLineChart('hr', '#d74493')
        charts.hr = hr
    }
    if (enabledGraphs.some((x) => x == 'hrv')) {
        const hrv = makeLineChart('hrv', '#d74493')
        charts.hrv = hrv
    }

    if (enabledGraphs.some((x) => x == 'breathing_rate')) {
        const breathingRateChart = makeLineChart('breathing_rate', '#d74493', 0)
        charts.breathingRate = breathingRateChart
    }
}
