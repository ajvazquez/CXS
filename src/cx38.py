import time
from lib_config import get_configuration
from lib_ini_exper import process_ini_files
from msvf import fun_mapper
from rsvf import fun_reducer
from const_mapred import KEY_SEP


class CXworker(object):

    def __init__(self, config_file="correlx.ini"):
        self.config_gen, self.config_ini = self.read_config(config_file=config_file)

    def read_config(self, config_file):
        v = 0
        timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        file_log = None

        config_gen = get_configuration(v=v, config_file=config_file, timestamp_str=timestamp_str, file_log=file_log,
                                       return_conf_obj=True)
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

    def mapper(self, f_input, f_name):
        return fun_mapper(self.config_gen, self.config_ini, f_input, f_name)

    def reducer(self, lines):
        # TODO: consider removing
        lines = list(sorted(lines, key=lambda x: x.split(KEY_SEP[0])))
        return fun_reducer(self.config_gen, self.config_ini, lines)
