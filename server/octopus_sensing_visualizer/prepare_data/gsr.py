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
from neurokit.bio.bio_eda import eda_process


def prepare_gsr_data(path: str):
    '''
    Return GSR data saved in the specified path

    @param str path: path to GSR file

    @rtype: np.array (shape: samples)

    @return an array of GSR signal
    '''
    df = pd.read_csv(path, index_col=False, header=None)
    data = df.to_numpy()
    return data[:, 0]


def prepare_phasic_tonic(gsr_data: np.ndarray, sampling_rate: int):
    '''
    Extract Pahsic and Tonic components from GSR data saved in the specified path

    @param np.array gsr_data: GSR data
    @param int sampling_rate: sampling rate

    @rtype: tuple(np.array, np.array)
    @note: Phasic, Tonic (shape: samples)

    @return Phasic and Tonic signals
    '''
    processed_eda = eda_process(gsr_data, sampling_rate=sampling_rate)
    eda = processed_eda['df']
    phasic = eda["EDA_Phasic"]
    tonic = eda["EDA_Tonic"]
    return np.array(phasic), np.array(tonic)
