
"""
# Add this to env activate
export SPARK_HOME=/home/aj/work/tfm/spark-3.0.1-bin-hadoop2.7

export PYTHONPATH=$PYTHONPATH:`pwd`/src
"""
import time
start_time = time.time()


# find spark
import findspark
findspark.init()

# spark context
from pyspark.sql import SparkSession

#.config("spark.some.config.option", "some-value") \
spark = SparkSession \
    .builder \
    .appName("test app") \
    .getOrCreate()
sc = spark.sparkContext

# testbytesio
x = sc.binaryFiles("file:///home/aj/work/cx_git/CorrelX/examples/test_dataset_vgos/media/*.vdif")

import cx38
import io
w = cx38.CXworker(config_file="/home/aj/work/cx_git/CorrelX/conf/correlx.ini")

def process_file(rdd):
    f_name = rdd[0].split("/")[-1]
    f = io.BytesIO(rdd[1])
    print("Processing file: {}".format(f_name))
    return w.mapper(f, f_name)

def reduce_lines(rdd):
    return w.reducer(rdd[1])


x3 = x.flatMap(lambda rdd:process_file(rdd))

from const_mapred import KEY_SEP, FIELD_SEP, SF_SEP
def get_sort_vector(x):
    def to_int(y):
        if y.isnumeric():
            return int(y)
        else:
            return y
    v = x.split(KEY_SEP)[0].replace(SF_SEP, FIELD_SEP).split(FIELD_SEP)
    return v

def sort_list(x):
    v = x.split(KEY_SEP)[0].replace(SF_SEP, FIELD_SEP).split(FIELD_SEP)
    return v
def fun_sort(x):
    return (x[0], list(sorted(x[1], key=sort_list)))

x_group = x3.reduceByKey(lambda x, y: x+y)
# sort lines
x_group = x_group.map(fun_sort)
x4 = x_group.flatMap(lambda rdd:reduce_lines(rdd))

with open("test_out.txt","w") as f_out:
    for x in x4.collect():
        print(x, file=f_out)

sc.stop()

end_time = time.time()
print("Elapsed: {}".format(end_time-start_time))

