#!/bin/bash

# Set frame size and number of frames per block
#FRAME=1032
FRAME=100032
FPB=1000

SUFFIX=6
OUT1="out4in_z"
OUT2="out4_z"

B=$(($FRAME*$FPB))

idx=-1
for f in "$@"; do
  ((idx++))
  outdir=$OUT2"_"$idx
  echo "Processing "$f"..."
  rm -rf $outdir
  mkdir $outdir

  rm -rf $OUT1
  mkdir $OUT1

  split --bytes=$B -d -a $SUFFIX $f $OUT1"/"
  count=`ls $OUT1| wc -l`

  for filename in `cd $OUT1;ls -1`; do
    newdir=$outdir"/"`basename $filename`
    mkdir $newdir
    mv $OUT1"/"$filename $newdir"/"`basename $f`
  done
  echo "Generated "$count" splits into "$outdir
done
