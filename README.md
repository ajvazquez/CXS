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

This dataset corresponds to 20 s of (assumed real data), 2 bits per sample, 1 channel and 2 polarizations, with a sampling frequency of 4 GHz (40 GB per station).

For this project, this data was generated with the script in ```examples/test_dataset_test/gen_test_file.py``` for 2 stations, a sampling frequency of 2 GHz (20 GB per station), and split into blocks of 100 MB with the script ```examples/test_dataset_test/aws/split_files.sh```
before uploading it to AWS S3.

### Procedure

Running a correlation on AWS EMR:

0. Generate the data and split it into blocks (multiple of the size of a VDIF frame) using the script ```examples/test_dataset_test/aws/split_files.sh```.
1. Create a cluster in AWS EMR, providing the bootstrap script in ```examples/test_dataset_test/aws/provision.sh```.
2. Upload the experiment folder to the master node, and the media files to S3.
3. Run the correlation.

### Results

Performance (processing rate) is calculated dividing the total data by the measured time and by the number of vCPUs (16).

```
              cluster             data     time      processing rate by single vCPU
DiFX-2.5.2    1x n1-highmem-16    80 GB    2000 s    2.56 MB/s
CXS338        4x m4.xlarge        40 GB    4309 s    0.59 MB/s
```

GCP n1-highmem-16:
* Processor: Intel Xeon @ 2.5 GHz. Virtual cores: 16.
* RAM: 104 GB.

AWS m4.xlarge:
* Processor: Intel Xeon E5-2676 v3 @ 2.4 GHz. Virtual cores: 4.
* RAM: 16 GB.

The following figure compares cluster sizes and total performance for the results shown above.

![Performance comparison](perf_comparison.png?raw=true "Performance Comparison")

### Notes about partitioned reading

The previous benchmark takes files pre-partitioned for CXS. Since [60c1e7](https://github.com/ajvazquez/CXS338/commit/60c1e7ee04dbab3ac2da5069d9d76156652e2475) this splitting is no longer necessary as it is possible to configure the block size for automatic partitioned reading, see for example [this configuration](examples/test_dataset_test/sub/cxs338.ini), where the "Spark input files" parameter is defined as a comma separated list of pairs file-path@block-size (in bytes).

### Notes about output generation

Options running CXS:
- Default: generates output distributedly in executors and finally joins it into a single file in the driver (recommended if single node or with filesystem shared by executors).
- No merge ("-n"): same as default but skipping the last merge step, output in executors.
- Single file ("-s"): relies on Spark for the merge in the driver (does not require a shared file system but may be prone to OOM).

## Deployment

### Installation from package

For packaging, increase version in ```version.txt``` and then run:
```
python setup.py sdist
```

For installation:
```
virtualenv -p python3 venv3
source venv3/bin/activate
pip install dist/cxs338-0.0.1.tar.gz
```

### Installation from repository

Installing directly from github:
```
python3 -m venv venv3
venv3/bin/pip install -e git+https://github.com/ajvazquez/CXS338.git@master#egg=CXS338
```

## Execution

```
cxs -c <path-to-cxs338.ini>
```


## Processing Chain

Integration with existing processing chains using dockerized tools can be seen in 
[VLBI correlation docker tools](https://github.com/ajvazquez/VLBI-Correlation-Docker-Tools).


## Development Environment

For setting up a simple development environment the runners ```d-cxp-dev``` and ```d-cxs-dev``` 
from [VLBI correlation docker tools](https://github.com/ajvazquez/VLBI-Correlation-Docker-Tools) can be used, overwriting the path to the 
sources folder in the run_dev.sh scripts.


## Tests

For a precision comparison between CorrelX and DiFX please refer to the [CorrelX manual](https://github.com/MITHaystack/CorrelX/blob/master/correlx-user-developer-guide.pdf).

For a precision comparison between CXS338 and CorrelX please use the following tests:

```
cd src
source venv3/bin/activate
python -m unittest discover -s .
```

## Project Status

This project is a prototype (alpha), only intended for development/testing.
