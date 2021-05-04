#!/bin/bash

aws s3 cp s3://aj-bucket-test/emr/exp.zip /home/hadoop/
unzip /home/hadoop/exp.zip

/home/hadoop/venv/bin/activate
cxs -c /home/hadoop/exp/cxs338.ini -s
