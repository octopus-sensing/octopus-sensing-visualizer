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
import json
from typing import Optional
import os
import configparser
import cherrypy
from octopus_sensing_visualizer.prepare_data.eeg import prepare_eeg_data, prepare_power_bands, prepare_power_bands_on_the_fly
from octopus_sensing_visualizer.prepare_data.gsr import prepare_gsr_data, prepare_phasic_tonic
from octopus_sensing_visualizer.prepare_data.ppg import prepare_ppg_data, prepare_ppg_components


class RootHandler():
    pass


class EndPoint():
    def __init__(self, config_file_path=None):

        self.data = {}
        self.sampling_rate = {}
        self.data_length = 0
        self.eeg_channels = []
        self.__power_bands = []
        if not os.path.isfile(config_file_path):
            raise Exception("File path is incorrect")

        # Load the configuration file
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read(config_file_path)

        for section in config.sections():
            if section == "EEG":
                self._load_eeg_data(config)
            if section == "PPG":
                self._load_ppg_data(config)
            if section == "GSR":
                self._load_gsr_data(config)

    def _load_eeg_data(self, config):
        eeg_path = config.get('EEG', 'path')
        eeg_sampling_rate = config.getint('EEG', 'sampling_rate')
        if not os.path.isfile(eeg_path):
            raise Exception("EEG file path is not valid")
        eeg_data, eeg_channels = prepare_eeg_data(eeg_path)
        self.eeg_channels = eeg_channels
        channels, samples = eeg_data.shape
        self.data_length = (samples/eeg_sampling_rate)
        if config.getboolean('EEG', 'display_signal') is True:
            self.data["eeg"] = eeg_data
            self.sampling_rate["eeg"] = eeg_sampling_rate

        if config.getboolean('EEG', 'display_alpha_signal') is True or \
           config.getboolean('EEG', 'display_beta_signal') is True or \
           config.getboolean('EEG', 'display_gamma_signal') is True or \
           config.getboolean('EEG', 'display_theta_signal') is True or \
           config.getboolean('EEG', 'display_delta_signal') is True:
            config_window_size = config.getint('EEG', 'window_size')
            overlap = config.getint('EEG', 'overlap')
            if config_window_size < 1:
                raise Exception("Window size should be equal or bigger than 1 seconds")
            if overlap > config_window_size:
                raise Exception("overlap should be smaller than window size")

            power_bands = \
                prepare_power_bands(eeg_data,
                                    eeg_sampling_rate,
                                    config_window_size,
                                    overlap)
            if config.getboolean('EEG', 'display_alpha_signal') is True:
                self.data["alpha_band"] = power_bands["Alpha"]
                self.sampling_rate["alpha_band"] = 1
            if config.getboolean('EEG', 'display_beta_signal') is True:
                self.data["beta_band"] = power_bands["Beta"]
                self.sampling_rate["beta_band"] = 1
            if config.getboolean('EEG', 'display_gamma_signal') is True:
                self.data["gamma_band"] = power_bands["Gamma"]
                self.sampling_rate["gamma_band"] = 1
            if config.getboolean('EEG', 'display_theta_signal') is True:
                self.data["theta_band"] = power_bands["Theta"]
                self.sampling_rate["theta_band"] = 1
            if config.getboolean('EEG', 'display_delta_signal') is True:
                self.data["delta_band"] = power_bands["Delta"]
                self.sampling_rate["delta_band"] = 1
            
        if config.getboolean('EEG', 'display_power_band_bars') is True:
            # Later we will measure power bands based on this data and sampling rate
            self.data["power_bands"] = eeg_data
            self.sampling_rate["power_bands"] = eeg_sampling_rate


    def _load_gsr_data(self, config):
        gsr_path = config.get('GSR', 'path')
        gsr_sampling_rate = config.getint('GSR', 'sampling_rate')
        if not os.path.isfile(gsr_path):
            raise Exception("GSR file path is not valid")
        gsr_data = prepare_gsr_data(gsr_path)
        samples, = gsr_data.shape
        self.data_length = (samples/gsr_sampling_rate)
        if config.getboolean('GSR', 'display_signal') is True:
            self.data["gsr"] = gsr_data
            self.sampling_rate["gsr"] = gsr_sampling_rate

        if config.getboolean('GSR', 'display_phasic') is True or \
           config.getboolean('GSR', 'display_tonic') is True:
            phasic, tonic = \
                prepare_phasic_tonic(gsr_data, gsr_sampling_rate)
            if config.getboolean('GSR', 'display_phasic') is True:
                self.data["gsr_phasic"] = phasic
                self.sampling_rate["gsr_phasic"] = gsr_sampling_rate
            if config.getboolean('GSR', 'display_tonic') is True:
                self.data["gsr_tonic"] = tonic
                self.sampling_rate["gsr_tonic"] = gsr_sampling_rate

    def _load_ppg_data(self, config):
        ppg_path = config.get('PPG', 'path')
        ppg_sampling_rate = config.getint('PPG', 'sampling_rate')
        if not os.path.isfile(ppg_path):
            raise Exception("PPG file path is not valid")
        ppg_data = prepare_ppg_data(ppg_path)
        samples, = ppg_data.shape
        self.data_length = (samples/ppg_sampling_rate)
        if config.getboolean('PPG', 'display_signal') is True:
            self.data["ppg"] = ppg_data
            self.sampling_rate["ppg"] = ppg_sampling_rate

        if config.getboolean('PPG', 'display_hr') is True or \
           config.getboolean('PPG', 'display_hrv') is True or \
           config.getboolean('PPG', 'display_breathing_rate') is True:
            window_size = config.getint('PPG', 'window_size')
            overlap = config.getint('PPG', 'overlap')
            hr_components = \
                prepare_ppg_components(ppg_data, ppg_sampling_rate,
                                       window_size=window_size,
                                       overlap=overlap)
            if config.getboolean('PPG', 'display_hr') is True:
                self.data["hr"] = hr_components["hr"]
                self.sampling_rate["hr"] = 1
            if config.getboolean('PPG', 'display_hrv') is True:
                self.data["hrv"] = hr_components["hrv"]
                self.sampling_rate["hrv"] = 1
            if config.getboolean('PPG', 'display_breathing_rate') is True:
                self.data["breathing_rate"] = hr_components["breathing_rate"]
                self.sampling_rate["breathing_rate"] = 1
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def get_data(self):
        body = cherrypy.request.json
        start_time: Optional[int] = body.get('start_time')
        window_size: Optional[int] = body.get('window_size')
        if start_time is None or window_size is None:
            raise ValueError("Both 'start_time' and 'window_size' params are mandatory")

        output = {}
        for key, value in self.data.items():
            sampling_rate = self.sampling_rate[key]
            start = start_time*sampling_rate
            end = (start_time+window_size)*sampling_rate
            if key == "eeg":
                output[key] = \
                    value[:, start:end].tolist()
            elif key == "power_bands":
                power_bands = \
                    prepare_power_bands_on_the_fly(value,
                                                   self.sampling_rate[key],
                                                   start_time,
                                                   window_size)
                output[key] = power_bands
                print(power_bands)

            else:
                output[key] = \
                    value[start:end].tolist()
        json_out = json.dumps(output)
        json_out = json_out.replace("NaN", "null")
        return json_out

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_metadata(self):
        metadata = {}
        metadata["enabled_graphs"] = list(self.data.keys())
        metadata["data_length"] = self.data_length
        metadata["sampling_rates"] = self.sampling_rate
        if "eeg" in list(self.data.keys()):
            metadata["eeg_channels"] = list(self.eeg_channels)
        return metadata


if __name__ == "__main__":
    end_point = EndPoint("server/octopus_sensing_visualizer/config.conf")
    output = end_point.get_data(10, 3)
    print(end_point.sampling_rate.keys())
    print(len(output['ppg']))
    print(output["alpha_band"])
