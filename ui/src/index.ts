/* This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
* Copyright © Nastaran Saffaryazdi 2021
*
* Octopus Sensing Visualizer is a free software: you can redistribute it and/or modify it under the
* terms of the GNU General Public License as published by the Free Software Foundation,
*  either version 3 of the License, or (at your option) any later version.
*
* Octopus Sensing Visualizer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
* without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
* See the GNU General Public License for more details.
*
 You should have received a copy of the GNU General Public License along with Octopus Sensing Visualizer.
* If not, see <https://www.gnu.org/licenses/>.
*/

import { Chart, LineController, LinearScale, Title, CategoryScale, PointElement, LineElement } from 'chart.js'

// To make Charts tree-shakeable, we need to register the components we're using.
Chart.register(LineController, LinearScale, Title, CategoryScale, PointElement, LineElement)

import { fetchGraphs, fetchDataLength, fetchEnabledGraphs } from './services'
import type { Charts } from './types'

const charts: Charts = {
    gsr: null,
    ppg: null,
    eeg: null,
}

function makeCanvas(id: string, htmlClass: string): string {
    return `
<div class="chart-container">
  <canvas id="${id}" class="${htmlClass}" />
</div>
`
}

export async function onSliderChange(sliderAmount: string) {
    // TODO: Draw messages in place of the chart when no data was available.
    const window_size = 5
    const start_time = Number.parseInt(sliderAmount)

    const data = await fetchGraphs(window_size, start_time)
    if (charts.eeg != null){
        if (data.eeg) {
            const eegData = data.eeg
            charts.eeg.forEach((chart: Chart, idx: number) => {
                if (eegData.length > idx) {
                    updateChart(chart, eegData[idx])
                } else {
                    console.error(
                        `Not enough data! charts: ${charts.eeg!.length} data: ${eegData.length}`,
                    )
                }
            })
        }
    }

    if (charts.gsr != null){
        if (data.gsr) {
            updateChart(charts.gsr, data.gsr)
        }
    } 

    if(charts.ppg != null){
        if (data.ppg) {
            updateChart(charts.ppg, data.ppg)
        }
    }

}

async function initSlider(){
    try {
        const dataLength = await fetchDataLength()
        const slider = document.getElementById("slider") as HTMLInputElement
        slider.value = "0"
        slider.min = "0"
        slider.max = dataLength.toString()
        slider.step = "1"
        slider.onchange = () => onSliderChange(slider.value)

    } catch (error) {
    // TODO: Show a notification or something
    console.error(error)
    }
}

function changeSliderValue()
{
    const slider = document.getElementById("slider") as HTMLInputElement
    var sliderAmount = Number.parseInt(slider.value)
    sliderAmount += 1
    slider.value = sliderAmount.toString()
    onSliderChange(slider.value)
    console.log(slider.value)
}

function makeChart(id: string, color: string): Chart {
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


function updateChart(chart: Chart, data: number[]) {
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

function createCharts(enabledGraphs: Array<string>){
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

async function makeHtml(enabledGraphs: Array<string>): Promise<string>{
    let pageHtml = '<div id="signal-container">'

    // TODO: Fix hard-coded 16, and add other charts
    if (enabledGraphs.some(x=> x=="gsr")){
        pageHtml += '<div class="title">GSR</div>'
        pageHtml += makeCanvas('gsr', 'gsr-chart')
    }

    if (enabledGraphs.some(x=> x=="ppg")){
        pageHtml += '<div class="title">PPG</div>'
        pageHtml += makeCanvas('ppg', 'ppg-chart')
    }
    if (enabledGraphs.some(x=> x=="eeg")){
        pageHtml += '<div class="title">EEG</div>'
        for (let idx = 0; idx < 16; idx++) {
            const id = 'eeg-' + idx
            pageHtml += makeCanvas(id, 'eeg-chart')
        }
    }

    pageHtml += '</div>'

    pageHtml += '<div id="others-container">'
    //pageHtml += '<div class="title">Camera</div>'
    //pageHtml += '<img id="webcam-image" src=""></img>'

    pageHtml += '</div>'


    return pageHtml
}

async function main() {
    const enabledGraphs = await fetchEnabledGraphs()
    const pageHtml = await makeHtml(enabledGraphs)
    
    const dataElement = document.getElementById('data-container')
    if (!dataElement) {
        throw new Error('Data element is null!')
    }

    dataElement.innerHTML = pageHtml
    createCharts(enabledGraphs)
    initSlider()

    setInterval(changeSliderValue, 1000)

}

main()