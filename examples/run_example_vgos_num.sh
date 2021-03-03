#!/bin/bash
# Run: source ./examples/run_example_vgos_num.sh
# 
is_legacy=1 python src/mapred_cx.py -c conf/correlx.ini --sort-numeric-pipeline -f exper=examples/test_dataset_vgos,serial=1,parallel=0
