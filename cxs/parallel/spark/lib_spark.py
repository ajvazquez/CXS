
"""
# Add this to env activate
export SPARK_HOME=/home/aj/work/tfm/spark-3.0.1-bin-hadoop2.7
export PYTHONPATH=$PYTHONPATH:`pwd`/cxs
"""
import io
import time
import findspark
from pyspark.sql import SparkSession
from pyspark import SparkConf
from app.base.const_mapred import KEY_SEP, FIELD_SEP, SF_SEP
from app.cx38 import CXworker

class CXSworker(CXworker):

    @staticmethod
    def start_spark(app_name=None, spark_config_pairs=None):
        if app_name is None:
            app_name = "s" + time.strftime("%Y%m%d_%H%M%S")
        findspark.init()
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

    def __init__(self, config_file):

        super().__init__(config_file=config_file)
        self.init_out()

    def read_input_files(self, sc):
        return sc.binaryFiles(self.config_gen.data_dir)

    def process_file(self, rdd):
       f_name = rdd[0].split("/")[-1]
       f = io.BytesIO(rdd[1])
       #print("Processing file: {}".format(f_name))
       return self.mapper(f, f_name)

    def reduce_lines(self, rdd):
        return self.reducer(rdd[1])

    def write_output(self, data):
        with open(self.out_file, "w") as f_out:
            for x in data.collect():
                print(x, file=f_out)

    def run(self, sc):
        def fun_sort(x):
            def sort_list(x):
                return x.split(KEY_SEP)[0].replace(SF_SEP, FIELD_SEP).split(FIELD_SEP)
            return (x[0], list(sorted(x[1], key=sort_list)))

        files = self.read_input_files(sc)
        data = files.flatMap(lambda rdd:self.process_file(rdd))
        data_grouped = data.reduceByKey(lambda x, y: x+y)
        data_sorted = data_grouped.map(fun_sort)
        data_reduced = data_sorted.flatMap(lambda rdd:self.reduce_lines(rdd))
        self.write_output(data_reduced)
