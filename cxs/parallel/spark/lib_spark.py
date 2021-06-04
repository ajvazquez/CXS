
"""
# Add this to env activate
export SPARK_HOME=/home/aj/work/tfm/spark-3.0.1-bin-hadoop2.7
export PYTHONPATH=$PYTHONPATH:`pwd`/cxs
"""
import io
import os
import time
from cxs.app.cx38 import CXworker

SPARK_HOME = "SPARK_HOME"
# TODO: dynamic based on number of files/partitions
MIN_PARTITIONS = 1000


class CXSworker(CXworker):

    debug_spark_partitions = False

    @staticmethod
    def start_spark(app_name=None, spark_config_pairs=None, spark_home=None):

        import findspark
        findspark.init()
        from pyspark.sql import SparkSession
        from pyspark import SparkConf

        if spark_home:
            os.environ[SPARK_HOME] = spark_home
        if app_name is None:
            app_name = "s" + time.strftime("%Y%m%d_%H%M%S")
        spark = SparkSession.builder.appName(app_name)
        if spark_config_pairs:
            conf = SparkConf().setAll(spark_config_pairs)
            spark = spark.config(conf=conf)
        spark = spark.getOrCreate()
        # TODO: configurable for debug...
        #sc = spark.sparkContext
        #print(sc.getConf().toDebugString())
        return spark.sparkContext

    @staticmethod
    def stop_spark(sc):
        sc.stop()

    def __init__(self, config_file, debug_partitions=False, save_txt_only=True):

        super().__init__(config_file=config_file)
        self.debug_spark_partitions = debug_partitions
        self.save_txt_only = save_txt_only
        self.init_out(raise_if_error=not save_txt_only)

    def read_input_files(self, sc):
        #return sc.binaryFiles(self.config_gen.data_dir)
        return sc.binaryFiles(self.config_gen.data_dir, minPartitions=MIN_PARTITIONS)

    def process_file(self, rdd):
       f_name = rdd[0].split("/")[-1]
       f = io.BytesIO(rdd[1])
       #print("Processing file: {}".format(f_name))
       return self.mapper(f, f_name)

    def reduce_lines(self, rdd):
        return self.reducer(rdd[1])

    def write_output_full(self, data):
        with open(self.out_file, "w") as f_out:
            for x in data.collect():
                print(x, file=f_out)

    def run(self, sc):

        num_channels = self.num_channels
        def f_x(x):
            y = list(map(int,x.split("-")[-2:]))
            y = y[0]*num_channels+y[1]
            return y

        files = self.read_input_files(sc)
        data = files.flatMap(lambda rdd:self.process_file(rdd))
        self.print_partitions(data, "map")

        data_grouped = data.reduceByKey(lambda x, y: x+y, self.num_partitions)
        self.print_partitions(data_grouped, "group")

        data_sorted = data_grouped.repartitionAndSortWithinPartitions(self.num_partitions, f_x)
        self.print_partitions(data_sorted, "repartition")

        data_reduced = data_sorted.flatMap(lambda rdd:self.reduce_lines(rdd))
        if self.save_txt_only:
            data_reduced.saveAsTextFile(self.out_file)
        else:
            self.write_output_full(data_reduced)


    # Debug

    def print_partitions(self, df, extra=None):
        if self.debug_spark_partitions:
            if hasattr(df, "explain"):
                df.explain()
            if hasattr(df, "rdd"):
                rdd = df.rdd
                is_rdd = False
            else:
                rdd = df
                is_rdd = True

            if not extra:
                extra = ""
            else:
                extra = " {} ".format(extra)
            if is_rdd:
                extra += " [RDD]"
            else:
                extra += " [DF]"
            print("---------{}----------".format(extra))
            num_partitions = rdd.getNumPartitions()
            records = df.glom().map(len).collect()
            print("Total partitions: {}".format(num_partitions))
            print("Records per partition: {}".format(records))
            print("Partitioner: {}".format(rdd.partitioner))
            parts = rdd.glom().collect()
            i = 0
            j = 0
            for p in parts:
                print("Partition {}:".format(i))
                ps = []
                for r in p:
                    # print("Row {}:{}".format(j, r))
                    np = r[0]
                    if np not in ps:
                        ps.append(np)
                    j = j + 1
                print(ps)
                i = i + 1

    def run_checks(self):

        # TODO: refactor
        import os
        import glob
        from cxs.config.lib_ini_files import get_val_vector, C_INI_MEDIA_S_FILES, C_INI_MEDIA_LIST, serial_params_to_array, extract_data_media
        from cxs.iocx.readers.vdif.lib_vdif import get_vdif_stats

        params_media=serial_params_to_array(self.config_ini.media_serial_str)
        data_dir = self.config_gen.data_dir
        if data_dir.startswith("file://"):
            data_dir = data_dir[7:]
        input_files = get_val_vector(params_media,C_INI_MEDIA_S_FILES,C_INI_MEDIA_LIST)
        paths_files = glob.glob(data_dir)
        count_match = 0
        tot = len(paths_files)
        found = []
        count_errors = 0
        for path_file in paths_files:
            for filename in input_files:
                if filename == os.path.basename(path_file):
                    count_match += 1
                    x = extract_data_media(params_media, filename)
                    fs = x[-2]
                    try:
                        [v_stations, v_seconds, v_frames, v_sizes, total_size, v_bpsample, v_data_type, num_samples, channels] = get_vdif_stats(path_file, first_second_only=True, v=0, extended=True)
                        num_channels = channels[0]
                        num_samples = num_samples/num_channels
                        bps = v_bpsample[0]
                        num_samples = num_samples/bps
                        if v_data_type[0]:
                            num_samples = num_samples/2
                        seconds_in_frame_per_second = num_samples/fs
                        if not abs(seconds_in_frame_per_second-1)<1e-10:
                            dt = "complex" if v_data_type[0] else "real"
                            fs_est = num_samples
                            print("WARNING: {} has {} s/s ({} channels; {} frames/s; {} samples; deduced fs: {:.2e} Hz; configured fs: {:.2e} Hz)".format(path_file, seconds_in_frame_per_second, num_channels, len(v_frames), dt, fs_est, fs))
                            count_errors += 1

                        # TODO: check channels and threads configured in media.ini

                        found.append(path_file)
                    except:
                        print("ERROR: cannot access input file {}".format(path_file))
                        count_errors += 1
        not_found = [x for x in paths_files if x not in found]
        if not count_match == tot:
            print("ERROR: could not find some input files: {}".format(", ".join(not_found)))
        else:
            print("OK: checked access to all input files: {}".format(", ".join(found)))
        if not count_errors:
            print("OK: proper configuration for media")
