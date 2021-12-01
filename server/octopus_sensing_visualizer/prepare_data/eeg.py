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
import datetime
import pandas as pd
import numpy as np

from scipy.signal import welch
from scipy.integrate import simps

# TODO Acelerometer, topomap, fft plot, time-frequency


def prepare_eeg_data(path: str):
    '''
    Reads EEG csv file and return its data

    @param str path: EEG file path
    
    @rtype: numpy.array, numpy.array

    @return: EEG data, channel names
    '''
    print(path)
    df = pd.read_csv(path, index_col=False)
    data = df.to_numpy()
    channels = df.head()
    return np.transpose(data), channels


def prepare_power_bands(eeg_data: np.array, sampling_rate: int, window_size: int, overlap: int):
    '''
    Split data to some windows and calculates EEG bandpowers for each window

    @param numpy.array eeg_data: A 2D array of EEG signal (samples * channels)
    @param int sampling_rate: EEG sampling rate
    @param int window_size : The size of desired window for extracting power bands
    @param int overlap: The amount of overlap between two subsequent window

    @rtype: dict{band_power_label: band_power}
    @note: output keys: ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
    @type: band_power: numpy.array
    @return: a dictionary of power bands
    '''
    eeg_data = np.transpose(eeg_data)
    samples, channels = eeg_data.shape

    eeg_bands = {'Delta': (0, 4),
                 'Theta': (4, 8),
                 'Alpha': (8, 12),
                 'Beta': (12, 30),
                 'Gamma': (30, 45)}

    delta = []
    theta = []
    alpha = []
    beta = []
    gamma = []
    start_time = 0
    signal_length = int(samples/sampling_rate)  # Length of signal in seconds
    if (start_time + window_size) > (samples/sampling_rate):
        raise Exception("Desired window are out of data range")
    while (start_time + window_size) < (samples/sampling_rate):
        extracted_data = \
            eeg_data[start_time*sampling_rate:(start_time+window_size)*sampling_rate, :]
        power_bands = \
            _get_total_power_bands(extracted_data, sampling_rate, eeg_bands)
        delta.append(power_bands["Delta"])
        theta.append(power_bands["Theta"])
        alpha.append(power_bands["Alpha"])
        beta.append(power_bands["Beta"])
        gamma.append(power_bands["Gamma"])
        start_time += (window_size - overlap)

    delta_band = np.zeros(signal_length)
    delta_band[0:window_size-1] = np.nan
    delta_band[window_size-1:signal_length-1] = np.array(delta)

    theta_band = np.zeros(signal_length)
    theta_band[0:window_size-1] = np.nan
    theta_band[window_size-1:signal_length-1] = np.array(theta)

    alpha_band = np.zeros(signal_length)
    alpha_band[0:window_size-1] = np.nan
    alpha_band[window_size-1:signal_length-1] = np.array(alpha)

    beta_band = np.zeros(signal_length)
    beta_band[0:window_size-1] = np.nan
    beta_band[window_size-1:signal_length-1] = np.array(beta)

    gamma_band = np.zeros(signal_length)
    gamma_band[0:window_size-1] = np.nan
    gamma_band[window_size-1:signal_length-1] = np.array(gamma)

    power_bands = {'Delta': delta_band,
                   'Theta': theta_band,
                   'Alpha': alpha_band,
                   'Beta': beta_band,
                   'Gamma': gamma_band}
    return power_bands


def prepare_power_bands_on_the_fly(data, sampling_rate, start_time, length, eeg_bands=None):
    '''
    Calculates power bands for a specified window of data

    @param numpy.array data: a two dimentional array.
    @note data: Each column is a channels. Shape should be time_points*channels

    @param int sampling_rate: EEG sampling rate
    @param int start_time: start time in second of the window for measuring
                           power bands
    @param int length: Length of window in second

    @keyword dict eeg_bands: a dictionary of desired power bands
    @type eeg_bands: dict{str: tuple(int, int)}
    @note: default value is None. When it is None, extracted power band will be:
           {'Delta': (0, 4),
            'Theta': (4, 8),
            'Alpha': (8, 12),
            'Beta': (12, 30),
            'Gamma': (30, 45)}

    @rtype numpy.array
    @return: an array of power bands
    @note: Default is [Delta, Theta, Alpha, Beta, Gamma]
    '''
    if eeg_bands is None:
        # Define EEG bands
        eeg_bands = {'Delta': [0.5, 4],
                     'Theta': [4, 8],
                     'Alpha': [8, 12],
                     'Beta': [12, 30],
                     'Gamma': [30, 45]}
    power_bands = {}
    for key, value in eeg_bands.items():
        extracted_data = data[:, start_time*sampling_rate:(start_time+length)*sampling_rate]
        sum_band_power = 0
        for ch in range(extracted_data.shape[0]):
            band_power = \
                bandpower(extracted_data[ch, :], sampling_rate, value, relative=True)
            sum_band_power += band_power
        power_bands[key] = sum_band_power/extracted_data.shape[0]
    return power_bands


