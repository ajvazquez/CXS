#!/bin/bash

PKG="s3://aj-bucket-test/emr/cxs338-0.0.1.tar.gz"
WDIR="/home/hadoop"
VENV=$WDIR"/venv"

# Get CXS
aws s3 cp $PKG $WDIR

# Dependencies
sudo yum install python3-devel -y

# Install virtualenv and CXS
virtualenv -p python3 $VENV
source $VENV/bin/activate
$VENV/bin/pip install $WDIR/cxs338-0.0.1.tar.gz
