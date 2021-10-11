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

import { ServerData, ServerMetaData} from './types'

// data to be sent to the POST request


export async function fetchServerData(window_size: number, start_time: number): Promise<ServerData> {
    const post_data = {
        window_size: window_size,
        start_time: start_time
      }
      
    const body = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(post_data)
    }

    const response = await fetch('http://' + window.location.host + '/api/get_data', body)

    if (!response.ok) {
        return Promise.reject('Could not fetch data from the server: ' + response.statusText)
    }

    const jsonResponse = await response.json()
    
    const data: ServerData = {
        eeg: jsonResponse.eeg ?? null,
        gsr: jsonResponse.gsr ?? null,
        ppg: jsonResponse.ppg ?? null,
        powerBands: jsonResponse.power_bands ?? null,
        deltaBand: jsonResponse.delta_band ?? null,
        thetaBand: jsonResponse.theta_band ?? null,
        alphaBand: jsonResponse.alpha_band ?? null,
        betaBand: jsonResponse.beta_band ?? null,
        gammaBand: jsonResponse.gamma_band ?? null,
        gsrPhasic: jsonResponse.gsr_phasic ?? null,
        gsrTonic: jsonResponse.gsr_tonic ?? null,
        hr: jsonResponse.hr ?? null,
        hrv: jsonResponse.hrv ?? null,
        breathingRate: jsonResponse.breathing_rate ?? null,
    }

    return data
}

export async function fetchServerMetadata(): Promise<ServerMetaData> {

    const response = await fetch('http://' + window.location.host + '/api/get_metadata')

    if (!response.ok) {
        return Promise.reject('Could not fetch data from the server: ' + response.statusText)
    }
    const jsonResponse = await response.json()
    const metadata: ServerMetaData = {
        dataLength: jsonResponse.data_length ?? null,
        enabledGraphs: jsonResponse.enabled_graphs ?? null,
        eegChannels: jsonResponse.eeg_channels ?? null,
        samplingRates: jsonResponse.sampling_rate ?? null
    }
    return metadata
}
