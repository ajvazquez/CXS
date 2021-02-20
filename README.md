# CXS338

The project CXS338 is a fork of [MIT Haystack's CorrelX](https://github.com/MITHaystack/CorrelX/) VLBI Correlator, developed by [ajvazquez](https://github.com/ajvazquez) on a postdoctoral research position at MIT Haystack back in 2015-2017.

This project (CXS338) starts as a migration of CorrelX to run on Spark as part of a Masters' Thesis on Big Data by this author in 2021, as a proof of concept with the following objectives:
* Migration from python2 to python3.
* Migration from Hadoop to Spark.
* Running a test correlation on a cloud computing service.

## Versions

About the naming convention:
* CXH227: CorrelX on Hadoop 2, Python 2.7 ([CorrelX legacy](https://github.com/MITHaystack/CorrelX/)).
* CXS338: CorrelX on Spark 3, Python 3.8.

## Configuration

```
cd src
virtualenv -p python3 venv3
source venv3/bin/activate
pip install -r ../requirements.txt
```


## Tests

```
cd src
source venv3/bin/activate
python -m unittest discover -s .
```