def prepare_power_bands_on_the_fly0(data, sampling_rate, start_time, length, eeg_bands=None):
    '''
    Calculate power bands

    @param numpy.array data: a two dimentional array.
    @note data: Each column is a channels. Shape should be time_points*channels

    @param int sampling_rate: EEG sampling rate
    @param int start_time: start time in second of the window for measuring
                           power bands
    @param int length: Length of window in second

    @keyword dict eeg_bands: a dictionary of desired power bands
    @type eeg_bands: dict{str: tuple(int, int)}
    @note: default value is None. When it is None, extracted power band will be:
           {'Delta': (0, 4),
            'Theta': (4, 8),
            'Alpha': (8, 12),
            'Beta': (12, 30),
            'Gamma': (30, 45)}

    @rtype numpy.array
    @return: an array of power bands
    @note: Default is [Delta, Theta, Alpha, Beta, Gamma]
    '''
    if eeg_bands is None:
        # Define EEG bands
        eeg_bands = {'Delta': (0, 4),
                     'Theta': (4, 8),
                     'Alpha': (8, 12),
                     'Beta': (12, 30),
                     'Gamma': (30, 45)}
    extracted_data = data[:, start_time*sampling_rate:(start_time+length)*sampling_rate]        
    power_bands = _get_total_power_bands(extracted_data, sampling_rate, eeg_bands)
    return power_bands

def _get_power_bands(signal: np.ndarray, sampling_rate: int, eeg_bands: dict):
    sample_count, = signal.shape
    # Get real amplitudes of FFT (only in postive frequencies)
    fft_values = np.absolute(np.fft.rfft(signal))

    # Get frequencies for amplitudes in Hz
    fft_freq = np.fft.rfftfreq(sample_count, 1.0/sampling_rate)

    eeg_band_fft = dict()
    for band in eeg_bands:
        freq_ix = np.where((fft_freq >= eeg_bands[band][0]) &
                           (fft_freq < eeg_bands[band][1]))[0]

        if(fft_values[freq_ix].size == 0):
            eeg_band_fft[band] = 0
        else:
            eeg_band_fft[band] = np.mean(fft_values[freq_ix])

    return eeg_band_fft


def _get_total_power_bands(data: np.ndarray, sampling_rate: int, eeg_bands: dict):
    '''
    calculates alpha, betha, delta, gamma bands for each channel
    It uses fft

    @param numpy.array data: EEG data
    @param int sampling_rate: sampling rete

    @rtype numpy.arraye(np.array(float)), shape is channel_count * 5
    @return an array of power bands for all channels
    '''
    columns, samples = data.shape
    ch = 0
    alpha = []
    beta = []
    delta = []
    theta = []
    gamma = []
    while ch < columns:
        power_band = _get_power_bands(data[ch, :], sampling_rate, eeg_bands)
        ch += 1
        alpha.append(power_band["Alpha"])
        beta.append(power_band["Beta"])
        delta.append(power_band["Delta"])
        theta.append(power_band["Theta"])
        gamma.append(power_band["Gamma"])
    power_bands = \
        {"Delta": np.mean(np.array(delta)),
         "Theta": np.mean(np.array(theta)),
         "Alpha": np.mean(np.array(alpha)),
         "Beta": np.mean(np.array(beta)),
         "Gamma": np.mean(np.array(gamma))}
    print(power_bands)
    return power_bands

def bandpower(data: np.ndarray, sampling_rate:int, band: list, window_sec: int=None, relative: bool=False):
    '''
    Computes the average power of the signal x in a specific frequency band.

    Parameters
    ----------
    @param np.array data: Input signal in the time-domain.
    @param float sampling_rate : Sampling frequency of the data.
    @param list band : Lower and upper frequencies of the band of interest.

    @keyword float window_sec : Length of each window in seconds.
    @note: If None, window_sec = (1 / min(band)) * 2
    @keyword boolean relative : If True, return the relative power (= divided by the total power of the signal).
        If False (default), return the absolute power.

    @rtype: float
    @return bp : Absolute or relative band power.
    '''
    band = np.asarray(band)
    low, high = band

    # Define window length
    if window_sec is not None:
        nperseg = window_sec * sampling_rate
    else:
        nperseg = (2 / low) * sampling_rate

    # Compute the modified periodogram (Welch)
    freqs, psd = welch(data, sampling_rate, nperseg=nperseg)

    # Frequency resolution
    freq_res = freqs[1] - freqs[0]

    # Find closest indices of band in frequency vector
    idx_band = np.logical_and(freqs >= low, freqs <= high)

    # Integral approximation of the spectrum using Simpson's rule.
    bp = simps(psd[idx_band], dx=freq_res)

    if relative:
        bp /= simps(psd, dx=freq_res)
    return bp



if __name__ == "__main__":
    path = "/tmp/preprocess/new/OpenBCI-20-00-01.csv"
    a = datetime.datetime.now()
    bands = prepare_power_bands_on_the_fly(path, 128, 5, 5)
    b = datetime.datetime.now()
    print(bands)
    print(b - a)
