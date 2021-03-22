import time
import os
# legacy
#from lib_config import get_configuration
from config.lib_config_cxs import get_configuration
from config.lib_ini_exper import process_ini_files
from config.lib_ini_files import get_all_values_serial, C_INI_MEDIA_CHANNELS, \
    serial_params_to_array, INI_VEC
from app.map.msvf import fun_mapper
from app.reduce.rsvf import fun_reducer
from app.base.const_mapred import KEY_SEP


class CXworker(object):

    config_gen = None
    config_ini = None
    num_partitions = None
    num_accs = None
    num_channels = None
    out_file = None

    def read_config(self, config_file):
        v = 0
        #timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        file_log = None

        config_gen = get_configuration(v=v, config_file=config_file, file_log=file_log)
        config_ini = process_ini_files(config_gen.data_dir,
                                       config_gen.ini_stations,
                                       config_gen.ini_sources,
                                       config_gen.ini_delay_model,
                                       config_gen.ini_delays,
                                       config_gen.ini_media,
                                       config_gen.ini_correlation,
                                       config_gen.one_baseline_per_task,
                                       return_config_obj=True,
                                       v=v)
        return [config_gen, config_ini]

    def get_partitions_info(self):
        params_media = serial_params_to_array(self.config_ini.media_serial_str)
        ch_v = get_all_values_serial(params_media,C_INI_MEDIA_CHANNELS)
        channels = []
        for ch in ch_v:
            channels.extend(ch.split(INI_VEC))
        channels = list(set(channels))
        num_channels = len(channels)
        s_duration = float(self.config_ini.signal_duration)
        acc_time = float(self.config_ini.accumulation_time)
        num_accs = int(-(s_duration//-acc_time))
        num_partitions = num_accs * num_channels
        print("Partitions: {} (accs: {}, channels: {})".format(num_partitions, num_accs, num_channels))
        return [num_partitions, num_accs, num_channels]

    def __init__(self, config_file="cxs338.ini"):
        self.config_gen, self.config_ini = self.read_config(config_file=config_file)
        self.num_partitions, self.num_accs, self.num_channels = self.get_partitions_info()

    def init_out(self):
        out_sub_dir = "s" + time.strftime("%Y%m%d_%H%M%S")
        out_dir = self.config_gen.out_dir+out_sub_dir
        os.mkdir(out_dir)
        self.out_dir = out_dir
        self.out_file = out_dir + "/{}_s0_v0.out".format(self.config_gen.out_prefix)

    def mapper(self, f_input, f_name):
        return fun_mapper(self.config_gen, self.config_ini, f_input, f_name)

    def reducer(self, lines):
        # TODO: consider removing
        lines = list(sorted(lines, key=lambda x: x.split(KEY_SEP[0])))
        return fun_reducer(self.config_gen, self.config_ini, lines)
