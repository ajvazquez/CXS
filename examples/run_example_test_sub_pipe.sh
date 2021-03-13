#!/bin/bash
# Run: source ./examples/run_example_vgos.sh
# 
python cxs/parallel/hadoop/mapred_cx.py -c examples/test_dataset_test/sub/correlx.ini -f exper=examples/test_dataset_test/sub,serial=1,parallel=0
