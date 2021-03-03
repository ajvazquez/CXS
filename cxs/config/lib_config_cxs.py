"""
Management of CXS configuration files.
"""

from __future__ import print_function
import os
if os.environ.get("is_legacy"):
    from const_config import *
else:
    from const_config_cxs import *

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
    

def get_configuration(file_log, config_file, v=0):
    """
    Read parameters from configuration file "configh.conf".
    
    Parameters
    ----------
     file_log : handler to file
         handler to log file.
     config_file : str
         path to CorrelX configuration file.
     timestamp_str : str
         suffix to be added to temporary data folder (hwere media will be split).
     v : int
         verbose if 1.
     
    Returns
    -------
     FFT_AT_MAPPER : bool
         Boolean, if 0 FFT is done at reducer (default).
     DATA_DIR : str
         Path with media input files.
     INI_FOLDER : str
         Folder with experiment .ini files.
     INI_STATIONS : str
         Stations ini file name.
     INI_SOURCES : str
         Sources ini file name.
     INI_DELAY_MODEL : str
         Delay model ini file name.
     INI_DELAYS : str
         Delay polynomials ini file name.
     INI_MEDIA : str
         Media ini file name.
     INI_CORRELATION : str
         Correlation ini file name.
     INTERNAL_LOG_MAPPER
         [remove] currently default 0.
     INTERNAL_LOG_REDUCER
         [remove] currenlty default 0.
     FFTS_PER_CHUNK
        [Remove] Number of DFT windows per mapper output, -1 by default (whole frame)
     ONE_BASELINE_PER_TASK : int
        0 by default (if 1, old implementation allowed scaling with one baseline per task in the reducers).
     MIN_MAPPER_CHUNK
        [Remove] Chunk constraints for mapper (-1).
     MAX_MAPPER_CHUNK
        [Remove] Chunk constraints for mapper (-1).
     TASK_SCALING_STATIONS: int
        0 by default (if 1, old implementation allowed linear scaling per task in the reducers).

    Notes
    -----
    |
    | **Configuration:**
    |
    |  All constants taken from const_config.py and const_hadoop.py.
    |
    |
    | **TO DO:**
    |
    |  OVER_SLURM: explain better, and check assumptions.
    |  Remove INTERNAL_LOG_MAPPER and INTERNAL_LOG_REDUCER.
    |  Remove FFTS_PER_CHUNK,MIN_MAPPER_CHUNK and MAX_MAPPER_CHUNK.
    |  Check that SINGLE_PRECISION is followed in mapper and reducer.
    """
    
   
    #config_file="configh.conf"
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(config_file)

    INTERNAL_LOG_MAPPER =    0                                                                # TO DO: remove
    INTERNAL_LOG_REDUCER =   0                                                                # TO DO: remove

    if v==1:
        print("\nReading configuration file...",file=file_log)    

    # Misc (Hadoop-other in legacy)
    FFT_AT_MAPPER =          config.getboolean( C_CONF_MISC, C_CONF_OTHER_FFT_MAP)
    ONE_BASELINE_PER_TASK =  config.getboolean( C_CONF_MISC, C_CONF_OTHER_ONE_BASELINE)
    TASK_SCALING_STATIONS =  config.getboolean( C_CONF_MISC, C_CONF_OTHER_SCALING_STATIONS)
    SINGLE_PRECISION =       config.getboolean( C_CONF_MISC, C_CONF_OTHER_SINGLE_PRECISION)
    FFTS_PER_CHUNK =         -1                                                                # TO DO: remove
    MIN_MAPPER_CHUNK =       -1                                                                # TO DO: remove
    MAX_MAPPER_CHUNK =       -1                                                                # TO DO: remove
    
    
    
    # Experiment
    INI_FOLDER =                         config.get(   C_CONF_EXP, C_CONF_EXP_FOLDER)
    INI_STATIONS = INI_FOLDER + "/" +    config.get(   C_CONF_EXP, C_CONF_EXP_STATIONS)
    INI_SOURCES = INI_FOLDER + "/" +     config.get(   C_CONF_EXP, C_CONF_EXP_SOURCES)
    INI_DELAYS = INI_FOLDER + "/" +      config.get(   C_CONF_EXP, C_CONF_EXP_DELAYS)
    INI_DELAY_MODEL = INI_FOLDER + "/" + config.get(   C_CONF_EXP, C_CONF_EXP_DELAY_MODEL)
    INI_MEDIA = INI_FOLDER + "/" +       config.get(   C_CONF_EXP, C_CONF_EXP_MEDIA)
    INI_CORRELATION = INI_FOLDER + "/" + config.get(   C_CONF_EXP, C_CONF_EXP_CORRELATION)
    DATA_DIR = INI_FOLDER + "/" +        config.get(   C_CONF_EXP, C_CONF_EXP_MEDIA_SUB) + "/"

    config = ConfigCXS(
        fft_at_mapper=FFT_AT_MAPPER,
        data_dir=DATA_DIR,
        ini_folder=INI_FOLDER,
        ini_stations=INI_STATIONS,
        ini_sources=INI_SOURCES,
        ini_delay_model=INI_DELAY_MODEL,
        ini_delays=INI_DELAYS,
        ini_media=INI_MEDIA,
        ini_correlation=INI_CORRELATION,
        internal_log_mapper=INTERNAL_LOG_MAPPER,
        internal_log_reducer=INTERNAL_LOG_REDUCER,
        ffts_per_chunk=FFTS_PER_CHUNK,
        one_baseline_per_task=ONE_BASELINE_PER_TASK,
        min_mapper_chunk=MIN_MAPPER_CHUNK,
        max_mapper_chunk=MAX_MAPPER_CHUNK,
        task_scaling_stations=TASK_SCALING_STATIONS,
        single_precision=SINGLE_PRECISION,
    )
    return config
