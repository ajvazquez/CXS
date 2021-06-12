#!/bin/bash

aws s3 cp s3://aj-bucket-test/emr/exp.zip /home/hadoop/
mkdir /home/hadoop/exp
unzip /home/hadoop/exp.zip -d /home/hadoop/

source /home/hadoop/venv/bin/activate
cxs -c /home/hadoop/exp/cxs338.ini -s
