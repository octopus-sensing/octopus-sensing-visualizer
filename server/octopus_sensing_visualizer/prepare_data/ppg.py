# This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
# Copyright © Nastaran Saffaryazdi 2021
#
# Octopus Sensing Visualizer is a free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
#  either version 3 of the License, or (at your option) any later version.
#
# Octopus Sensing Visualizer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Octopus Sensing Visualizer.
# If not, see <https://www.gnu.org/licenses/>.

import pandas as pd
import numpy as np
import heartpy as hp
import matplotlib.pyplot as plt


def display_signal(signal):
    plt.plot(signal)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.show()


def prepare_ppg_data(path: str):
    '''
    Return PPG data saved in the specified path

    @param str path: path to PPG file

    @rtype: np.array (shape: samples)

    @return an array of PPG signal
    '''
    df = pd.read_csv(path, index_col=False, header=None)
    data = df.to_numpy()
    return data[:, 0]


def prepare_ppg_components(ppg_data: np.ndarray, sampling_rate: int,
                           window_size: int = 20, overlap: int = 19):
    '''
    Extracts HR, HRV and breathing rate from PPG

    @param np.array ppg_data: PPG data
    @param int sampling_rate: PPG sampling rate

    @keyword int window_length: Length of sliding window for measurment in seconds
    @keyword float overlap: Amount of overlap between two windows in seconds

    @rtype: dict(str, numpy.array)
    @note: dict.keys = ["hr", "hrv", "breathing_rate"]

    @return a dictionary of PPG components
    '''

    data = hp.filter_signal(ppg_data,
                            [0.7, 2.5],
                            sample_rate=sampling_rate,
                            order=3,
                            filtertype='bandpass')
    print(sampling_rate, data.shape)
    wd, m = hp.process_segmentwise(data,
                                   sample_rate=sampling_rate,
                                   segment_width=window_size,
                                   segment_overlap=overlap/window_size)

    signal_length = (data.shape[0] / sampling_rate)
    hr = np.zeros(int(signal_length))

    hr[0:window_size-1] = np.nan
    hr[window_size-1:int(signal_length)-1] = np.array(m['bpm'])

    hrv = np.zeros(int(signal_length))
    hrv[0:window_size-1] = np.nan
    hrv[window_size-1:int(signal_length)-1] = np.array(m['sdsd'])

    breathing_rate = np.zeros(int(signal_length))
    breathing_rate[0:window_size-1] = np.nan
    breathing_rate[window_size-1:int(signal_length)-1] = np.array(m['breathingrate'])

    hr_components = {"hr": hr,
                     "hrv": hrv,
                     "breathing_rate": breathing_rate}

    return hr_components
