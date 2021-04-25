
C_CONF_MISC = "Misc"
C_CONF_OTHER_FFT_MAP =          'FFT at mapper'
C_CONF_OTHER_ONE_BASELINE =     'One baseline per task'
C_CONF_OTHER_SCALING_STATIONS = 'Task scaling stations'
C_CONF_OTHER_SINGLE_PRECISION = 'Single precision'


C_CONF_EXP =                    "Experiment"
C_CONF_EXP_FOLDER =             'Experiment folder'
C_CONF_EXP_STATIONS =           'Stations file'
C_CONF_EXP_SOURCES =            'Sources file'
C_CONF_EXP_EOP =                'EOP file'
C_CONF_EXP_DELAYS =             'Delays file'
C_CONF_EXP_DELAY_MODEL =        'Delay model file'
C_CONF_EXP_MEDIA =              'Media file'
C_CONF_EXP_CORRELATION =        'Correlation file'
#C_CONF_EXP_MEDIA_SUB =          'Media sub-folder'
C_CONF_EXP_MEDIA_SPARK =        'Spark input files'
C_CONF_EXP_MEDIA_SUB_PREFIX =   'Output sub-folder prefix'


C_CONF_FILES =                  "Files"
C_CONF_FILES_SPARK_HOME_DIR =   'Spark home'
C_CONF_FILES_OUT_DIR =          'Output directory'
C_CONF_FILES_PREFIX_OUTPUT =    'Prefix for output'

C_CONF_SPARK =                  "Spark"


class ConfigCXS(object):

    def __init__(self,
                 fft_at_mapper,
                 data_dir,
                 ini_folder,
                 ini_stations,
                 ini_sources,
                 ini_delay_model,
                 ini_delays,
                 ini_media,
                 ini_correlation,
                 internal_log_mapper,
                 internal_log_reducer,
                 ffts_per_chunk,
                 one_baseline_per_task,
                 min_mapper_chunk,
                 max_mapper_chunk,
                 task_scaling_stations,
                 single_precision,
                 out_dir,
                 out_prefix,
                 spark_config_pairs,
                 spark_home
                 ):

        self.fft_at_mapper = fft_at_mapper
        self.data_dir = data_dir
        self.ini_folder = ini_folder
        self.ini_stations = ini_stations
        self.ini_sources = ini_sources
        self.ini_delay_model = ini_delay_model
        self.ini_delays = ini_delays
        self.ini_media = ini_media
        self.ini_correlation = ini_correlation
        self.internal_log_mapper = internal_log_mapper
        self.internal_log_reducer = internal_log_reducer
        self.ffts_per_chunk = ffts_per_chunk
        self.one_baseline_per_task = one_baseline_per_task
        self.min_mapper_chunk = min_mapper_chunk
        self.max_mapper_chunk = max_mapper_chunk
        self.task_scaling_stations = task_scaling_stations
        self.single_precision = single_precision
        self.out_dir = out_dir
        self.out_prefix = out_prefix
        self.spark_config_pairs = spark_config_pairs
        self.spark_home = spark_home
