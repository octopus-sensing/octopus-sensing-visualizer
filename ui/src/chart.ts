import { Chart, LineController, LinearScale, Title, CategoryScale, PointElement, LineElement } from 'chart.js'

import type { Charts } from './types'

export const charts: Charts = {
    gsr: null,
    ppg: null,
    eeg: null,
}

export function makeChart(id: string, color: string): Chart {
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
        },
        data: {
            labels: [],
            datasets: [
                {
                    label: id,
                    data: [],
                    fill: false,
                    borderColor: color,
                },
            ],
        },
    })
}

export function updateChart(chart: Chart, data: number[]) {
    if (!chart.data.datasets) {
        throw new Error("in updateChart: 'chart.data.datasets' is undefined! Should never happen!")
    }

    chart.data.datasets[0].data = data

    const labels = Array(data.length)
    for (let idx = 0; idx < data.length; idx++) {
        labels[idx] = idx
    }
    chart.data.labels = labels

    // 'none': disables update animation
    chart.update('none')
}

export function clearCharts() {

    if (charts.eeg != null){
        charts.eeg.forEach(channelChart => updateChart(channelChart, []))
    }

    if (charts.gsr != null){
        updateChart(charts.gsr, [])
    } 

    if(charts.ppg != null){
        updateChart(charts.ppg, [])
    }
}

export function createCharts(enabledGraphs: Array<string>){
    if (enabledGraphs.some(x=> x=="gsr")){
        const gsr_chart = makeChart('gsr', '#44d7a3')
        charts.gsr = gsr_chart
    }

    if (enabledGraphs.some(x=> x=="ppg")){
        const ppg_chart = makeChart('ppg', '#d74493')
        charts.ppg = ppg_chart
    }

    if (enabledGraphs.some(x=> x=="eeg")){
        const eeg_charts = Array(16)
        for (let idx = 0; idx < 16; idx++) {
            const id = 'eeg-' + idx
            eeg_charts[idx] = makeChart(id, '#44a3d7')
        }
        charts.eeg = eeg_charts
    }

    
}