import time
import os
from pathlib import Path
from parallel.spark.lib_spark import CXSworker
import argparse


DEFAULT_CONFIG = "/home/aj/work/cx_git/CorrelX/conf/cxs338.ini"


start_time = time.time()


def run_spark_task(config_file):
    cxs = CXSworker(config_file=config_file)

    sc = cxs.start_spark()
    cxs.run(sc)
    cxs.stop_spark(sc)

    Path(cxs.out_file).touch()


    end_time = time.time()
    print("Elapsed: {}".format(end_time-start_time))


def main():
    cparser = argparse.ArgumentParser(description='CXS338')

    cparser.add_argument('-c', action="store", \
                         dest="configuration_file",default=DEFAULT_CONFIG, \
                         help="Specify a configuration file.")

    args = cparser.parse_args()
    config_file = args.configuration_file

    error = None
    if not os.path.exists(config_file):
        error = "Configuration file {} does not exist".format(config_file)
        print("ERROR: {}".format(error))

    if not error:
        run_spark_task(config_file)


if __name__ == '__main__':
    main()
