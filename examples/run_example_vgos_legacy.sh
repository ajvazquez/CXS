#!/bin/bash
# Run: source ./examples/run_example_vgos.sh
# 
PYTHONPATH=src:$PYTHONPATH is_legacy=1 python src/mapred_cx.py -c conf/correlx.ini -f exper=examples/test_dataset_vgos,serial=1,parallel=0
