#!/usr/bin/env python3
import time
import os
import glob
from pathlib import Path
import shutil
import argparse
from cxs.parallel.spark.lib_spark import CXSworker


def run_spark_task(config_file, keep=False, debug_partitions=False, save_txt=False):
    start_time = time.time()
    cxs = CXSworker(config_file=config_file,
                    debug_partitions=debug_partitions,
                    save_txt_only=save_txt)

    sc = cxs.start_spark(spark_config_pairs=cxs.config_gen.spark_config_pairs,
                         spark_home=cxs.config_gen.spark_home)

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
    print("Done.")


def run_checks(config_file):
    cxs = CXSworker(config_file=config_file)
    cxs.run_checks()



def main():
    cparser = argparse.ArgumentParser(description='CXS338')

    cparser.add_argument('-c', action="store", \
                         dest="configuration_file", required=True, \
                         help="Specify a configuration file.")

    cparser.add_argument('--check', action="store_true", \
                         dest="check", default=False, \
                         help="Check configuration (does not run correlation).")

    cparser.add_argument('-k', action="store", type=int, \
                         dest="keep", default=None, \
                         help="Number of minutes to keep Spark session open.")

    cparser.add_argument('-n', action="store_false", \
                         dest="no_merge", default=False, \
                         help="Do not merge output files.")

    cparser.add_argument('-d', action="store_true", \
                         dest="save_driver", default=False, \
                         help="Save as single file to driver (Spark collect).")

    cparser.add_argument('-v', action="store_true", \
                         dest="verbose", default=False, \
                         help="Verbose.")

    args = cparser.parse_args()
    config_file = args.configuration_file
    keep = args.keep
    save_txt = not args.save_driver
    group_output = not args.no_merge
    verbose = args.verbose

    error = None
    if not os.path.exists(config_file):
        error = "Configuration file {} does not exist".format(config_file)
        print("ERROR: {}".format(error))

    if not error and args.check:
        run_checks(config_file)
        error = "Check run"

    if not error:
        run_spark_task(config_file, keep, verbose, save_txt)


if __name__ == '__main__':
    main()
