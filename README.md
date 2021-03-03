# CXS338

The project CXS338 is a fork of [MIT Haystack's CorrelX](https://github.com/MITHaystack/CorrelX/) VLBI Correlator, developed by [ajvazquez](https://github.com/ajvazquez) on a postdoctoral research position at MIT Haystack back in 2015-2017.
The original project's main objectives were "scalability, flexibility and simplicity".


This project (CXS338) starts as a migration of CorrelX to run on [Apache Spark](https://spark.apache.org/) as part of a Masters' Thesis on Big Data at UNED by this author in 2021, as a proof of concept with the following objectives:
* Simplifying usage (simplicity).
* Migrating from Python 2 to Python 3 (flexibility).
* Migrating from Hadoop to Spark (performance).
* Running a test correlation on a cloud computing service (scalability).

## Versions

About the naming convention:
* CXH227: CorrelX on Hadoop 2, Python 2.7 ([CorrelX legacy](https://github.com/MITHaystack/CorrelX/)).
* CXPL38: CorrelX on Pipeline, Python 3.8.
* CXS338: CorrelX on Spark 3, Python 3.8.

## Configuration

Download Apache Spark 3.0.2 pre-built for Apache Hadoop 2.7:
```
wget https://ftp.cixug.es/apache/spark/spark-3.0.2/spark-3.0.2-bin-hadoop2.7.tgz
tar -xvzf spark-3.0.2-bin-hadoop2.7
```

Create environment and install requirements:
```
cd src
virtualenv -p python3 venv3
source venv3/bin/activate
pip install -r ../requirements.txt
```
Add the following lines to venv3/bin/activate (replace the path as required):
```
export SPARK_HOME=/home/cxuser/spark-3.0.2-bin-hadoop2.7
export PYTHONPATH=$PYTHONPATH:`pwd`/src
export PYTHONPATH=$PYTHONPATH:`pwd`/cxs
```
Reactivate environment:
```
source venv3/bin/activate
```

## Basic Correlation

### Pipeline
```
bash examples/run_example_vgos.sh
```
### Hadoop
```
bash sh/configure_hadoop_cx.sh
bash examples/run_example_vgos_hadoop.sh
```
### Spark
```
bash sh/run_example_vgos_spark.sh
```

### Time Comparison
The following times are for the previous examples running on a single host with minimal configuration.
```
                    real    reported   notes
CXPL27 (pipeline)    15 s    7 s
CXPL38 (pipeline)    16 s    8 s
CXH227 (hadoop)     247 s   64 s       (24.6 hdfs in, 2.6 hdfs out, 36.6 hadoop-1s-8v)
CXS338 (spark)       16 s   16 s
```


## Tests

```
cd src
source venv3/bin/activate
python -m unittest discover -s .
```