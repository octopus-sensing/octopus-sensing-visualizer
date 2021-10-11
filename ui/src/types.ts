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

import {Chart} from 'chart.js'

export type ServerData = {
    eeg?: number[][]
    gsr?: number[]
    ppg?: number[]
    deltaBand?: number[]
    thetaBand?: number[]
    alphaBand?: number[]
    betaBand?: number[]
    gammaBand?: number[]
    powerBands?: number[]
    gsrPhasic?: number[]
    gsrTonic?: number[]
    hr?: Array<number | null>
    hrv?: Array<number | null>
    breathingRate?: Array<number | null>
}

export type ServerMetaData = {
    dataLength: number
    enabledGraphs: string[]
    eegChannels: string[] | null
    samplingRates: number[]
}


export type Charts = {
    eeg: Chart[] | null
    gsr: Chart | null
    ppg: Chart | null
    deltaBand: Chart | null
    thetaBand: Chart | null
    alphaBand: Chart | null
    betaBand: Chart | null
    gammaBand: Chart | null
    powerBands: Chart | null
    gsrPhasic: Chart | null
    gsrTonic: Chart | null
    hr: Chart | null
    hrv: Chart | null
    breathingRate: Chart | null
}
