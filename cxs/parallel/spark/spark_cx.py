import time
import os
import glob
from pathlib import Path
import shutil
from parallel.spark.lib_spark import CXSworker
import argparse


DEFAULT_CONFIG = "/home/aj/work/cx_git/CorrelX/conf/cxs338.ini"


start_time = time.time()


def run_spark_task(config_file, keep=False):
    cxs = CXSworker(config_file=config_file)

    sc = cxs.start_spark(spark_config_pairs=cxs.config_gen.spark_config_pairs)

    cxs.run(sc)

    try:
        if keep:
            end_time = time.time()
            print("Elapsed: {}".format(end_time - start_time))
            keep_m = 60*keep
            print("Keeping Spark session open for {} minutes".format(keep_m))
            time.sleep(keep_m)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        cxs.stop_spark(sc)

    if not keep:
        end_time = time.time()
        print("Elapsed: {}".format(end_time-start_time))

    print("Merging output...")

    with open(cxs.out_file, 'wb') as fod:
        for f in glob.glob(cxs.out_dir+"/sub_*.out"):
            with open(f, 'rb') as fd:
                shutil.copyfileobj(fd, fod)
    print("Done.")


def run_checks(config_file):
    cxs = CXSworker(config_file=config_file)
    cxs.run_checks()



def main():
    cparser = argparse.ArgumentParser(description='CXS338')

    cparser.add_argument('-c', action="store", \
                         dest="configuration_file", default=DEFAULT_CONFIG, \
                         help="Specify a configuration file.")

    cparser.add_argument('--check', action="store_true", \
                         dest="check", default=False, \
                         help="Check configuration (does not run correlation).")

    cparser.add_argument('-k', action="store", type=int, \
                         dest="keep", default=None, \
                         help="Number of minutes to keep Spark session open.")

    args = cparser.parse_args()
    config_file = args.configuration_file
    keep = args.keep

    error = None
    if not os.path.exists(config_file):
        error = "Configuration file {} does not exist".format(config_file)
        print("ERROR: {}".format(error))

    if not error and args.check:
        run_checks(config_file)
        error = "Check run"

    if not error:
        run_spark_task(config_file, keep)


if __name__ == '__main__':
    main()
