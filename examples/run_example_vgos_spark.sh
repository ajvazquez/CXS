#!/bin/bash
if [ -d "/opt/cx" ]; then
  python cxs/parallel/spark/spark_cx.py -c examples/test_dataset_vgos/cxs338.ini
else
  python cxs/parallel/spark/spark_cx.py -c examples/test_dataset_vgos/cxs338_local.ini
fi
