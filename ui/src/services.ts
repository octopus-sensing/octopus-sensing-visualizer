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

import { ServerData } from './types'

// data to be sent to the POST request


export async function fetchGraphs(window_size: number, start_time: number): Promise<ServerData> {
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

    return response.json()
}

export async function fetchDataLength(): Promise<ServerData> {

    const response = await fetch('http://' + window.location.host + '/api/get_data_length')

    if (!response.ok) {
        return Promise.reject('Could not fetch data from the server: ' + response.statusText)
    }

    return response.json()
}

export async function fetchEnabledGraphs(): Promise<ServerData> {

    const response = await fetch('http://' + window.location.host + '/api/get_enabled_graphs')

    if (!response.ok) {
        return Promise.reject('Could not fetch data from the server: ' + response.statusText)
    }

    return response.json()
}