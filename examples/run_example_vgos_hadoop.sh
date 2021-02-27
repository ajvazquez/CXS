#!/bin/bash
python -u src/mapred_cx.py -c conf/correlx.ini -f exper=examples/test_dataset_vgos/,serial=0,parallel=1,adjr=-1 -s correlx/logs/job_1 | tee logs/job_1.txt