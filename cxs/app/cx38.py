import glob
import os
import time
# legacy
#from lib_config import get_configuration
from cxs.config.lib_config_cxs import get_configuration
from cxs.config.lib_ini_exper import process_ini_files
from cxs.config.lib_ini_files import get_all_values_serial, C_INI_MEDIA_CHANNELS, \
    serial_params_to_array, INI_VEC
from cxs.app.map.msvf import fun_mapper
from cxs.app.reduce.rsvf import fun_reducer
from cxs.app.base.const_mapred import KEY_SEP


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

    def config_for_partitioned_reading(self):
        config_data = None
        if "@" in self.config_gen.data_dir:
            config_data = [x.split("@") for x in self.config_gen.data_dir.split(",")]
            config_data = [[fpath, int(bsize)] for fpath, bsize in config_data]
        return config_data

    def get_read_partitions_info(self):
        config_partitioned_reading = self.config_for_partitioned_reading()
        if not config_partitioned_reading:
            data_dir = self.config_gen.data_dir
            if data_dir.startswith("file://"):
                data_dir = data_dir[7:]
            paths_files = glob.glob(data_dir)
            print("Partitions reading: {} (one reader per file)".format(len(paths_files)))
        else:
            try:
                total_blocks = 0
                paths_files = [x[0] for x in config_partitioned_reading]
                paths_files = [x[7:] if x.startswith("file://") else x for x in paths_files]
                for count in range(len(paths_files)):
                    config_partitioned_reading[count][0] = paths_files[count]
                blocks = [os.path.getsize(x[0])/x[1] for x in config_partitioned_reading]
                total_blocks = sum(blocks)
                if total_blocks - int(total_blocks) == 0:
                    total_blocks = int(total_blocks)
                print("Partitions reading: {} ({})".format(total_blocks, "+".join(list(map(str,blocks)))))
                for fpath, bsize in config_partitioned_reading:
                    num_blocks = os.path.getsize(fpath)/bsize
                    #print(" - {} -> block size={}, total blocks={}".format(fpath, bsize, num_blocks))
                    if num_blocks-num_blocks//1 != 0:
                        print("   + WARNING: non-integer number of blocks for {}".format(fpath))
            except:
                print("Partitions reading: ?")

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
        print("Partitions processing: {} (accs: {}, channels: {})".format(num_partitions, num_accs, num_channels))
        return [num_partitions, num_accs, num_channels]

    def __init__(self, config_file="cxs338.ini"):
        self.config_gen, self.config_ini = self.read_config(config_file=config_file)
        self.get_read_partitions_info()
        self.num_partitions, self.num_accs, self.num_channels = self.get_partitions_info()

    def init_out(self, raise_if_error=True):
        out_sub_dir = "s" + time.strftime("%Y%m%d_%H%M%S")
        out_dir = self.config_gen.out_dir+out_sub_dir
        try:
            os.makedirs(out_dir, exist_ok=True)
        except Exception as e:
            if raise_if_error:
                raise e
        self.out_dir = out_dir
        self.out_file = out_dir + "/{}_s0_v0.out".format(self.config_gen.out_prefix)

    def mapper(self, f_input, f_name):
        return fun_mapper(self.config_gen, self.config_ini, f_input, f_name)

    def reducer(self, lines):
        lines.sort(key=lambda x: x.split(KEY_SEP)[0])
        return fun_reducer(self.config_gen, self.config_ini, lines)

