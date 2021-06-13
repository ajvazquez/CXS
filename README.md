# CXS338

The project CXS338 is a fork of [MIT Haystack's CorrelX](https://github.com/MITHaystack/CorrelX/) VLBI Correlator, developed by [A.J. Vazquez Alvarez](https://github.com/ajvazquez) on a postdoctoral research position at MIT Haystack back in 2015-2017.
The original project's main objectives were "scalability, flexibility and simplicity". This project aims at adding "performance" to that list.


This project (CXS338) starts as a migration of CorrelX to run on [Apache Spark](https://spark.apache.org/) as part of a Masters' Thesis on Big Data at UNED by this author in 2021, as a proof of concept with the following objectives:
* Simplifying architecture and usage (simplicity).
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
export SPARK_HOME=/home/aj/spark-3.0.2-bin-hadoop2.7
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

## Benchmark

### Dataset

The test data corresponds to the dataset described in "Prospects for Wideband VLBI Correlation in the Cloud", by Gill et al.,
published in Publications of the Astronomical Society of the Pacific, 131:124501 (13pp), 2019 October.

This dataset corresponds to 20 s of (assumed real data), 2 bits per sample, 1 channel and 2 polarizations, with a sampling frequency of 2 GHz (20 GB per station).
For this project, this data was generated with the script in ```examples/test_dataset_test/gen_test_file.py``` for 2 stations, and split into blocks of 100 MB with the script ```examples/test_dataset_test/aws/split_files.sh```
before uploading it to AWS S3.

### Procedure

Running a correlation on AWS EMR:

0. Generate the data and split it into blocks (multiple of the size of a VDIF frame) using the script ```examples/test_dataset_test/aws/split_files.sh```.
1. Create a cluster in AWS EMR, providing the bootstrap script in ```examples/test_dataset_test/aws/provision.sh```.
2. Upload the experiment folder to the master node, and the media files to S3.
3. Run the correlation.

### Results

Performance (processing rate) is calculated dividing the total data (40 GB) by the measured time and by the number of vCPUs (16).

```
              cluster             time      processing rate by single vCPU
DiFX-2.5.2    1x n1-highmem-16    2000 s    1.28 MB/s
CXS338        4x m4.xlarge        4309 s    0.59 MB/s
```

GCP n1-highmem-16:
* Processor: Intel Xeon @ 2.5 GHz. Virtual cores: 16.
* RAM: 104 GB.

AWS m4.xlarge:
* Processor: Intel Xeon E5-2676 v3 @ 2.4 GHz. Virtual cores: 4.
* RAM: 16 GB.

The following figure compares cluster sizes and total performance for the results shown above.

![Performance comparison](perf_comparison.png?raw=true "Performance Comparison")

## Deployment

### Packaging

Increase version in ```version.txt``` and then run:
```
python setup.py sdist
```

### Installation

```
virtualenv -p python3 venv3
source venv3/bin/activate
pip install pip install dist/cxs338-0.0.1.tar.gz
```

### Execution

```
cxs -c <path-to-cxs338.ini>
```

## Tests

For a precision comparison between CorrelX and DiFX please refer to the [CorrelX manual](https://github.com/MITHaystack/CorrelX/blob/master/correlx-user-developer-guide.pdf).

For a precision comparison between CXS338 and CorrelX please use the following tests:

```
cd src
source venv3/bin/activate
python -m unittest discover -s .
```

## Project Status

This project is a prototype / alpha. 
