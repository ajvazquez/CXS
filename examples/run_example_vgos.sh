#!/bin/bash
# Run: source ./examples/run_example_vgos.sh
# 
python cxs/parallel/hadoop/mapred_cx.py -c conf/correlx.ini -f exper=examples/test_dataset_vgos,serial=1,parallel=0
